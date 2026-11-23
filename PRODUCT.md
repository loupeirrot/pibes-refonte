# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Site statique HTML/CSS/JS écrit à la main, assemblé par `build.py` (Python standard), hébergé chez OVH (Apache + PHP). Détail : `ARCHITECTURE.md`.

## Users

- Des dirigeants et responsables de communication d'entreprises, de marques, d'institutions et des artistes, dans les Landes et au Pays basque, qui ont un budget de communication. Ils arrivent par recommandation, par Instagram ou par un lien envoyé, souvent sur téléphone, et veulent savoir en quelques secondes si Pierre sait faire ce qu'il leur faut.
- Des artisans, commerçants et indépendants locaux qui veulent montrer leur savoir-faire avec un budget serré.

## Product Purpose

Le site de Pierre Bargelès, vidéaste à Capbreton. Il doit faire comprendre l'offre en 5 secondes, la prouver par les films et les reels, et amener à un contact qualifié (qui, quel projet, quel budget). Réussite : les critères mesurés du §15 de `ARCHITECTURE.md`.

## Positioning

Pierre filme l'histoire d'une entreprise (un mini-documentaire) et en tire toute sa communication : reels, photos, site internet, publication programmée. Une seule personne écrit, tourne, monte, étalonne et met en ligne. 20 ans d'audiovisuel, dont 18 à France Télévisions à des postes techniques de régie et de car de production.

## Operating Context

Le visiteur compare avec d'autres vidéastes locaux, qui n'affichent pas leurs prix. Il regarde d'abord les images. Le lien est souvent ouvert depuis un texto ou Instagram.

## Capabilities and Constraints

- Trois offres : mini-documentaire, communication globale, reels. Deux pages d'entrée hors menu : artisans et commerces, vidéo immobilière.
- Pas de prix affichés en version 1. Pas de drone ni de FPV dans l'offre affichée.
- Pierre ne gère pas les réseaux sociaux au quotidien ; il livre les contenus et automatise leur publication.
- Vidéos sur Bunny Stream et YouTube, jamais dans le site. Aucun script tiers.

## Brand Commitments

- Identité visuelle figée : celle de la page `/portfolio/` en ligne (fond noir chaud, texte crème, accent ambre, police Geist, frise de montage). Détail : `DESIGN.md`.
- Le site dit « je » et vouvoie. Phrases courtes, mots concrets. Textes : `CONTENU.md`.

## Evidence on Hand

- Films : Optima by Delwood (YouTube `2J7MZ--tcww`), Laboratoire Ziwig (YouTube `B3PK27fVF2A`).
- Six reels sur Bunny Stream : `src/donnees/projets.json`.
- Absent à ce jour, à ne jamais inventer : témoignages validés, chiffres de résultat, prix, délais, photos de Pierre en tournage. Liste de ce que Pierre doit fournir : `SUIVI.md`.

## Product Principles

1. L'image d'abord : chaque écran montre un film ou un reel de Pierre.
2. Un fait vérifiable vaut mieux qu'un adjectif.
3. Dire aussi ce que Pierre ne fait pas.
4. Rien d'inventé : un bloc sans matière n'existe pas.

## Accessibility & Inclusion

Contraste du texte ≥ 4,5:1, navigation complète au clavier, focus visible, respect de `prefers-reduced-motion`, cibles tactiles de 44 px.
