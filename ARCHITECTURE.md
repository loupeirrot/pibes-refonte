# Refonte pibes.fr : architecture

Document de référence pour tout modèle qui travaille sur la refonte. Rédigé le 16/11/2026.
Fichiers liés, dans ce même dossier : `DESIGN.md` (charte et composants : la source de vérité du design), `PRODUCT.md` (le produit en une page), `skills/` (skills de design Impeccable et Taste), `plan-site.json` (pages, balises, redirections, budgets), `CONTENU.md` (textes), `LOTS.md` (découpage du travail), `SUIVI.md` (état d'avancement et matière attendue), `verifier.py` (recette automatique).

## 0. Règles non négociables

1. **Un lot par session**, sauf si Pierre demande d'en enchaîner plusieurs. Lire `SUIVI.md`, faire le lot demandé, lancer la recette, mettre `SUIVI.md` à jour, s'arrêter. En cas d'enchaînement : un lot ne commence que quand le précédent affiche `RECETTE OK` et que `SUIVI.md` est à jour.
2. **Le juge est `verifier.py`**, pas le modèle ni Pierre. Un lot est terminé quand `python3 verifier.py --lot N` affiche `RECETTE OK`. Ne jamais modifier `verifier.py` ni `plan-site.json` pour faire passer un lot. Si une règle semble fausse, l'écrire dans `SUIVI.md` (rubrique « Questions pour Pierre ») et s'arrêter sur ce point.
3. **Ne rien inventer.** Pas de témoignage, de chiffre, de client, de prix, de délai ou de date qui ne figure pas dans `CONTENU.md` ou dans un fichier fourni par Pierre. Pas de photo de banque d'images ni d'image générée présentée comme son travail.
4. **Matière manquante = bloc absent.** Un passage marqué `[À FOURNIR Fx : …]` ou `[À CONFIRMER Fx : …]` dans `CONTENU.md` n'est jamais rempli par supposition. Tant que Pierre n'a pas fourni l'élément (voir `SUIVI.md`), le bloc entier est laissé hors de la page. La recette refuse toute page qui contient encore un de ces marqueurs. Une page entière restée sans matière (étude de cas, page légale) n'est pas construite et se déclare à la recette avec `--en-attente` (voir `LOTS.md`).
5. **Pas de prix sur le site** en version 1 (décision de Pierre du 16/11/2026). Les emplacements sont prévus, vides.
6. **Le site dit « je » et vouvoie le visiteur.** Jamais « nous », « notre », « nos » (la recette le contrôle, hors citations de clients dans `<blockquote>`).
7. **Ne jamais supprimer** un fichier du dossier de Pierre ni du serveur sans qu'il le demande. Dans le dossier connecté, la suppression est d'ailleurs refusée par le système (voir §3).
8. **Aucune dépendance à installer pour construire le site.** Python 3 de base uniquement pour `build.py`.
9. **Avant de toucher à l'interface** (HTML d'une page, CSS, animation) : lire `DESIGN.md` en entier, puis `skills/impeccable/reference/craft-floor.md`. `DESIGN.md` fixe l'identité ; les skills servent à mieux l'exécuter, jamais à la remplacer (`skills/LISEZMOI.md`).

## 1. À quoi sert le site

Pierre Bargelès est vidéaste indépendant à Capbreton (Landes). 20 ans d'audiovisuel, dont 18 à France Télévisions (postes techniques de régie et de car de production, pas réalisateur : ne jamais écrire « réalisateur à France Télévisions »).

Le site doit faire trois choses, dans cet ordre :
1. En 5 secondes, faire comprendre : **il filme l'histoire d'une entreprise et en tire toute sa communication** (film, reels, photos, site).
2. Montrer des preuves : le film Optima by Delwood en tête, puis les reels.
3. Amener à un contact qualifié (qui, quel projet, quel budget).

Deux publics, deux portes d'entrée dès l'accueil :
- **Entreprises, marques, institutions** avec un budget de communication : mini-documentaire et communication globale. C'est la cible à développer.
- **Artisans, commerçants, indépendants** : reels, photos, présentation filmée. Pierre les garde pour l'instant parce qu'ils le font connaître.

Pierre ne fait pas de gestion de réseaux sociaux au quotidien. Il livre un stock de contenus et peut automatiser leur publication. Le site le dit clairement.

## 2. Décisions d'architecture

| Sujet | Décision | Raison |
|---|---|---|
| Technologie | Site statique HTML/CSS/JS écrit à la main, assemblé par `build.py` (Python standard) | Aucun abonnement, aucun framework à maintenir, lisible par Pierre (il connaît HTML/CSS), facile à reprendre par n'importe quel modèle |
| Webflow | Abandonné pour ce site | L'export actuel traîne des restes du gabarit « Play », pèse 25 Mo à l'accueil et se modifie mal à la main |
| Hébergement | OVH mutualisé, inchangé (Apache + PHP) | Le formulaire repose sur `form-handler.php` ; la page `/portfolio/` y vit déjà |
| Vidéos | Jamais dans le site. Reels sur Bunny Stream (bibliothèque `801824`, CDN `vz-25e90935-e10.b-cdn.net`), films longs sur YouTube chargés au clic | L'espace OVH est plein ; le poids de l'accueil doit passer de 25 Mo à moins de 3 Mo |
| Adresses | Fichiers `.html` à la racine, liens **relatifs** partout (sauf `404.html`) | Le site s'ouvre par double-clic sur l'ordinateur de Pierre et fonctionne tel quel dans un dossier de test `/v2/` ; `projets.html` et `contact.html` gardent leur adresse |
| Adresse canonique | `https://www.pibes.fr` | Le serveur redirige déjà vers `www` |
| Charte | Celle de la page `/portfolio/` en ligne, relevée dans son CSS et écrite dans `DESIGN.md`, resserrée avec les skills Impeccable et Taste | Déjà choisie par Pierre en novembre 2026 ; les deux doivent se ressembler |
| Polices | Geist et Geist Mono hébergées sur le site, en `woff2` | Pas de requête vers un tiers, meilleur temps de chargement |
| Scripts tiers | Aucun. Pas d'outil de statistiques ni de bandeau cookies en version 1 | Rien n'est déposé avant un clic du visiteur. Les demandes se comptent dans les envois du formulaire, le trafic dans Search Console |
| Fichiers du site | Tout sous `assets/` (`assets/css`, `assets/js`, `assets/img`, `assets/fonts`) | Aucun mélange avec les dossiers de l'ancien site (`css/`, `js/`, `images/`, `videos/`, `fonts/`), que Pierre pourra supprimer d'un bloc après la bascule |
| Prix | Non affichés en version 1 | Décision de Pierre. Repère pour les afficher : 2 contrats de plus de 2 000 € signés sur 3 mois de suite |

## 3. Environnement de travail

- Dossier de travail sur l'ordinateur de Pierre : `Documents/Claude/Projects/Pibes/Site pibes.fr/refonte/`. Y travailler directement avec le terminal du poste (`device_bash`, dossier monté sous `$HOME/mnt/Pibes/`). Ne pas travailler sur une copie dans le cloud : Pierre ne la verrait pas.
- Outils vérifiés sur ce poste le 16/11/2026 : Python 3.10, Pillow 12.3, ffmpeg avec `libwebp` et `libaom-av1`, Node et npm (registre npm joignable).
- **Suppression impossible** : `rm` et `os.remove` échouent (« Operation not permitted »). Écraser un fichier et le renommer fonctionnent. Conséquences : `build.py` ne vide jamais `dist/`, il écrase. Ne pas créer de fichiers temporaires dans le dossier ; utiliser `/tmp`.
- Réseau du poste : limité. `curl https://pibes.fr` est refusé. Pour lire le site en ligne, utiliser le navigateur intégré.
- L'ancien site (export Webflow) n'est pas dans ce dossier. La version corrigée des pages actuelles est dans `../corrections-etape0/` : elle sert de référence pour les anciens textes, pas de base de code.
- Références de style et de comportement : `../../Claude outputs/prompt_portfolio.md` (cahier des charges de la page portfolio : grille de reels, lecteur plein écran) et, si Pierre l'a déposé, `reference/portfolio/index.html` (code de la page en ligne).

## 4. Arborescence du dossier `refonte/`

```
refonte/
  ARCHITECTURE.md  CONTENU.md  LOTS.md  SUIVI.md
  DESIGN.md  PRODUCT.md   charte et fiche produit (format lu par le skill Impeccable)
  skills/                 skills de design : impeccable/, taste-skill/, LISEZMOI.md
  plan-site.json          pages, balises, redirections, budgets (ne pas modifier)
  verifier.py             recette (ne pas modifier)
  build.py                assemble src/ vers dist/                      [lot 1]
  optimiser.py            fabrique les images web depuis medias/        [lot 6]
  src/
    partiels/             tete.html, entete.html, pied.html, + composants réutilisés
    pages/                un fichier par page du plan : contenu de <main> seulement
    css/                  10-jetons.css, 20-base.css, 30-composants.css, 40-pages.css
    js/                   site.js, video.js, contact.js
    donnees/projets.json  films et reels (fourni, à compléter par Pierre)
    serveur/htaccess.base bloc fixe du .htaccess
  medias/originaux/       images sources déposées par Pierre (jamais mises en ligne)
  statique/               copié tel quel à la racine de dist/ (assets/img, assets/fonts, favicon)
  reference/              fichiers déposés par Pierre (portfolio, form-handler.php)
  dist/                   le site construit : c'est ce dossier qui part sur OVH
```

## 5. `build.py` : contrat

`python3 build.py` construit `dist/`. `python3 build.py --staging` construit la version de test (toutes les pages en `noindex`, `robots.txt` avec `Disallow: /`).

Pour chaque page de `plan-site.json` dont le fichier `src/pages/<fichier>` existe :
1. Assembler `tete.html` + `entete.html` + `<main id="contenu">` + contenu de la page + `</main>` + `pied.html`.
2. Remplacer les jetons : `{{racine}}` (vide à la racine, `../` dans `projets/`, `/` pour `404.html`), `{{titre}}`, `{{description}}`, `{{canonique}}`, `{{og_image}}` (URL absolue), `{{annee}}`, `{{version}}` (8 premiers caractères d'un hachage du CSS et du JS, pour `site.css?v=…`), `{{> nom}}` (inclut `src/partiels/nom.html`), et les champs de `site` : `{{email}}`, `{{telephone}}`, `{{telephone_affiche}}`.
3. Dans la navigation, ajouter `aria-current="page"` au lien de la page en cours.
4. Scripts chargés selon le gabarit : `site.js` partout ; `video.js` pour `accueil`, `offre`, `realisations`, `etude` ; `contact.js` pour `contact`. Toujours avec `defer`.
5. Pour `index.html`, générer le bloc JSON-LD `ProfessionalService` à partir de `site` (nom, url, telephone, email, adresse : ville et code postal, zone : Landes et Pyrénées-Atlantiques, liens Instagram, LinkedIn, Facebook).

Puis :
- concaténer `src/css/*.css` dans l'ordre alphabétique vers `dist/assets/css/site.css` (commentaires et blancs retirés) ;
- copier `src/js/` vers `dist/assets/js/` et `statique/` vers `dist/` ;
- générer `dist/sitemap.xml` (pages du plan construites, sauf `"sitemap": false`), `dist/robots.txt`, `dist/.htaccess` (`src/serveur/htaccess.base` + une ligne `Redirect 301 <de> <vers>` par redirection du plan + une ligne `Redirect gone <chemin>` par entrée de `disparues_410`) ;
- écrire `dist/MANIFESTE.txt` (liste des fichiers produits) et afficher les fichiers de `dist/` qui n'y figurent plus, pour que Pierre les supprime à la main.

Une page du plan sans fichier source est ignorée avec un message : elle appartient à un lot à venir.

## 6. Charte graphique

Toute la charte est dans `DESIGN.md` : couleurs, typographie, mise en page, formes, composants, mouvement, interdits. C'est la seule source de vérité du design ; ce document ne la répète pas.

- Les jetons CSS à copier dans `10-jetons.css` sont dans `DESIGN.md`, section Colors.
- Polices : récupérer les `woff2` variables (sous-ensemble latin) dans les paquets npm `@fontsource-variable/geist` et `@fontsource-variable/geist-mono` (télécharger dans `/tmp`, copier seulement les `woff2` utiles dans `statique/assets/fonts/`). `font-display: swap`, précharger la police de texte.
- Conception d'abord pour 390 px de large, puis 768, 1024 et 1440 px.
- `verifier.py` contrôle ce qui se vérifie dans le code : jetons présents, aucune couleur en dur hors de `10-jetons.css`, pas de texte en dégradé, d'ombre portée, d'effet de verre, de `transition: all`, de courbe à rebond, de corps au-dessus de 6rem, de surtitre au-dessus d'un `h1` ou d'un `h2`.

## 7. Gabarits et composants

Gabarits (champ `gabarit` du plan) : `accueil`, `offre`, `realisations`, `etude`, `contact`, `simple`.

Composants à écrire une fois dans `30-composants.css` et à réutiliser. Leur apparence et leurs états sont décrits dans `DESIGN.md` (section Components) :

| Composant | Rôle |
|---|---|
| `entete` | Logo texte « Pierre Bargelès », navigation, bouton « Parler de votre projet ». Menu plein écran sur mobile, bouton avec `aria-expanded` |
| `pied` | Coordonnées, liens des offres, liens utiles, réseaux, mentions |
| `ouverture` | Bloc d'ouverture d'une page : `h1` sur deux lignes, chapeau, boutons, média. Seul bloc animé au chargement |
| `portes` | Les deux publics de l'accueil : deux colonnes séparées par un filet, sans boîte |
| `liste-offres` | Trois rangées séparées par des filets, la première plus grande avec l'image du film. Pas de cartes égales |
| `frise` | Frise de montage avec tête de lecture ambre : la méthode en 4 étapes, le parcours de la page À propos. Motif du site |
| `barre-mobile` | Barre fixe en bas d'écran sous 960 px : Appeler, Écrire |
| `grille-reels` | Vignettes 9:16, 2 colonnes sur mobile et 3 au-delà, aperçu animé, lecteur plein écran. Comportement décrit dans `prompt_portfolio.md` |
| `film` | Façade YouTube : image, bouton lecture, titre. Charge le lecteur au clic |
| `livrables` | Liste de ce que le client reçoit |
| `citation` | `<blockquote>` avec nom et qualité. Uniquement pour une citation validée par son auteur |
| `faq` | `<details>` / `<summary>` |
| `appel` | Bloc de fin de page : une phrase, téléphone, bouton contact |
| `formulaire` | Voir §11 |

Chaque page contient : un lien d'évitement `<a class="evitement" href="#contenu">Aller au contenu</a>` en premier élément du `<body>`, un seul `<main>`, un seul `<h1>` identique au plan, des titres sans saut de niveau, des `<nav>` avec `aria-label`.

## 8. Pages et navigation

La liste des pages, leurs balises et leur lot sont dans `plan-site.json`. Les textes sont dans `CONTENU.md`.

- Menu : Mini-documentaire · Communication globale · Reels · Réalisations · À propos · bouton « Parler de votre projet » (vers `contact.html`).
- `artisans.html` et `video-immobiliere.html` ne sont pas dans le menu : on y arrive par l'accueil (porte « artisan ») et par le pied de page.
- Pied de page : lien « CV et portfolio » vers `portfolio/` (page existante sur le serveur, à ne pas toucher).
- Une étude de cas (`projets/*.html`) n'est construite que si Pierre a rempli sa fiche (voir `SUIVI.md`, F12). Sinon le projet apparaît seulement dans la grille de `projets.html`.

## 9. Vidéo

- **Aucun fichier vidéo dans `dist/`** et aucune balise `<iframe>` dans le HTML.
- Reels (Bunny Stream) : vignette locale, aperçu muet de 8 secondes chargé seulement quand la vignette est à l'écran (`https://vz-25e90935-e10.b-cdn.net/<id>/play_360p.mp4`), 2 aperçus en lecture au plus, lecteur plein écran au clic avec le son. Les identifiants sont dans `src/donnees/projets.json`.
- Vidéo d'ouverture de l'accueil : `<video preload="none" poster="…" muted playsinline loop data-src="…">`. `site.js` pose `src` et lance la lecture après l'événement `load`, sauf si `prefers-reduced-motion` ou `navigator.connection.saveData`. L'image `poster` est l'élément principal de la page : `fetchpriority="high"`, moins de 150 Ko.
- Films YouTube : façade locale (image + bouton). Au clic, `video.js` insère le lecteur `https://www.youtube-nocookie.com/embed/<id>?autoplay=1&rel=0`. Image de la façade : un photogramme fourni par Pierre de préférence, sinon `https://i.ytimg.com/vi/<id>/hqdefault.jpg`.
- Toute balise `<video>` a `preload="none"` et un `poster`, et jamais `autoplay` dans le HTML.

## 10. Images

- Pierre dépose les originaux dans `medias/originaux/`. `optimiser.py` (Pillow) produit dans `statique/assets/img/` des WebP en 480, 960 et 1600 px de large (qualité 78), nommés `<nom>-<largeur>.webp`.
- Balise type : `<img src="…-960.webp" srcset="…-480.webp 480w, …-960.webp 960w, …-1600.webp 1600w" sizes="…" alt="…" width="…" height="…" loading="lazy">`.
- Toujours `alt` (vide si l'image est décorative), `width` et `height`. `loading="lazy"` partout sauf l'image principale de la page (`fetchpriority="high"`, une seule par page).
- 300 Ko au plus par image. Image de partage `assets/img/partage.jpg`, 1200 × 630, en JPEG.
- Favicon : `favicon.svg` à la racine (un « P » dans la charte), plus `favicon.ico`.

## 11. Formulaire de contact

Le serveur a déjà `form-handler.php` (à ne pas modifier sans que Pierre fournisse le fichier, F2). Contrat observé sur le site en ligne :
- envoi en `POST`, `FormData`, vers `form-handler.php` (chemin relatif) ;
- champs : `Name`, `Email`, `T-l-phone`, `Subject`, `Message`, et `honeypot` qui doit rester vide ;
- réponse JSON `{ "success": true|false, "message": "…" }`.

Le nouveau formulaire affiche des champs en plus (profil, type de projet, budget). Ils ne sont **pas** envoyés comme champs séparés : `contact.js` construit un `FormData` avec les six champs du contrat seulement, et place les réponses en tête de `Message` :

```
[Profil : Artisan ou commerçant] [Projet : Reels] [Budget : 1 000 à 3 000 €]

(message saisi)
```

`Subject` reçoit le type de projet. Chaque champ visible a un `<label for>`. Le champ `honeypot` est masqué en CSS, avec `tabindex="-1"`, `autocomplete="off"` et `aria-hidden="true"`. Les messages de succès et d'erreur sont dans une zone `aria-live="polite"`. Sans JavaScript, la page affiche le téléphone et l'e-mail.

## 12. Référencement et serveur

- `title`, `description`, `h1` : ceux du plan, à la lettre. `canonical` sur `https://www.pibes.fr/…`. Balises `og:title`, `og:description`, `og:image`, `og:url`, `og:type` et `twitter:card` sur chaque page.
- Données structurées : `ProfessionalService` sur l'accueil (généré par `build.py`). `VideoObject` sur les études de cas quand la date de mise en ligne du film est connue.
- `.htaccess` (`src/serveur/htaccess.base`), chaque bloc dans un `<IfModule>` :
  - passage en `https` et en `www` par une redirection 301 ;
  - `ErrorDocument 404 /404.html` ;
  - `Options -Indexes` ;
  - compression (`mod_deflate`) du HTML, du CSS, du JS, du SVG et du JSON ;
  - cache (`mod_expires`) : 1 an pour `assets/` (les adresses du CSS et du JS portent `?v=`), 1 heure pour le HTML ;
  - en-têtes `X-Content-Type-Options: nosniff` et `Referrer-Policy: strict-origin-when-cross-origin`.
- Redirections : uniquement au format `Redirect 301 /ancienne.html /nouvelle.html`, générées depuis le plan.
- `404.html` est servie pour n'importe quelle adresse : c'est la seule page dont les liens partent de la racine (`/assets/css/site.css`, `/contact.html`).
- Mentions légales et politique de confidentialité : obligatoires pour un site professionnel (fiche « Mentions obligatoires sur le site internet d'une entreprise », entreprendre.service-public.gouv.fr/vosdroits/F37351). Le site actuel n'en a pas.

## 13. Performance et accessibilité : budgets

Contrôlés par `verifier.py` : HTML ≤ 100 Ko par page, CSS total ≤ 80 Ko, JS total ≤ 60 Ko, image ≤ 300 Ko, police ≤ 150 Ko, poids local au chargement ≤ 1,5 Mo pour l'accueil et 1,2 Mo ailleurs.

Contrôlés à la main au lot 8, sur le site de test :
- PageSpeed Insights mobile, accueil et une page d'offre : performance ≥ 90, accessibilité ≥ 95 ;
- LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 (seuils « bon » de Google, web.dev/articles/vitals) ;
- poids transféré de l'accueil au premier chargement ≤ 3 Mo (onglet Réseau du navigateur) ;
- contraste du texte ≥ 4,5:1, navigation complète au clavier, focus visible ;
- rendu regardé à 1440, 1024, 768, 390 et 320 px : rien ne déborde, rien ne se chevauche, cibles tactiles de 44 px.

## 14. Mise en ligne

1. **Site de test** : `python3 build.py --staging`, puis Pierre envoie le contenu de `dist/` par FTP dans `/v2/` (30 Mo libres suffisent, F9). Adresse : `https://www.pibes.fr/v2/`.
2. **Recette** (lot 8) sur `/v2/`.
3. **Bascule** : `python3 build.py`, puis Pierre envoie le contenu de `dist/` à la racine du serveur, en écrasant. Ne supprimer à ce moment-là **aucun** fichier du serveur.
4. **Contrôles après bascule** (navigateur) : chaque ancienne adresse de `plan-site.json` répond par une redirection vers la bonne page ; `/portfolio/` s'affiche toujours ; un envoi de test du formulaire arrive dans la boîte de Pierre.
5. **Ménage**, une fois les contrôles passés, par Pierre : supprimer du serveur les dossiers de l'ancien site (`css/`, `js/`, `images/`, `videos/`, `fonts/`, `services/`, `template-pages/`, `elements/`, `v2/`) et les anciennes pages (`about.html`, `services.html`, `licenses-copy.html`, `401.html`). Ne jamais toucher à `portfolio/`, à `form-handler.php` ni aux fichiers que Pierre ne reconnaît pas (il héberge aussi des pages de présentation envoyées par lien).
6. Search Console : soumettre `https://www.pibes.fr/sitemap.xml`.

## 15. Critères de réussite du projet

Mesurés par un outil ou par un tiers, jamais sur l'avis du modèle ou de Pierre :
1. `python3 verifier.py --lot 8` : `RECETTE OK`.
2. PageSpeed Insights mobile ≥ 90 en performance sur l'accueil (contre un accueil de 25 Mo aujourd'hui).
3. Test des 5 secondes sur 5 personnes extérieures : au moins 4 savent dire ce que fait Pierre et pour qui (5 testeurs : nngroup.com/articles/why-you-only-need-to-test-with-5-users).
4. Search Console, 4 semaines après la bascule : toutes les pages du sitemap indexées, aucune erreur.
5. Nombre de demandes reçues par le formulaire par mois, comparé aux 3 mois d'avant la bascule.

## 16. Prévu plus tard, hors version 1

- Grille de prix « à partir de » (emplacements réservés dans les pages d'offre).
- Avis Google et témoignages filmés.
- Études de cas supplémentaires, version anglaise, outil de statistiques.
