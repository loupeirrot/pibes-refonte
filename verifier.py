#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recette automatique de la refonte pibes.fr.

Usage :
    python3 verifier.py --lot 3              # contrôle dist/ pour les lots 1 à 3
    python3 verifier.py --lot 8 --staging    # recette du site de test (noindex attendu)
    python3 verifier.py --lot 4 --en-attente projets/ziwig.html   # page sans matière

Sortie : la liste des ERREURS (bloquantes) et des ALERTES (à lire), puis
« RECETTE OK » (code 0) ou « RECETTE KO » (code 1).

Ce script est le juge de chaque lot. Il ne dépend que de la bibliothèque
standard de Python 3. Ne pas le modifier pour faire passer un lot : si une
règle paraît fausse, l'écrire dans SUIVI.md et demander à Pierre.
"""
import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ICI = os.path.dirname(os.path.abspath(__file__))
VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
         "meta", "source", "track", "wbr"}
EXT_VIDEO = (".mp4", ".mov", ".webm", ".m4v", ".avi")
EXT_IMAGE = (".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg")
CHAMPS_FORMULAIRE = ["Name", "Email", "T-l-phone", "Subject", "Message", "honeypot"]


class Page(HTMLParser):
    """Relève ce dont la recette a besoin dans une page HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.balises = []          # (nom, attributs)
        self.ids = set()
        self.titres = []           # (niveau, texte)
        self.title = None
        self.jsonld = []
        self.visible = []          # texte hors script/style/blockquote
        self._captures = []        # [nom, [morceaux]]
        self._ignore = 0
        self._citation = 0
        self.doctype = False
        self._pile = []            # classes des éléments ouverts
        self._dernier = None       # classes du dernier élément fermé, sans texte depuis
        self.surtitres = []        # titres h1/h2 précédés d'un libellé

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, nom, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        self.balises.append((nom, a))
        classes = a.get("class", "")
        if re.search(r"surtitre|eyebrow|kicker", classes):
            self.surtitres.append(f"classe « {classes} »")
        if nom in ("h1", "h2") and self._dernier is not None \
                and re.search(r"\bmono\b", self._dernier):
            self.surtitres.append(f"libellé mono juste avant un <{nom}>")
        self._dernier = None
        if nom not in VIDES:
            self._pile.append((nom, classes))
        if "id" in a:
            self.ids.add(a["id"])
        if nom in ("script", "style"):
            self._ignore += 1
            if nom == "script" and a.get("type") == "application/ld+json":
                self._captures.append(["jsonld", []])
        elif nom == "blockquote":
            self._citation += 1
        elif nom == "title" or re.fullmatch(r"h[1-6]", nom):
            self._captures.append([nom, []])

    def handle_startendtag(self, nom, attrs):
        self.handle_starttag(nom, attrs)
        if nom not in VIDES:
            self.handle_endtag(nom)

    def handle_endtag(self, nom):
        while self._pile:
            n, classes = self._pile.pop()
            if n == nom:
                self._dernier = classes
                break
        if nom in ("script", "style"):
            self._ignore = max(0, self._ignore - 1)
            if self._captures and self._captures[-1][0] == "jsonld":
                self.jsonld.append("".join(self._captures.pop()[1]))
        elif nom == "blockquote":
            self._citation = max(0, self._citation - 1)
        elif self._captures and self._captures[-1][0] == nom:
            _, morceaux = self._captures.pop()
            texte = " ".join("".join(morceaux).split())
            if nom == "title":
                self.title = texte
            else:
                self.titres.append((int(nom[1]), texte))

    def handle_data(self, data):
        if data.strip():
            self._dernier = None
        for c in self._captures:
            c[1].append(data)
        if not self._ignore and not self._citation:
            self.visible.append(data)

    def premier(self, nom, **filtre):
        for n, a in self.balises:
            if n == nom and all(a.get(k) == v for k, v in filtre.items()):
                return a
        return None

    def tous(self, nom):
        return [a for n, a in self.balises if n == nom]


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def taille(chemin):
    try:
        return os.path.getsize(chemin)
    except OSError:
        return 0


def main():
    ap = argparse.ArgumentParser(description="Recette de la refonte pibes.fr")
    ap.add_argument("--lot", type=int, required=True, help="dernier lot terminé (1 à 8)")
    ap.add_argument("--dist", default=os.path.join(ICI, "dist"))
    ap.add_argument("--plan", default=os.path.join(ICI, "plan-site.json"))
    ap.add_argument("--en-attente", nargs="*", default=[], metavar="FICHIER",
                    help="pages du plan pas encore construites faute de matière "
                         "(seulement celles marquées peut_attendre dans le plan)")
    ap.add_argument("--staging", action="store_true",
                    help="site de test : toutes les pages doivent être en noindex")
    args = ap.parse_args()

    plan = json.loads(lire(args.plan))
    site = plan["site"]
    origine = site["origine"].rstrip("/")
    budgets = plan["budgets_octets"]
    dist = os.path.abspath(args.dist)
    erreurs, alertes = [], []

    def err(page, msg):
        erreurs.append(f"[{page}] {msg}")

    def alerte(page, msg):
        alertes.append(f"[{page}] {msg}")

    if not os.path.isdir(dist):
        print(f"ERREUR : dossier introuvable : {dist}")
        print("RECETTE KO")
        return 1

    prevues = {p["fichier"]: p for p in plan["pages"]}
    attente = set()
    for f in args.en_attente:
        motif = prevues.get(f, {}).get("peut_attendre")
        if not motif:
            err(f, "--en-attente refusé : cette page ne peut pas attendre")
        elif motif == "legal" and args.lot >= 8 and not args.staging:
            err(f, "--en-attente refusé : les pages légales sont obligatoires pour la mise en ligne")
        else:
            attente.add(f)
            alerte(f, "page en attente de matière (voir SUIVI.md)")
    exigees = [p for p in plan["pages"] if p["lot"] <= args.lot and p["fichier"] not in attente]

    # ---------- inventaire de dist ----------
    fichiers = []
    for racine, _, noms in os.walk(dist):
        for n in noms:
            rel = os.path.relpath(os.path.join(racine, n), dist).replace(os.sep, "/")
            fichiers.append(rel)
    ensemble = set(fichiers)

    for rel in fichiers:
        if rel.lower().endswith(EXT_VIDEO):
            err(rel, "fichier vidéo dans dist : les vidéos vont sur Bunny Stream ou YouTube")
        if rel.lower().endswith((".woff", ".ttf", ".otf", ".eot")):
            err(rel, "police : format woff2 uniquement")
        if rel.lower().endswith(".woff2") and taille(os.path.join(dist, rel)) > 150000:
            err(rel, "police de plus de 150 Ko : utiliser un sous-ensemble latin")
        if rel.lower().endswith(EXT_IMAGE) and not rel.lower().endswith(".svg"):
            if taille(os.path.join(dist, rel)) > budgets["image_max"]:
                err(rel, f"image de plus de {budgets['image_max'] // 1000} Ko")

    css_total = sum(taille(os.path.join(dist, r)) for r in fichiers if r.endswith(".css"))
    js_total = sum(taille(os.path.join(dist, r)) for r in fichiers if r.endswith(".js"))
    if css_total > budgets["css_total_max"]:
        err("css", f"CSS total {css_total} octets > {budgets['css_total_max']}")
    if js_total > budgets["js_total_max"]:
        err("js", f"JS total {js_total} octets > {budgets['js_total_max']}")

    # ---------- design : règles vérifiables dans le CSS (DESIGN.md) ----------
    css = "\n".join(lire(os.path.join(dist, r)) for r in fichiers if r.endswith(".css"))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    serre = re.sub(r"\s+", "", css).lower()
    if css:
        for nom, valeur in plan.get("jetons_obligatoires", {}).items():
            if f"{nom}:{valeur}" not in serre:
                err("css", f"jeton manquant ou modifié : {nom}: {valeur} (DESIGN.md)")
        for motif, quoi in [("prefers-reduced-motion", "bloc prefers-reduced-motion"),
                            (":focus-visible", "style :focus-visible"),
                            ("::selection", "style ::selection"),
                            ("text-wrap:balance", "text-wrap: balance sur les titres"),
                            ("color-scheme:dark", "color-scheme: dark"),
                            ("caret-color", "caret-color"),
                            ("font-display:swap", "font-display: swap")]:
            if motif not in serre:
                err("css", f"manque : {quoi} (DESIGN.md)")
        for motif, quoi in [(r"background-clip:text", "texte en dégradé (background-clip: text)"),
                            (r"transition(-property)?:all\b", "transition: all"),
                            (r"backdrop-filter:", "effet de verre (backdrop-filter)"),
                            (r"box-shadow:(?!none)", "ombre portée : le site est plat"),
                            (r"border-(left|right)(-width)?:(?:[2-9]|\d{2,})px", "bordure épaisse sur un côté"),
                            (r"transition[^;}]*[:,](width|height|top|left|right|bottom|margin)", "transition sur une propriété de mise en page"),
                            (r"(linear|radial|conic)-gradient\([^;}]*(#[0-9a-f]{3,8}|rgb)", "dégradé de couleurs")]:
            if re.search(motif, serre):
                err("css", f"interdit par DESIGN.md : {quoi}")
        for m in re.finditer(r"cubic-bezier\(([^)]*)\)", serre):
            try:
                v = [float(x) for x in m.group(1).split(",")]
                if len(v) == 4 and not (0 <= v[1] <= 1 and 0 <= v[3] <= 1):
                    err("css", f"courbe à rebond interdite : cubic-bezier({m.group(1)})")
            except ValueError:
                pass
        for m in re.finditer(r"font-size:([^;}]+)", serre):
            for rem in re.findall(r"(\d*\.?\d+)rem", m.group(1)):
                if float(rem) > 6:
                    err("css", f"corps de {rem}rem : 6rem au plus")
        for m in re.finditer(r"letter-spacing:(-\d*\.?\d+)em", serre):
            if float(m.group(1)) < -0.04:
                err("css", f"approche de {m.group(1)}em : -0.04em au plus serré")
    src_css = os.path.join(ICI, "src", "css")
    if os.path.isdir(src_css) and os.path.abspath(args.dist) == os.path.join(ICI, "dist"):
        for n in sorted(os.listdir(src_css)):
            if n.endswith(".css") and "jetons" not in n:
                t = re.sub(r"/\*.*?\*/", "", lire(os.path.join(src_css, n)), flags=re.S)
                t = re.sub(r"url\([^)]*\)", "", t)
                trouve = re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\boklch\(", t)
                if trouve:
                    err(f"src/css/{n}", f"couleur en dur ({trouve[0]}…) : toutes les couleurs sont dans 10-jetons.css")

    # ---------- analyse des pages ----------
    pages = {}
    for rel in fichiers:
        if rel.endswith(".html"):
            p = Page()
            brut = lire(os.path.join(dist, rel))
            p.feed(brut)
            p.brut = brut
            pages[rel] = p
            if rel not in prevues:
                alerte(rel, "page absente de plan-site.json (orpheline ?)")

    for p in exigees:
        if p["fichier"] not in pages:
            err(p["fichier"], f"page du lot {p['lot']} absente de dist")

    conserves = plan.get("serveur_a_conserver", [])
    hotes_medias = set(plan.get("hotes_medias_autorises", []))
    vus_titres, vus_desc = {}, {}

    def resoudre(page, valeur, balise):
        """Contrôle une URL trouvée dans une page."""
        v = valeur.strip()
        if not v or v.startswith(("data:", "javascript:")):
            if v.startswith("javascript:"):
                err(page, f"lien javascript: interdit ({v[:40]})")
            return None
        if v.startswith("mailto:"):
            if v[7:].split("?")[0].lower() != site["email"].lower():
                err(page, f"mailto inattendu : {v}")
            return None
        if v.startswith("tel:"):
            if re.sub(r"[^\d+]", "", v[4:]) != site["telephone"]:
                err(page, f"tel inattendu : {v} (attendu tel:{site['telephone']})")
            return None
        u = urlparse(v)
        if u.scheme in ("http", "https"):
            if u.scheme == "http":
                err(page, f"lien http non sécurisé : {v}")
            if balise == "a":
                return None
            if balise in ("img", "video", "source") and u.netloc in hotes_medias:
                return None
            err(page, f"ressource externe interdite dans <{balise}> : {v}")
            return None
        if v.startswith("//"):
            err(page, f"URL sans protocole interdite : {v}")
            return None
        if page == "404.html":
            # servie par Apache pour n'importe quelle adresse : ses liens partent de la racine
            if v.startswith("#"):
                return None
            if not v.startswith("/"):
                err(page, f"dans 404.html les liens partent de la racine (« /{v} ») : {v}")
                return None
            v = v[1:] or "index.html"
            u = urlparse(v)
        elif v.startswith("/"):
            err(page, f"lien absolu « {v} » : utiliser un lien relatif (aperçu local et dossier de test)")
            return None
        if v.startswith("#"):
            if len(v) > 1 and unquote(v[1:]) not in pages[page].ids:
                err(page, f"ancre introuvable : {v}")
            return None
        chemin = unquote(u.path)
        base = os.path.dirname(page)
        cible = os.path.normpath(os.path.join(base, chemin)).replace(os.sep, "/")
        if cible.startswith(".."):
            err(page, f"lien qui sort du site : {v}")
            return None
        cible_dossier = cible + "/" if chemin.endswith("/") else cible
        if any(cible_dossier == c or cible_dossier.startswith(c) for c in conserves):
            return None
        if chemin.endswith("/"):
            cible = cible + "/index.html"
        if cible not in ensemble:
            prevue = prevues.get(cible)
            if prevue and cible in attente:
                err(page, f"lien vers {cible}, page en attente : retirer le lien tant qu'elle n'existe pas")
            elif prevue and prevue["lot"] > args.lot:
                alerte(page, f"lien vers {cible}, page prévue au lot {prevue['lot']}")
            else:
                err(page, f"lien cassé : {v}")
            return None
        if u.fragment and cible in pages and unquote(u.fragment) not in pages[cible].ids:
            err(page, f"ancre introuvable dans {cible} : #{u.fragment}")
        return cible

    for rel, p in sorted(pages.items()):
        info = prevues.get(rel)
        bas = p.brut.lower()

        # structure
        if not p.doctype:
            err(rel, "<!doctype html> manquant")
        html = p.premier("html")
        if not html or html.get("lang") != site["langue"]:
            err(rel, f'<html lang="{site["langue"]}"> attendu')
        if not p.premier("meta", charset="utf-8") and not p.premier("meta", charset="UTF-8"):
            err(rel, '<meta charset="utf-8"> manquant')
        if not p.premier("meta", name="viewport"):
            err(rel, "meta viewport manquante")
        if len(p.tous("main")) != 1:
            err(rel, "il faut exactement un <main>")
        if p.tous("iframe"):
            err(rel, "<iframe> dans le HTML : YouTube se charge au clic (façade), jamais au chargement")

        # titres
        h1 = [t for n, t in p.titres if n == 1]
        if len(h1) != 1 or not h1[0]:
            err(rel, f"il faut exactement un <h1> non vide (trouvé : {len(h1)})")
        elif info and h1[0] != info["h1"]:
            err(rel, f"h1 « {h1[0]} » différent du plan « {info['h1']} »")
        precedent = 0
        for niveau, texte in p.titres:
            if niveau > precedent + 1:
                err(rel, f"saut de niveau de titre avant « {texte[:40]} » (h{precedent} puis h{niveau})")
            precedent = niveau

        # balises SEO
        desc = (p.premier("meta", name="description") or {}).get("content", "")
        if not p.title:
            err(rel, "<title> manquant")
        if info:
            if p.title != info["titre"]:
                err(rel, f"title « {p.title} » différent du plan")
            if desc != info["description"]:
                err(rel, "meta description différente du plan")
            attendu = origine + "/" + ("" if rel == "index.html" else rel)
            canon = (p.premier("link", rel="canonical") or {}).get("href")
            if canon != attendu:
                err(rel, f"canonical « {canon} », attendu « {attendu} »")
            for prop in ("og:title", "og:description", "og:image", "og:url", "og:type"):
                if not (p.premier("meta", property=prop) or {}).get("content"):
                    err(rel, f"balise {prop} manquante")
            og_image = (p.premier("meta", property="og:image") or {}).get("content", "")
            if og_image and not og_image.startswith(origine + "/"):
                err(rel, "og:image doit être une URL absolue du site")
        if p.title:
            if len(p.title) > 65:
                err(rel, f"title trop long ({len(p.title)} > 65)")
            vus_titres.setdefault(p.title, []).append(rel)
        if desc:
            if not 70 <= len(desc) <= 165:
                err(rel, f"description de {len(desc)} caractères (attendu 70 à 165)")
            vus_desc.setdefault(desc, []).append(rel)
        else:
            err(rel, "meta description manquante")
        robots = (p.premier("meta", name="robots") or {}).get("content", "").lower()
        doit_noindex = args.staging or bool(info and info.get("noindex"))
        if doit_noindex and "noindex" not in robots:
            err(rel, "noindex attendu sur cette page")
        if not doit_noindex and "noindex" in robots:
            err(rel, "noindex présent sur une page qui doit être indexée")

        # contenu interdit
        for chaine in plan["chaines_interdites"]:
            if chaine == "todo":
                trouve = re.search(r"\btodo\b", bas)
            else:
                trouve = chaine in bas
            if trouve:
                err(rel, f"chaîne interdite : « {chaine} »")
        visible = " ".join(" ".join(p.visible).split()).lower()
        if re.search(r"\b(nous|notre|nos)\b", visible):
            m = re.search(r".{0,30}\b(nous|notre|nos)\b.{0,30}", visible)
            err(rel, f"le site parle à la première personne du singulier (« je ») : …{m.group(0)}…")
        for mot in plan["mots_a_eviter"]:
            if mot in visible:
                alerte(rel, f"mot à éviter : « {mot} »")
        for motif in p.surtitres:
            err(rel, f"surtitre interdit au-dessus d'un titre ({motif}) : voir DESIGN.md")
        if "!" in visible:
            alerte(rel, "point d'exclamation dans le texte")
        if "→" in visible or "➜" in visible:
            alerte(rel, "flèche dans le texte : pas de flèche après un lien")
        if "—" in visible:
            alerte(rel, "tiret cadratin dans le texte : préférer deux-points, virgule ou point")

        # liens et ressources
        poids = taille(os.path.join(dist, rel))
        if poids > budgets["html_max"]:
            err(rel, f"HTML de {poids} octets > {budgets['html_max']}")
        locales = set()
        for nom, a in p.balises:
            if nom == "a":
                if "href" not in a:
                    continue
                resoudre(rel, a["href"], "a")
                if a.get("target") == "_blank" and "noopener" not in a.get("rel", ""):
                    err(rel, f'lien target="_blank" sans rel="noopener" : {a["href"]}')
            elif nom == "link":
                rels = a.get("rel", "").split()
                if "canonical" in rels or "alternate" in rels:
                    continue
                c = resoudre(rel, a.get("href", ""), "link")
                if c:
                    locales.add(c)
            elif nom == "script":
                if a.get("src"):
                    c = resoudre(rel, a["src"], "script")
                    if c:
                        locales.add(c)
                    if "defer" not in a and a.get("type") != "module":
                        err(rel, f"script sans defer : {a['src']}")
            elif nom == "img":
                if "alt" not in a:
                    err(rel, f"<img> sans attribut alt : {a.get('src')}")
                if not a.get("width") or not a.get("height"):
                    err(rel, f"<img> sans width/height : {a.get('src')}")
                if a.get("loading") != "lazy" and a.get("fetchpriority") != "high":
                    err(rel, f'<img> sans loading="lazy" (ou fetchpriority="high" pour l\'image principale) : {a.get("src")}')
                c = resoudre(rel, a.get("src", ""), "img")
                if c:
                    locales.add(c)
                for cand in a.get("srcset", "").split(","):
                    if cand.strip():
                        resoudre(rel, cand.strip().split()[0], "img")
            elif nom == "source":
                for cand in (a.get("srcset", "") or a.get("src", "")).split(","):
                    if cand.strip():
                        resoudre(rel, cand.strip().split()[0], "source")
            elif nom == "video":
                if a.get("preload") != "none":
                    err(rel, '<video> doit avoir preload="none"')
                if not a.get("poster"):
                    err(rel, "<video> sans poster")
                else:
                    c = resoudre(rel, a["poster"], "video")
                    if c:
                        locales.add(c)
                if "autoplay" in a:
                    err(rel, "<video autoplay> interdit dans le HTML : la lecture est lancée par le script")
                if a.get("src"):
                    resoudre(rel, a["src"], "video")
            elif nom == "button":
                if a.get("type") not in ("button", "submit"):
                    err(rel, "<button> sans type (button ou submit)")
        if sum(1 for a in p.tous("img") if a.get("fetchpriority") == "high") > 1:
            err(rel, 'une seule image fetchpriority="high" par page')
        total = poids + sum(taille(os.path.join(dist, c)) for c in locales)
        plafond = budgets["accueil_locale_max"] if rel == "index.html" else budgets["page_locale_max"]
        if total > plafond:
            err(rel, f"poids local au chargement {total} octets > {plafond}")

        # accessibilité de base
        if not any(a.get("href", "").startswith("#") and "evitement" in a.get("class", "")
                   for a in p.tous("a")):
            err(rel, 'lien d\'évitement manquant (<a class="evitement" href="#contenu">)')
        for a in p.tous("nav"):
            if not a.get("aria-label"):
                err(rel, "<nav> sans aria-label")

    for titre, ou in vus_titres.items():
        if len(ou) > 1:
            err(", ".join(ou), f"title en double : « {titre} »")
    for d, ou in vus_desc.items():
        if len(ou) > 1:
            err(", ".join(ou), "meta description en double")

    # ---------- accueil : données structurées ----------
    if "index.html" in pages:
        ok = False
        for bloc in pages["index.html"].jsonld:
            try:
                d = json.loads(bloc)
            except ValueError:
                err("index.html", "JSON-LD invalide")
                continue
            if d.get("@type") in ("ProfessionalService", "LocalBusiness"):
                ok = True
                if d.get("url") != origine + "/":
                    err("index.html", f"JSON-LD url ≠ {origine}/")
                if d.get("telephone") != site["telephone"]:
                    err("index.html", "JSON-LD telephone inattendu")
                if (d.get("address") or {}).get("addressLocality") != site["ville"]:
                    err("index.html", "JSON-LD address.addressLocality inattendu")
        if not ok:
            err("index.html", "JSON-LD ProfessionalService manquant")

    # ---------- contact : contrat du formulaire ----------
    if "contact.html" in pages:
        p = pages["contact.html"]
        noms = {a.get("name") for n, a in p.balises if n in ("input", "textarea", "select")}
        for champ in CHAMPS_FORMULAIRE:
            if champ not in noms:
                err("contact.html", f"champ « {champ} » manquant (contrat de form-handler.php)")
        if not p.tous("form"):
            err("contact.html", "<form> manquant")
        for n, a in p.balises:
            if n in ("input", "textarea", "select") and a.get("type") != "hidden" \
                    and a.get("name") != "honeypot":
                ident = a.get("id")
                if not ident or not any(l.get("for") == ident for l in p.tous("label")):
                    err("contact.html", f"champ « {a.get('name')} » sans <label for>")
        scripts = " ".join(lire(os.path.join(dist, r)) for r in fichiers if r.endswith(".js"))
        if "form-handler.php" not in scripts and "form-handler.php" not in p.brut:
            err("contact.html", "aucune référence à form-handler.php")

    # ---------- fichiers serveur (à partir du lot 7) ----------
    if args.lot >= 7:
        if "robots.txt" not in ensemble:
            err("robots.txt", "fichier manquant")
        else:
            r = lire(os.path.join(dist, "robots.txt"))
            if f"Sitemap: {origine}/sitemap.xml" not in r:
                err("robots.txt", f"ligne « Sitemap: {origine}/sitemap.xml » manquante")
            if args.staging and "Disallow: /" not in r:
                alerte("robots.txt", "site de test : « Disallow: / » conseillé")
        if "sitemap.xml" not in ensemble:
            err("sitemap.xml", "fichier manquant")
        else:
            locs = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", lire(os.path.join(dist, "sitemap.xml"))))
            attendues = {origine + "/" + ("" if p["fichier"] == "index.html" else p["fichier"])
                         for p in exigees if p.get("sitemap", True)}
            for u in sorted(attendues - locs):
                err("sitemap.xml", f"URL manquante : {u}")
            for u in sorted(locs - attendues):
                err("sitemap.xml", f"URL en trop : {u}")
        if ".htaccess" not in ensemble:
            err(".htaccess", "fichier manquant")
        else:
            lignes = lire(os.path.join(dist, ".htaccess")).splitlines()
            actives = [l.strip() for l in lignes if l.strip() and not l.strip().startswith("#")]
            for r in plan["redirections"]:
                if not any(re.search(r"\b301\b", l) and r["de"] in l.split() and r["vers"] in l.split()
                           for l in actives):
                    err(".htaccess", f"redirection 301 manquante : {r['de']} -> {r['vers']}")
            for chemin in plan["disparues_410"]:
                if not any(chemin.rstrip("/") in l and ("gone" in l.lower() or "410" in l or "[G" in l)
                           for l in actives):
                    err(".htaccess", f"réponse 410 manquante pour {chemin}")
            texte = "\n".join(actives)
            if "ErrorDocument 404" not in texte:
                err(".htaccess", "ErrorDocument 404 manquant")
            if "https" not in texte.lower():
                err(".htaccess", "redirection vers https manquante")
        if site["image_partage"] not in ensemble:
            err(site["image_partage"], "image de partage (og:image) manquante")
        if not any(r.startswith("favicon") for r in fichiers):
            err("favicon", "favicon manquant à la racine")

    # ---------- bilan ----------
    print(f"Recette du lot {args.lot} — {len(pages)} pages, {len(fichiers)} fichiers dans {dist}")
    for a in alertes:
        print("ALERTE  " + a)
    for e in erreurs:
        print("ERREUR  " + e)
    print(f"{len(erreurs)} erreur(s), {len(alertes)} alerte(s)")
    print("RECETTE KO" if erreurs else "RECETTE OK")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
