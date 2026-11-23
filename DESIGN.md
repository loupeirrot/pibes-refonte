---
name: pibes.fr
colors:
  fond: "#12110f"
  fond-2: "#181614"
  noir: "#0a0908"
  encre: "#efebe4"
  encre-2: "rgba(239, 235, 228, .78)"
  doux: "#a29d94"
  trait: "rgba(239, 235, 228, .11)"
  trait-2: "rgba(239, 235, 228, .22)"
  accent: "#f2a900"
  accent-vif: "#ffb91c"
  encre-accent: "#161107"
typography:
  display:
    fontFamily: "Geist"
    fontSize: "clamp(2.2rem, 11.4vw, 6rem)"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Geist"
    fontSize: "clamp(2.4rem, 5.4vw, 4rem)"
    fontWeight: 500
    lineHeight: 1.04
    letterSpacing: "-0.04em"
  title:
    fontFamily: "Geist"
    fontSize: "clamp(1.9rem, 3.2vw, 2.65rem)"
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  subtitle:
    fontFamily: "Geist"
    fontSize: "1.4rem"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Geist"
    fontSize: "1.03rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Geist"
    fontSize: "0.94rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Geist Mono"
    fontSize: "0.72rem"
    fontWeight: 400
    letterSpacing: "0.08em"
rounded:
  cadre: "4px"
  pilule: "999px"
spacing:
  "1": "4px"
  "2": "8px"
  "3": "12px"
  "4": "16px"
  "6": "24px"
  "8": "32px"
  "10": "40px"
  "12": "48px"
  "16": "64px"
  "24": "96px"
  marge: "clamp(20px, 4vw, 48px)"
  section: "clamp(72px, 9vw, 120px)"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.encre-accent}"
    rounded: "{rounded.pilule}"
    height: "46px"
    padding: "0 22px"
  button-primary-hover:
    backgroundColor: "{colors.accent-vif}"
  button-outline:
    textColor: "{colors.encre}"
    rounded: "{rounded.pilule}"
    height: "46px"
    padding: "0 22px"
  cadre-media:
    backgroundColor: "{colors.fond-2}"
    rounded: "{rounded.cadre}"
---

# Design System: pibes.fr

Source de vérité du design. Les valeurs viennent du CSS de la page `/portfolio/` en ligne, relevé le 16/11/2026 : c'est l'identité choisie par Pierre, elle est **figée**. Ce document la reprend à l'identique, puis la resserre avec les règles des skills Impeccable (`skills/impeccable/`) et Taste (`skills/taste-skill/`). Là où un skill contredit l'identité d'origine, l'identité gagne : la liste de ces écarts est à la fin.

## Overview

**Idée directrice : la table de montage.** Une salle sombre, l'image au centre, et une tête de lecture ambre qui indique où l'on en est. Pierre est monteur : la frise de montage et sa tête de lecture (déjà présentes dans le « Parcours » de la page portfolio) sont le motif du site.

- Le site est en mode *Persuade* au sens d'Impeccable : le visiteur doit comprendre l'offre, la désirer et agir. Les pages de réalisations sont en mode *Experience* : le film passe devant l'interface.
- Les films et les reels portent chaque écran. Le texte est court, posé sur un fond uni.
- **L'ambre ne décore jamais.** Il désigne ce qui se joue ou ce qu'il faut faire : le bouton principal, la tête de lecture, la barre de progression d'un reel, le focus clavier, la sélection de texte, un seul mot dans le titre de fin de page. Un seul élément ambre par écran, focus mis à part.
- Sombre partout, sans section claire. C'est la lumière dans laquelle on regarde un film.

## Colors

### Primary
- **Ambre tête de lecture** (`--accent` #f2a900) : bouton principal, tête de lecture, progression, focus, sélection. Au survol du bouton : `--accent-vif` #ffb91c. Texte posé dessus : `--encre-accent` #161107.

### Neutral
- **Noir chaud** (`--fond` #12110f) : fond de toutes les pages.
- **Noir chaud relevé** (`--fond-2` #181614) : bandes de section (méthode, parcours), fond d'un cadre avant le chargement de l'image.
- **Noir de salle** (`--noir` #0a0908) : lecteur plein écran, cadre des films.
- **Crème** (`--encre` #efebe4) : titres et texte principal.
- **Crème atténué** (`--encre-2`, 78 %) : texte courant secondaire, navigation.
- **Gris chaud** (`--doux` #a29d94) : deuxième ligne des grands titres, légendes, libellés mono.
- **Traits** (`--trait` 11 %, `--trait-2` 22 %) : filets de 1 px, contours de boutons et de pastilles.

### Named Rules
- **Aucune couleur écrite en dur** hors de `10-jetons.css`. Ni `#000` ni `#fff`.
- **Pas de gris neutre** : tout texte secondaire sort de la famille crème.
- Contraste : texte courant ≥ 4,5:1, grands titres ≥ 3:1. Mesuré : `--doux` sur `--fond` 7,0:1, `--encre-2` sur `--fond` 9,9:1, `--encre-accent` sur `--accent` 9,4:1. Les traits (`--trait-2` : 1,9:1) ne portent jamais une information à eux seuls.

Bloc à copier tel quel dans `10-jetons.css` :

```css
:root {
  color-scheme: dark;
  --fond: #12110f; --fond-2: #181614; --noir: #0a0908;
  --encre: #efebe4; --encre-2: rgba(239, 235, 228, .78); --doux: #a29d94;
  --trait: rgba(239, 235, 228, .11); --trait-2: rgba(239, 235, 228, .22);
  --accent: #f2a900; --accent-vif: #ffb91c; --encre-accent: #161107;
  --police: "Geist", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "Geist Mono", ui-monospace, Menlo, monospace;
  --largeur: 1240px; --marge: clamp(20px, 4vw, 48px);
  --section: clamp(72px, 9vw, 120px); --rayon: 4px;
  --glisse: cubic-bezier(.2, .7, .2, 1);
}
```

## Typography

Une seule famille, Geist. Geist Mono n'est pas un style : il sert aux **données** seulement.

### Hierarchy
- **Display** (500, `clamp(2.2rem, 11.4vw, 6rem)`, interligne 1, approche -0,04em) : le `h1` de l'accueil et des pages d'offre. Sur deux lignes : la première en crème, la seconde en graisse 300 et en `--doux` (`<h1>Ligne 1 <span>ligne 2</span></h1>`, `span { display: block }`). C'est la signature typographique de la page portfolio.
- **Headline** (500, `clamp(2.4rem, 5.4vw, 4rem)`, 1,04, -0,04em) : le titre du bloc de fin de page, avec un seul mot en ambre ; la phrase de la section « Ce que je ne fais pas » (sans ambre).
- **Title** (500, `clamp(1.9rem, 3.2vw, 2.65rem)`, 1,1, -0,03em) : les `h2`.
- **Subtitle** (500, 1,4rem, 1,15, -0,02em) : les `h3` (offres, étapes, entrées de frise).
- **Body** (400, 1,03rem, 1,6) : texte courant, 65 caractères par ligne au plus ; le chapeau sous un `h1` est limité à 46ch, en `--encre-2`.
- **Small** (0,94rem) : navigation, boutons (graisse 500), texte secondaire. Légendes à 0,875rem, pied de page à 0,84rem.
- **Label** (Geist Mono, 0,72rem, +0,08em, capitales, `--doux`, `font-variant-numeric: tabular-nums`) : dates, années, durées, formats (16:9, 9:16), numéros d'étape. Rien d'autre.

### Named Rules
- **Pas de surtitre.** Aucun libellé au-dessus d'un `h1` ou d'un `h2` (interdit par Impeccable, et absent de la page portfolio). Le titre se suffit.
- `text-wrap: balance` sur les titres, `text-wrap: pretty` sur les paragraphes.
- Plafonds : aucun corps au-dessus de 6rem, aucune approche sous -0,04em.
- Polices hébergées sur le site, `woff2`, `font-display: swap`, police de texte préchargée.

## Layout

- **Cadre** : `max-width: var(--largeur)`, `padding-inline: var(--marge)`. Tous les blocs s'alignent sur ses deux bords : mêmes marges à gauche et à droite, rien qui dépasse d'un seul côté.
- **Échelle d'espacement** sur une base de 4 px (voir les jetons). Serré à l'intérieur d'un groupe (8 à 16 px), large entre les groupes (40 à 64 px), `--section` entre les sections. Plus d'espace au-dessus d'un titre qu'en dessous : `h2` suivi de `clamp(24px, 3vw, 36px)`.
- **Grilles asymétriques** reprises de la page portfolio : `7fr / 5fr` (film principal et film secondaire, offre principale et son image), `4fr / 7fr` (titre à gauche, frise à droite), ouverture en `1fr / auto` (chapeau à gauche, boutons à droite, alignés en bas) à partir de 960 px.
- **Une idée par section**, une à deux hauteurs d'écran à 1440 × 900. L'ouverture tient seule dans le premier écran avec son bouton principal ; le média qui suit peut être coupé net par le bas de l'écran, jamais un titre de la section suivante.
- **Bandes** : une section sur `--fond-2` bordée de filets `--trait` en haut et en bas sert à rompre le rythme (méthode, parcours). Deux par page au plus.
- **Largeurs de contrôle** : 1440, 1024, 768, 390 et 320 px. À 390 px : une colonne, boutons en pleine largeur par paires, menu plein écran. À 320 px : rien ne déborde, rien ne se chevauche.
- **Cibles tactiles** de 44 px de haut au moins.
- Points de rupture d'origine : 640, 768, 960 px.

## Elevation & Depth

Le site est plat. La profondeur vient de trois tons (`--fond`, `--fond-2`, `--noir`) et de filets de 1 px. **Aucune ombre portée**, aucun flou décoratif, aucun effet de verre.

## Shapes

- Cadres d'image et de vidéo : rayon de 4 px (`--rayon`), `overflow: hidden`.
- Boutons, pastilles, lien d'évitement : pilule (999 px).
- Icônes de lecture, boutons du lecteur : cercle.
- Filets de 1 px. Aucune bordure colorée épaisse sur un côté.

## Components

### Buttons
- **Forme** : pilule, 46 px de haut (44 px dans la barre mobile), `padding: 0 22px`, 0,94rem, graisse 500.
- **Principal** (`.btn-accent`) : fond `--accent`, texte `--encre-accent`. Survol : `--accent-vif`.
- **Secondaire** (`.btn-trait`) : contour 1 px `--trait-2`. Survol : contour `--encre`.
- **Appui** : `translateY(1px)`. Transitions de 0,2 s.
- Une seule paire de boutons sur tout le site. Deux actions au plus dans une ouverture.

### Liens
- Dans le texte et les listes : soulignement qui se trace de gauche à droite au survol (`background-size` de 0 à 100 % sur 1 px, 0,35 s, `--glisse`). Jamais de flèche après le texte d'un lien.

### Navigation
- En-tête de 64 px, filet `--trait` en dessous. Marque à gauche (logo de 18 px de haut et « Pierre Bargelès »), liens à droite en 0,94rem `--encre-2`, bouton principal au bout.
- Sous 768 px : bouton de menu (`aria-expanded`), menu en plein écran.
- **Barre d'action mobile** (sous 960 px) : fixée en bas, deux boutons « Appeler » et « Écrire », apparaît après l'ouverture de la page, tient compte de `env(safe-area-inset-bottom)`.

### Ouverture de page
- `h1` Display sur deux lignes, puis, sur une même rangée à partir de 960 px, le chapeau (46ch) à gauche et les boutons à droite. Le média vient dessous, sur toute la largeur du cadre.
- Accueil : le chapeau contient le fait qui situe Pierre (métier, lieu, 20 ans d'audiovisuel dont 18 à France Télévisions). Pas de rangée de chiffres.

### Cadre de film (`.film`)
- 16:9, rayon 4 px, fond `--noir`. Image à `brightness(.9)`, bouton de lecture crème de 64 px au centre. Survol : `brightness(1)`, `scale(1.015)` sur l'image, `scale(1.06)` sur le bouton. Légende dessous : titre en `--encre` graisse 500, suite en `--doux`.

### Grille de reels (`.grille-reels`)
- 2 colonnes sous 768 px (écart 24 px / 10 px, les vignettes paires décalées de 28 px vers le bas), 3 colonnes au-delà (écart 40 px / 10 px, la colonne du milieu décalée de 64 px).
- Vignette 9:16, rayon 4 px. Bouton de lecture crème de 34 px en bas à gauche. Zoom lent de l'image (`scale(1.05)` en 9 s) quand elle est à l'écran. Aperçu vidéo en fondu de 0,6 s. Barre de progression ambre de 2 px en bas pendant l'aperçu.
- Légende sous la vignette : « **Titre.** Sous-titre. » en 0,875rem.
- Lecteur plein écran : `<dialog>` sur `--noir`, commandes rondes de 48 px.

### Liste d'offres (remplace les « cartes »)
- Les trois offres ne sont **pas** trois cartes égales. Ce sont trois rangées séparées par des filets `--trait`, sur toute la largeur du cadre.
- La première (mini-documentaire) est la plus grande : image du film à gauche (`7fr`), titre, deux lignes et lien à droite (`5fr`). Les deux suivantes : titre `h3` à gauche, deux lignes au centre, lien à droite, sans image.
- Survol d'une rangée : le soulignement du lien se trace ; rien d'autre ne bouge.

### Deux publics (« portes »)
- Deux colonnes séparées par un filet vertical `--trait` (empilées avec un filet horizontal sous 768 px). Pas de boîte, pas de fond, pas d'icône. `h3`, un paragraphe, un lien.

### Frise et tête de lecture (motif du site)
- Reprise du « Parcours » de la page portfolio : chaque étape est un « clip » avec, à gauche, un trait vertical de 2 px `--encre` ; une tête de lecture ambre (filet de 1 px et son libellé mono) descend le long de la frise avec le défilement.
- Utilisée pour **la méthode en quatre étapes** (libellés 01 à 04 : la suite est réelle) et pour le parcours de la page « À propos » (libellé : l'année).
- Posée dans une bande `--fond-2`, en grille `4fr / 7fr` à partir de 960 px.
- C'est le seul mouvement lié au défilement du site.

### Formulaire
- Champs : fond transparent, filet du bas 1 px `--doux` (7,0:1, pour que le champ se voie), texte `--encre`, libellé visible au-dessus en 0,94rem `--encre-2`. Focus : filet `--accent`, plus l'anneau de focus. Erreur : message sous le champ concerné, en toutes lettres.
- Boutons radio et listes : `accent-color: var(--accent)`.

### Surfaces du navigateur
- `::selection` : fond `--accent`, texte `--encre-accent`.
- `:focus-visible` : `outline: 2px solid var(--accent)`, `outline-offset: 3px`.
- `caret-color: var(--accent)`, `scrollbar-color: var(--trait-2) var(--fond)`, `text-underline-offset: .2em`.

### Mouvement
- **Courbe** : `--glisse` pour tout. Pas de rebond ni d'élastique.
- **Durées** : 0,2 s (survol, appui), 0,35 s (soulignement, menus, barre mobile), 0,6 s (fondu d'aperçu), 0,8 s (entrée de l'ouverture).
- **Une entrée par page** : au chargement, le `h1`, le chapeau et les boutons montent de 14 px en fondu, décalés de 0,1 s et 0,16 s. Rien d'autre n'entre en scène.
- **Aucune apparition au défilement.** Le contenu est visible par défaut, sans JavaScript. (La page portfolio en a une, `.revele` : ne pas la reprendre.)
- Animer seulement `transform`, `opacity`, `filter`, `background-size`, les couleurs. Jamais `width`, `height`, `top`, `left`, ni `transition: all`.
- `prefers-reduced-motion: reduce` : plus de déplacement ni de zoom, tête de lecture masquée ; les fondus et les changements de couleur restent.

## Do's and Don'ts

### Do:
- **Do** mettre un film ou un reel dans chaque écran de l'accueil.
- **Do** composer le `h1` sur deux lignes, la seconde en graisse 300 et en `--doux`.
- **Do** garder les légendes des reels et le décalage des colonnes : ils font partie de l'identité d'origine.
- **Do** réserver l'ambre à ce qui se joue ou à l'action principale, une fois par écran.
- **Do** regarder le rendu à 1440, 1024, 768, 390 et 320 px avant de dire qu'un lot est fini, et corriger en une passe ce que ce regard montre.
- **Do** lire `skills/impeccable/reference/craft-floor.md` juste avant de toucher à l'interface.

### Don't:
- **Don't** poser un surtitre au-dessus d'un titre.
- **Don't** aligner des chiffres avec un petit libellé dessous (« 20 ans », « 18 ans »…) : le fait va dans la phrase qu'il prouve.
- **Don't** construire une section avec des cartes égales « icône, titre, texte », ni emboîter des cartes.
- **Don't** utiliser de texte en dégradé, d'effet de verre, d'ombre portée, de bordure colorée épaisse sur un côté.
- **Don't** faire apparaître les sections en fondu au défilement, ni de parallaxe sur le texte, ni de carrousel, ni d'inclinaison au survol.
- **Don't** utiliser Geist Mono pour « faire technique » : données seulement.
- **Don't** mettre d'emoji, de flèche après un lien, de violet.
- **Don't** écrire une couleur en dur dans une feuille autre que `10-jetons.css`.

## Écarts assumés avec les skills

L'identité d'origine et la réalité d'un site client passent avant ces règles des skills :

| Règle du skill | Ce que fait le site | Raison |
|---|---|---|
| Taste : pages sombres réservées aux sites « tech » | Sombre partout | Identité d'origine |
| Taste : aucune légende sous une image | Légende sous chaque reel et chaque film | Identité d'origine ; elle nomme le client |
| Taste : rien de décalé | Colonnes de reels décalées | Identité d'origine |
| Taste : coordonnées factices, pas de numéro de téléphone réel ni de SIRET | Coordonnées réelles | Site en production, mentions légales obligatoires |
| Taste : palette, police et ouverture tirées au sort par ses scripts | Palette, police et ouverture fixées ici | Identité d'origine |
| Taste : gabarit et feuille de style du skill (`starter.html`, `system.css`) | CSS propre au site | Budget de 80 Ko de CSS, identité d'origine |
| Impeccable : corps maximal 6rem, approche minimale -0,04em | Appliqué (la page portfolio monte à 6,5rem et -0,045em) | Écart invisible à l'œil, règle retenue |
| Impeccable et Taste : pas d'apparition au défilement | Appliqué (la page portfolio en a une) | Contenu visible sans JavaScript |
