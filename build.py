#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le site pibes.fr : src/ + statique/ -> dist/.

Usage :
    python3 build.py              # version de production
    python3 build.py --staging    # version de test (/v2/) : tout en noindex, robots.txt fermé

Contrat : ARCHITECTURE.md, §5. Python 3 standard, aucune dépendance.
Le dossier dist/ n'est jamais vidé (la suppression est refusée sur ce poste) :
les fichiers sont écrasés, et ceux qui ne sont plus produits sont listés à la fin
pour que Pierre les supprime à la main.
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, "src")
DIST = os.path.join(ICI, "dist")
STATIQUE = os.path.join(ICI, "statique")

# Scripts chargés selon le gabarit (ARCHITECTURE.md §5.4)
SCRIPTS = {
    "accueil": ["site.js", "video.js"],
    "offre": ["site.js", "video.js"],
    "realisations": ["site.js", "video.js"],
    "etude": ["site.js", "video.js"],
    "contact": ["site.js", "contact.js"],
    "simple": ["site.js"],
    "liens": [],
}

ICONE_LECTURE = ('<svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true" focusable="false">'
                 '<path d="M2 .8v10.4a.6.6 0 0 0 .9.5l8.4-5.2a.6.6 0 0 0 0-1L2.9.3A.6.6 0 0 0 2 .8z"/></svg>')

produits = []      # chemins relatifs à dist/, pour MANIFESTE.txt
ecrits = 0


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def ecrire(rel, contenu):
    """Écrit dist/rel seulement si le contenu change (ni suppression, ni vidage)."""
    global ecrits
    chemin = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    donnees = contenu.encode("utf-8") if isinstance(contenu, str) else contenu
    if not os.path.exists(chemin) or open(chemin, "rb").read() != donnees:
        with open(chemin, "wb") as f:
            f.write(donnees)
        ecrits += 1
    produits.append(rel.replace(os.sep, "/"))


def copier(source, rel):
    with open(source, "rb") as f:
        ecrire(rel, f.read())


def attr(texte):
    return html.escape(texte, quote=True)


def minifier_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip() + "\n"


def partiel(nom):
    chemin = os.path.join(SRC, "partiels", nom + ".html")
    if not os.path.exists(chemin):
        sys.exit(f"ERREUR : partiel introuvable : src/partiels/{nom}.html")
    return lire(chemin)


def inclure(texte, profondeur=0):
    if profondeur > 8:
        sys.exit("ERREUR : inclusions de partiels trop imbriquées")
    return re.sub(r"\{\{>\s*([\w-]+)\s*\}\}",
                  lambda m: inclure(partiel(m.group(1)), profondeur + 1), texte)


def grille_reels(projets, public=None, ident=None):
    """Grille de reels générée depuis projets.json (lisible sans JavaScript).
    {{reels}} : tous ; {{reels:public}} : un public ; {{reel:id}} : un seul reel."""
    reels = [p for p in projets["projets"] if p["type"] == "reel"
             and (public is None or public in p.get("public", []))
             and (ident is None or p["id"] == ident)]
    lignes = ['<ul class="grille-reels">']
    for p in reels:
        titre, sous = p["titre"], p["sous_titre"]
        lignes.append(
            f'<li><a class="reel" href="https://iframe.mediadelivery.net/play/{projets["bunny"]["bibliotheque"]}/{p["video"]}"'
            f' data-video="{attr(p["video"])}" data-titre="{attr(titre)}" data-sous="{attr(sous)}"'
            f' aria-label="{attr(f"Lire le reel {titre}, {sous}")}">'
            f'<span class="reel-cadre"><span class="reel-zoom">'
            f'<img src="{{{{racine}}}}assets/img/{p["vignette"]}.jpg" alt="" width="720" height="1280" loading="lazy" decoding="async">'
            f'</span><span class="reel-icone">{ICONE_LECTURE}</span><span class="reel-avance"></span></span>'
            f'<span class="legende"><b>{html.escape(titre)}.</b> {html.escape(sous)}.</span></a></li>')
    lignes.append("</ul>")
    return "\n".join(lignes)


def grille_films(projets):
    """Cartes des films (façade YouTube) ; lien vers l'étude de cas seulement si sa page existe."""
    films = [p for p in projets["projets"] if p["type"] == "film"]
    lignes = ['<ul class="grille-films">']
    for p in films:
        titre, sous, vid = p["titre"], p["sous_titre"], p["video"]
        vign = None
        for cand in (p.get("vignette"), (p.get("vignette") or "") + "-miniature"):
            if cand and os.path.exists(os.path.join(STATIQUE, "assets", "img", f"{cand}-960.webp")):
                vign = cand
                break
        if vign:
            media = (f'<img src="{{{{racine}}}}assets/img/{vign}-960.webp"'
                     f' srcset="{{{{racine}}}}assets/img/{vign}-480.webp 480w, {{{{racine}}}}assets/img/{vign}-960.webp 960w"'
                     f' sizes="(min-width: 768px) 46vw, 92vw" width="960" height="536" alt="" loading="lazy" decoding="async">')
            classe = "film-bouton"
        else:
            media = ""
            classe = "film-bouton film-sans-image"
        etude = p.get("etude")
        lien = ""
        if etude and os.path.exists(os.path.join(SRC, "pages", etude)):
            lien = f'<a class="lien" href="{{{{racine}}}}{etude}">Lire l\u2019étude de cas</a>'
        lignes.append(
            f'<li class="film"><div class="film-cadre"><a class="{classe}" href="https://www.youtube.com/watch?v={attr(vid)}"'
            f' data-youtube="{attr(vid)}" data-titre="{attr("Lecteur YouTube : " + titre)}"'
            f' aria-label="{attr(f"Lire le film {titre} sur YouTube")}">{media}'
            f'<span class="film-icone">{ICONE_LECTURE}</span></a></div>'
            f'<p class="legende"><b>{html.escape(titre)}.</b> {html.escape(sous)}.</p>{lien}</li>')
    lignes.append("</ul>")
    return "\n".join(lignes)


def video_ouverture(site, apercu):
    """Balise <video> de l'ouverture de l'accueil (ARCHITECTURE.md, F4).
    En ligne : MP4 de Bunny Stream (site.video_ouverture = identifiant Bunny).
    Aperçu GitHub : fichiers de medias/web/, copiés dans apercu/assets/video/.
    Sans l'un ni l'autre : rien, l'image fixe reste seule."""
    if apercu:
        grand = "{{racine}}assets/video/ouverture-1080.mp4"
        petit = "{{racine}}assets/video/ouverture-720.mp4"
    elif site.get("video_ouverture"):
        base = f"https://{site.get('cdn_bunny', 'vz-25e90935-e10.b-cdn.net')}/{site['video_ouverture']}"
        grand, petit = f"{base}/play_720p.mp4", f"{base}/play_480p.mp4"
    else:
        return ""
    return (f'<video class="ouverture-video" muted loop playsinline preload="none" aria-hidden="true"'
            f' poster="{{{{racine}}}}assets/img/ouverture-960.webp" data-src="{grand}" data-src-petit="{petit}"></video>')


def json_ld(site, origine):
    donnees = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": site["nom"],
        "description": "Vidéaste à Capbreton : mini-documentaires, reels, photos et sites internet.",
        "url": origine + "/",
        "telephone": site["telephone"],
        "email": site["email"],
        "image": origine + "/" + site["image_partage"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": site["ville"],
            "postalCode": site["code_postal"],
            "addressRegion": "Landes",
            "addressCountry": "FR",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Landes"},
            {"@type": "AdministrativeArea", "name": "Pyrénées-Atlantiques"},
        ],
        "sameAs": [
            "https://www.instagram.com/pierre.bargeles/",
            "https://www.linkedin.com/in/pierre-bargeles/",
            "https://www.facebook.com/profile.php?id=61572107414089",
        ],
    }
    texte = json.dumps(donnees, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{texte}\n</script>'


def main():
    ap = argparse.ArgumentParser(description="Construit dist/ à partir de src/")
    ap.add_argument("--staging", action="store_true", help="site de test : noindex partout")
    ap.add_argument("--apercu", action="store_true",
                    help="aperçu GitHub Pages : écrit dans apercu/ (pas dans dist/), noindex, "
                         "et sert la vidéo d'ouverture depuis medias/web/ au lieu de Bunny")
    args = ap.parse_args()

    plan = json.loads(lire(os.path.join(ICI, "plan-site.json")))
    projets = json.loads(lire(os.path.join(SRC, "donnees", "projets.json")))
    site = plan["site"]
    origine = site["origine"].rstrip("/")
    global DIST
    if args.apercu:
        args.staging = True
        DIST = os.path.join(ICI, "apercu")
    os.makedirs(DIST, exist_ok=True)

    # ---------- CSS et JS ----------
    dossier_css = os.path.join(SRC, "css")
    css = "".join(lire(os.path.join(dossier_css, n)) + "\n"
                  for n in sorted(os.listdir(dossier_css)) if n.endswith(".css"))
    css = minifier_css(css)
    dossier_js = os.path.join(SRC, "js")
    js = {n: lire(os.path.join(dossier_js, n)) for n in sorted(os.listdir(dossier_js)) if n.endswith(".js")}
    version = hashlib.sha256((css + "".join(js.values())).encode("utf-8")).hexdigest()[:8]
    ecrire("assets/css/site.css", css)
    for n, contenu in js.items():
        ecrire(f"assets/js/{n}", contenu)

    # ---------- fichiers statiques ----------
    if os.path.isdir(STATIQUE):
        for racine, _, noms in os.walk(STATIQUE):
            for n in sorted(noms):
                if n.startswith(".") and n != ".htaccess":
                    continue  # .DS_Store et autres fichiers cachés
                source = os.path.join(racine, n)
                copier(source, os.path.relpath(source, STATIQUE))

    # ---------- aperçu GitHub : vidéo d'ouverture servie depuis le dépôt ----------
    if args.apercu:
        web = os.path.join(ICI, "medias", "web")
        for n in ("ouverture-1080.mp4", "ouverture-720.mp4"):
            if os.path.exists(os.path.join(web, n)):
                copier(os.path.join(web, n), "assets/video/" + n)

    # ---------- pages ----------
    annee = str(datetime.date.today().year)
    tete, entete, pied = partiel("tete"), partiel("entete"), partiel("pied")
    construites, ignorees = [], []
    for page in plan["pages"]:
        fichier = page["fichier"]
        source = os.path.join(SRC, "pages", fichier)
        if not os.path.exists(source):
            ignorees.append(f"{fichier} (lot {page['lot']})")
            continue
        if fichier == "404.html":
            racine = "/"
        else:
            racine = "../" * fichier.count("/")
        gabarit = page["gabarit"]
        if gabarit == "liens":
            # page de liens (bio des réseaux) : ni en-tête ni pied de page
            corps = (tete + '<main id="contenu">\n' + lire(source).strip() + "\n</main>\n{{scripts}}\n</body>\n</html>\n")
        else:
            corps = (tete + entete + '<main id="contenu">\n' + lire(source).strip() + "\n</main>\n" + pied)
        corps = inclure(corps)

        # grilles de reels générées depuis projets.json : {{reels}} ou {{reels:artisan}}
        corps = corps.replace("{{films}}", grille_films(projets))
        # liens légaux du pied de page : seulement si les pages existent (F7)
        for legal in ("mentions-legales.html", "confidentialite.html"):
            if not os.path.exists(os.path.join(SRC, "pages", legal)):
                corps = re.sub(r'\s*<a class="lien" href="[^"]*' + re.escape(legal) + r'">[^<]*</a>', "", corps)
        corps = re.sub(r"\{\{reels(?::([\w-]+))?\}\}", lambda m: grille_reels(projets, m.group(1)), corps)
        corps = re.sub(r"\{\{reel:([\w-]+)\}\}", lambda m: grille_reels(projets, ident=m.group(1)), corps)

        scripts = []
        for n in SCRIPTS.get(gabarit, ["site.js"]):
            if n in js:
                scripts.append(f'<script src="{{{{racine}}}}assets/js/{n}?v={{{{version}}}}" defer></script>')
            else:
                print(f"  attention : {n} manquant pour {fichier} (gabarit {gabarit})")
        noindex = args.staging or page.get("noindex", False)
        canonique = origine + "/" + ("" if fichier == "index.html" else fichier)
        jetons = {
            "scripts": "\n".join(scripts),
            "robots": '<meta name="robots" content="noindex">' if noindex else "",
            "jsonld": json_ld(site, origine) if fichier == "index.html" else "",
            "titre": attr(page["titre"]),
            "description": attr(page["description"]),
            "canonique": canonique,
            "og_image": origine + "/" + site["image_partage"],
            "annee": annee,
            "email": site["email"],
            "telephone": site["telephone"],
            "telephone_affiche": site["telephone_affiche"],
            "video_ouverture": video_ouverture(site, args.apercu) if fichier == "index.html" else "",
        }
        # deux passes : les jetons insérés peuvent en contenir d'autres ({{racine}}, {{version}})
        for _ in range(2):
            corps = re.sub(r"\{\{(\w+)\}\}", lambda m: jetons.get(m.group(1), m.group(0)), corps)
            jetons.update({"racine": racine, "version": version})
        reste = re.findall(r"\{\{[^}]*\}\}", corps)
        if reste:
            sys.exit(f"ERREUR : jeton inconnu dans {fichier} : {reste[0]}")

        # navigation : lien de la page en cours
        corps = corps.replace(f'data-page="{fichier}"', 'aria-current="page"')
        corps = re.sub(r'\sdata-page="[^"]*"', "", corps)
        corps = re.sub(r"\n\s*\n+", "\n", corps)
        ecrire(fichier, corps)
        construites.append(page)

    # ---------- sitemap, robots, .htaccess ----------
    aujourdhui = datetime.date.today().isoformat()
    urls = []
    for page in construites:
        if page.get("sitemap", True) and not page.get("noindex"):
            loc = origine + "/" + ("" if page["fichier"] == "index.html" else page["fichier"])
            urls.append(f"  <url><loc>{loc}</loc><lastmod>{aujourdhui}</lastmod></url>")
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    if args.staging:
        robots = "# Site de test : ne pas indexer\nUser-agent: *\nDisallow: /\n"
    else:
        robots = "User-agent: *\nAllow: /\n"
    ecrire("robots.txt", robots + f"\nSitemap: {origine}/sitemap.xml\n")

    base = lire(os.path.join(SRC, "serveur", "htaccess.base")).rstrip() + "\n"
    lignes = ["", "# ---------- Anciennes adresses (générées depuis plan-site.json) ----------",
              "<IfModule mod_alias.c>"]
    lignes += [f"  Redirect 301 {r['de']} {r['vers']}" for r in plan["redirections"]]
    lignes += [f"  Redirect gone {c}" for c in plan["disparues_410"]]
    lignes.append("</IfModule>")
    ecrire(".htaccess", base + "\n".join(lignes) + "\n")

    # ---------- manifeste ----------
    liste = sorted(set(produits))
    manifeste = ("# Fichiers produits par build.py" + (" --staging" if args.staging else "")
                 + f" le {aujourdhui}\n" + "\n".join(liste) + "\n")
    chemin_manifeste = os.path.join(DIST, "MANIFESTE.txt")
    if not os.path.exists(chemin_manifeste) or lire(chemin_manifeste) != manifeste:
        with open(chemin_manifeste, "w", encoding="utf-8") as f:
            f.write(manifeste)
    attendus = set(liste) | {"MANIFESTE.txt"}
    orphelins = []
    for racine, _, noms in os.walk(DIST):
        for n in noms:
            rel = os.path.relpath(os.path.join(racine, n), DIST).replace(os.sep, "/")
            if rel not in attendus:
                orphelins.append(rel)

    print(f"Construit {len(construites)} page(s) dans {os.path.basename(DIST)}/" + (" (staging : noindex)" if args.staging else "")
          + f", {len(liste)} fichiers, {ecrits} écrit(s) ou modifié(s), version {version}")
    for i in ignorees:
        print(f"  ignorée, pas encore de source : {i}")
    if orphelins:
        print("Fichiers de dist/ qui ne sont plus produits (à supprimer à la main) :")
        for o in sorted(orphelins):
            print(f"  {o}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
