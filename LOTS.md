# Refonte pibes.fr : découpage en lots

Un lot = une session = un modèle. Chaque lot se termine par la recette `python3 verifier.py --lot N` et par la mise à jour de `SUIVI.md`.

## Message à envoyer pour lancer un lot

Copier ce message dans une nouvelle conversation du projet Pibes, avec le dossier `Pibes` connecté, en remplaçant `N` :

> Tu exécutes le lot N de la refonte de pibes.fr. Travaille directement dans le dossier `Site pibes.fr/refonte/` de mon ordinateur.
> 1. Lis en entier `ARCHITECTURE.md`, puis `SUIVI.md`, puis la section « Lot N » de `LOTS.md`, puis dans `CONTENU.md` les pages de ce lot. Si le lot touche à l'interface (lots 1 à 5 et 8), lis aussi `DESIGN.md` en entier et `skills/impeccable/reference/craft-floor.md`. Si les skills `impeccable` et `taste` sont disponibles dans ton environnement, charge-les aussi ; en cas de désaccord, `DESIGN.md` l'emporte.
> 2. Fais uniquement ce lot. Respecte les règles du §0 de `ARCHITECTURE.md`. N'invente aucun contenu : si une matière manque, laisse le bloc hors de la page et note-le.
> 3. Lance `python3 build.py` puis `python3 verifier.py --lot N` et corrige jusqu'à `RECETTE OK`. Ne modifie ni `verifier.py` ni `plan-site.json`. Les pages restées sans matière dans les lots précédents (voir `SUIVI.md`) se déclarent avec `--en-attente`.
> 4. Mets à jour `SUIVI.md` (état du lot, journal, questions pour moi).
> 5. Termine par un résumé de 5 lignes : ce qui est fait, ce qui manque, le résultat de la recette.

## Quel modèle pour quel lot

| Lot | Contenu | Modèle conseillé |
|---|---|---|
| 0 | Matière à fournir | Pierre, sans modèle |
| 1 | Socle technique | Sonnet 5.5 |
| 2 | Accueil | Sonnet 5.5 |
| 3 | Pages d'offre | Sonnet 5.5 |
| 4 | Réalisations et vidéo | Sonnet 5.5 |
| 5 | À propos, contact, pages légales | Sonnet 5.5 |
| 6 | Images | Haiku 5.5 |
| 7 | Serveur et référencement | Haiku 5.5 |
| 8 | Recette et mise en ligne | Sonnet 5.5 |

Enchaîner deux lots dans la même conversation est possible (par exemple 1 et 2) : utiliser alors le modèle conseillé le plus fort des deux, et exiger `RECETTE OK` et `SUIVI.md` à jour entre les deux.

Règle de repli : si un lot échoue deux fois à la recette avec le modèle conseillé, le relancer une fois avec le modèle au-dessus (Haiku → Sonnet → Opus ou Fable), pas plus. Si le rendu visuel de l'accueil ne convient pas, refaire seulement le lot 2 avec un modèle plus fort : le reste du site reprend ses composants.

Ordre : 1, 2, 3, 4, 5, 6, 7, 8. Le lot 6 peut passer avant le lot 2 si Pierre a déjà déposé ses images.

---

## Lot 0 : matière à fournir (Pierre)

Liste et cases à cocher dans `SUIVI.md`. Rien n'est bloquant pour démarrer le lot 1. F3, F4 et F5 améliorent beaucoup le lot 2 ; F12 conditionne les études de cas du lot 4 ; F7 conditionne les pages légales du lot 5 ; F9 conditionne le lot 8.

## Lot 1 : socle technique

**But** : un squelette qui se construit et passe la recette, sur lequel les lots suivants n'ont plus qu'à poser des pages.

**À produire**
- `build.py` selon le contrat du §5 de `ARCHITECTURE.md`, y compris `--staging`, `MANIFESTE.txt`, `sitemap.xml`, `robots.txt`, `.htaccess`.
- `src/partiels/tete.html`, `entete.html`, `pied.html` (textes : `CONTENU.md`, « Éléments communs »).
- `src/css/10-jetons.css` (§6), `20-base.css` (remise à zéro, typographie, grille, boutons, liens, focus visible, lien d'évitement), `30-composants.css` (entête, pied, ouverture avec son entrée au chargement, appel, barre mobile), `40-pages.css` (vide).
- `src/js/site.js` : menu mobile, barre d'action mobile, tête de lecture de la frise, respect de `prefers-reduced-motion`. Aucune apparition au défilement : le contenu est visible sans JavaScript.
- Les surfaces du navigateur de `DESIGN.md` (sélection, focus, curseur de saisie, barre de défilement) dans `20-base.css`.
- `src/serveur/htaccess.base` (§12).
- Polices Geist et Geist Mono en `woff2` dans `statique/assets/fonts/` (§6), `favicon.svg`.
- `src/pages/404.html`.

**Recette** : `python3 verifier.py --lot 1` → `RECETTE OK`. De plus, `dist/404.html` ouvert dans un navigateur affiche l'en-tête, le pied de page et la charte. Regarder le rendu à 1440, 1024, 768, 390 et 320 px (captures à 390 et 1440 px à joindre au résumé).

## Lot 2 : accueil

**But** : la page qui doit passer le test des 5 secondes.

**À produire** : `src/pages/index.html` avec toutes les sections de `CONTENU.md`, et les composants `portes`, `liste-offres`, `frise`, `film`, `grille-reels`, `citation` dans `30-composants.css` (apparence : `DESIGN.md`) ; `src/js/video.js` (façade YouTube, grille de reels, lecteur plein écran, vidéo d'ouverture). Comportement de la grille : `../../Claude outputs/prompt_portfolio.md`, et `reference/portfolio/index.html` s'il est présent (F1).

**Points d'attention**
- Ordre de lecture sur mobile : `h1`, chapeau, boutons, puis le média.
- L'image principale de l'ouverture porte `fetchpriority="high"`. Tout le reste est en `loading="lazy"`.
- Blocs F3 et F4 absents tant que la matière n'est pas cochée dans `SUIVI.md` : la page doit rester équilibrée sans eux.
- Vignettes des reels : en attendant le lot 6, utiliser celles de `../../Claude outputs/miniatures_portfolio.zip` (les extraire dans `/tmp`, les copier dans `statique/assets/img/`).

**Fiches à lire en plus** : `skills/impeccable/reference/typeset.md`, `layout.md` et `animate.md`.

**Recette** : `python3 verifier.py --lot 2` → `RECETTE OK`. Rendu regardé à 1440, 1024, 768, 390 et 320 px ; captures à 390 et 1440 px. Dans le résumé, répondre par une preuve (sélecteur ou valeur) à trois questions : quel est le seul élément ambre de chaque écran ? où est le fait qui situe Pierre dans le premier écran ? qu'est-ce qui bouge au chargement, et rien d'autre ?

## Lot 3 : pages d'offre

**À produire** : `mini-documentaire.html`, `communication-globale.html`, `reels.html`, `artisans.html`, `video-immobiliere.html`, sur un même gabarit `offre` ; composants `livrables` et `faq`. Emplacement prix présent sous forme de commentaire HTML, vide.

**Recette** : `python3 verifier.py --lot 3` → `RECETTE OK`.

## Lot 4 : réalisations et vidéo

**À produire** : `projets.html` (films puis reels, depuis `src/donnees/projets.json`, lu par `build.py` au moment de la construction, pas par le navigateur) ; gabarit `etude` ; une page par étude de cas **dont la fiche F12 est remplie**.

Une étude sans fiche n'est pas construite, et aucun lien ne pointe vers elle. La déclarer à la recette avec `--en-attente`, et la noter dans `SUIVI.md`.

**Recette** : `python3 verifier.py --lot 4` → `RECETTE OK`. Avec des études en attente, par exemple : `python3 verifier.py --lot 4 --en-attente projets/ziwig.html projets/tasta-wood-solution.html`.

## Lot 5 : à propos, contact, pages légales

**À produire** : `a-propos.html`, `contact.html` avec `src/js/contact.js` (contrat : §11), `mentions-legales.html` et `confidentialite.html` (seulement si F7 est coché ; sinon les déclarer avec `--en-attente` et noter le blocage : elles sont obligatoires avant la mise en ligne, la recette du lot 8 les exige).

**Points d'attention** : tester l'envoi du formulaire est impossible hors du serveur. Vérifier à la place, dans le navigateur, que le `FormData` construit contient exactement les six champs du contrat et que `Message` commence par la ligne `[Profil : …] [Projet : …] [Budget : …]`.

**Recette** : `python3 verifier.py --lot 5` → `RECETTE OK`.

## Lot 6 : images

**À produire** : `optimiser.py` (§10) ; toutes les images de `medias/originaux/` converties ; balises `<img>` des pages mises à jour avec `srcset`, `sizes`, `width`, `height` ; `assets/img/partage.jpg` (1200 × 630) ; `favicon.ico`.

**Recette** : `python3 verifier.py --lot 6` → `RECETTE OK`, et aucune image de plus de 300 Ko.

## Lot 7 : serveur et référencement

**À produire** : contrôle complet de `.htaccess`, `sitemap.xml`, `robots.txt` générés ; balises `og:` et `twitter:card` sur toutes les pages ; `VideoObject` sur les études de cas quand la date du film est connue ; relecture de tous les `alt`.

**Recette** : `python3 verifier.py --lot 7` → `RECETTE OK`.

## Lot 8 : recette et mise en ligne

1. `python3 build.py --staging` puis `python3 verifier.py --lot 8 --staging` → `RECETTE OK`.
2. Pierre envoie `dist/` dans `/v2/` par FTP (F9).
3. Avec le navigateur, sur `https://www.pibes.fr/v2/` : parcourir toutes les pages à 1440, 1024, 768, 390 et 320 px, en suivant `skills/impeccable/reference/polish.md` et `audit.md` ; relire les textes contre `skills/taste-skill/references/copy-tells.md` ; tester le menu, la grille de reels, le lecteur, la façade YouTube, le formulaire (un envoi réel, avec l'accord de Pierre) ; mesurer le poids transféré de l'accueil.
4. Pierre lance PageSpeed Insights (pagespeed.web.dev) sur l'accueil et une page d'offre de `/v2/`, en mobile, et note les scores dans `SUIVI.md`. Cibles : §13.
5. Corriger, reconstruire, recommencer jusqu'aux cibles.
6. `python3 build.py` puis `python3 verifier.py --lot 8` → `RECETTE OK`. Pierre fait la bascule et les contrôles du §14.

**Critère de fin** : les 5 critères du §15 sont notés dans `SUIVI.md`, avec leur mesure.
