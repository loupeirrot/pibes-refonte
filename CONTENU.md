# Refonte pibes.fr : textes des pages

> 20/11/2026 : textes de l'accueil, de la communication globale, de la frise, du bloc de fin, des études de cas, des pages légales et des pages tatouage, santé et liens revus avec Pierre. Pour ces pages, la version de référence est désormais `src/pages/`.

Textes à reprendre tels quels. Le `title`, la `description` et le `h1` de chaque page sont dans `plan-site.json` et font foi.

## Règles d'écriture

- « Je » pour Pierre, « vous » pour le visiteur. Jamais « nous ».
- Phrases courtes, mots concrets. Pas de : percutant, sublimer, booster, sur mesure, clé en main, passionné, innovant, « n'hésitez pas ». Pas de tiret cadratin.
- Aucun prix, aucun chiffre de résultat, aucun délai qui ne soit pas écrit ici.
- Pas de surtitre au-dessus d'un titre. Pas de rangée de chiffres : un fait va dans la phrase qu'il prouve. Pas de tournure « pas X, mais Y » : dire le fait. Pas de point d'exclamation, pas de flèche après le texte d'un lien (les « → » de ce document indiquent seulement la page de destination).
- Les `h1` se composent sur deux lignes quand le plan le permet : la coupe est indiquée par « / ». Le texte reste celui du plan, à la lettre.
- `[À FOURNIR Fx : …]` et `[À CONFIRMER Fx : …]` : tant que l'élément n'est pas coché dans `SUIVI.md`, **le bloc entier est laissé hors de la page**. Ne jamais le remplir par supposition.
- Typographie française : espace insécable avant `: ; ? !` et dans « » ; apostrophe courbe ’ dans le HTML.
- Les titres de section ci-dessous (`###`) deviennent des `<h2>` dans la page, sauf mention contraire.

## Éléments communs

### En-tête
Logo texte : **Pierre Bargelès**
Menu : Mini-documentaire · Communication globale · Reels · Réalisations · À propos
Bouton : **Parler de votre projet** → `contact.html`

### Pied de page
- Colonne 1 : Pierre Bargelès · Vidéaste · Capbreton (40) · 06 70 71 84 05 · adresse e-mail (champ `site.email` du plan)
- Colonne 2, « Offres » : Mini-documentaire · Communication globale · Reels · Artisans et commerces · Vidéo immobilière
- Colonne 3, « Le site » : Réalisations · À propos · CV et portfolio (`portfolio/`) · Contact
- Colonne 4, « Réseaux » : Instagram `https://www.instagram.com/pierre.bargeles/` · LinkedIn `https://www.linkedin.com/in/pierre-bargeles/` · Facebook `https://www.facebook.com/profile.php?id=61572107414089`
- Dernière ligne : © {{annee}} Pierre Bargelès · Mentions légales · Confidentialité

### Bloc de fin de page (`appel`), sur toutes les pages sauf contact et pages légales
Titre (style Headline, le mot « projet » en ambre) : **Un projet en tête ?**
Texte : Dites-moi en deux phrases ce que vous voulez montrer. Je vous réponds avec une idée de film et de ce qu'on peut en tirer.
Boutons : **Appeler le 06 70 71 84 05** · **Écrire** → `contact.html`

---

## 404.html

Texte : La page que vous cherchez n'existe pas, ou elle a changé d'adresse.
Liens : Retour à l'accueil · Voir les réalisations · Me contacter

---

## index.html

### Ouverture (pas de `h2` : c'est le bloc du `h1`)
`h1` : voir plan. Coupe : Je filme votre histoire, / et j'en tire toute votre communication.
Chapeau : Vidéaste à Capbreton, dans les Landes. 20 ans d'audiovisuel, dont 18 à France Télévisions. Je réalise un mini-documentaire sur votre entreprise, puis je le décline en reels, en photos et en site internet.
Boutons : **Parler de votre projet** → `contact.html` · **Voir les réalisations** → `projets.html`
Média : `[À FOURNIR F4 : vidéo d'ouverture sur Bunny et son photogramme]`. En attendant F4, image fixe : `optima-atelier.jpg` (accord donné, voir `SUIVI.md`, F5).

### Pour qui je travaille
Deux colonnes séparées par un filet, sans boîte (composant « portes » de `DESIGN.md`).

Colonne 1. **Une entreprise, une marque, une institution**
Vous avez un budget de communication et vous voulez des supports qui durent : un film qui raconte votre métier, et tout ce qu'on peut en tirer.
Lien : Voir le mini-documentaire → `mini-documentaire.html`

Colonne 2. **Un artisan, un commerçant, un indépendant**
Vous voulez montrer votre savoir-faire sans y passer vos soirées : un reel, de belles photos, une présentation claire.
Lien : Voir ce que je propose → `artisans.html`

### Les trois offres (ancre `id="offres"`)
Trois rangées séparées par des filets (composant « liste d'offres » de `DESIGN.md`), la première plus grande, avec l'image du film.

Rangée **Le mini-documentaire**
Un film de 3 à 15 minutes sur votre entreprise, votre métier ou votre œuvre. La pièce centrale, dont tout le reste découle.
→ `mini-documentaire.html`

Rangée **La communication globale**
Le film, les reels, une banque de photos, un site internet et la publication programmée. De quoi communiquer pendant un an.
→ `communication-globale.html`

Rangée **Les reels**
Des formats courts tournés chez vous et montés comme des films, à l'unité ou par journée de tournage.
→ `reels.html`

### Un film, et tout ce qui en découle
Titre du film : Optima by Delwood. Quand un hélicoptère devient une œuvre d'art.
Média : façade YouTube, identifiant `2J7MZ--tcww`.
Texte : `[À CONFIRMER F3 : deux phrases de contexte sur le projet, validées par Pierre et Delwood]`
Liste « Tiré du même tournage » : le film · le reel « Posca by Delwood » · `[À CONFIRMER F3 : autres supports livrés]`
Citation : `[À FOURNIR F3 : citation de Delwood validée par lui]`
Lien : Lire l'étude de cas → `projets/optima-delwood.html` (seulement si la page existe)

### La méthode, en quatre étapes
Frise avec tête de lecture (composant de `DESIGN.md`), libellés 01 à 04.

1. **L'immersion.** Je viens voir comment vous travaillez. On décide ensemble de ce que le film doit raconter, et à qui.
2. **Le tournage.** Une à trois journées chez vous. Image, son, lumière : je m'occupe de tout, vous faites votre métier.
3. **Le montage et les déclinaisons.** Le film d'abord. Puis les reels, les photos et les formats pour votre site.
4. **La diffusion.** Je vous remets un calendrier de publication, ou je programme tout pour que vos contenus partent sans vous.

### Reels
Chapeau : Tournés sur place, montés et étalonnés avec le même soin qu'un film.
Grille : les 6 reels de `src/donnees/projets.json`.
Lien : Tous les reels → `reels.html`

### Ce que je ne fais pas
Composée en grand (style Headline de `DESIGN.md`), sans ambre :
Je ne gère pas vos réseaux sociaux au quotidien. Je vous donne de quoi publier pendant des mois, et je peux automatiser l'envoi.

### Bloc de fin de page

---

## mini-documentaire.html

### Ouverture
`h1` : voir plan. Coupe : Le mini-documentaire : / un film qui raconte vraiment votre métier
Chapeau : Un film de 3 à 15 minutes, tourné chez vous, qui montre ce que vous faites et pourquoi vous le faites. Il sert ensuite de réserve : on en tire des reels, des photos et les vidéos de votre site.
Bouton : **Parler de votre projet**

### Pour qui
Pour les entreprises, les marques, les artistes, les associations et les institutions qui ont quelque chose à montrer : un savoir-faire, un lancement, un anniversaire, un projet qui sort de l'ordinaire.

### Ce que vous recevez
- Le film, au format 16:9, prêt pour YouTube, votre site et vos présentations
- Une bande-annonce courte
- Des reels verticaux tirés du même tournage
- Une série de photos
- Les fichiers adaptés à chaque plateforme

Phrase sous la liste : Le nombre de reels et de photos est fixé dans le devis.

### Trois formats
`[À CONFIRMER F13 : composition des trois formats (Essentiel, Signature, Grand format), sans prix]`

### La méthode, en quatre étapes
Reprendre la frise de l'accueil.

### Exemple
Cadre du film Optima by Delwood (façade YouTube `2J7MZ--tcww`) et lien vers l'étude de cas si elle existe.

### Budget
Chaque film fait l'objet d'un devis détaillé, ligne par ligne. Donnez-moi votre budget, même approximatif : je vous dis ce qu'il permet de faire, et ce qu'il ne permet pas.
Emplacement réservé, vide en version 1 : `<!-- PRIX : prévu plus tard -->`

### Questions fréquentes
`[À CONFIRMER F11 : retouches comprises, acompte, cession des droits, délais]`

### Bloc de fin de page

---

## communication-globale.html

### Ouverture
`h1` : voir plan. Coupe : Un tournage, / tous vos supports de communication
Chapeau : De quoi communiquer pendant un an, à partir d'un seul tournage : un film, des reels, une banque de photos, et un site qui les met en valeur.
Bouton : **Parler de votre projet**

### Pour qui
Pour les entreprises qui lancent ou refont leur communication et qui veulent des supports cohérents, faits par la même personne, à partir du même tournage.

### Ce que vous recevez
- **Un film de présentation**, pour votre site, vos rendez-vous et vos réseaux
- **Des reels**, tirés du tournage
- **Une banque de photos** : vos locaux, votre équipe, vos produits, vos réalisations
- **Un site internet** qui met ces images en valeur, que je conçois et que je mets en ligne
- **La publication programmée** : vos posts Instagram et LinkedIn partent aux dates prévues, sans que vous ayez à y penser

### Ce que je ne fais pas
Je ne suis pas gestionnaire de réseaux sociaux. Je ne réponds pas aux commentaires et je ne publie pas au jour le jour. Je vous livre les contenus et le système qui les envoie. C'est plus simple pour vous, et vous ne dépendez de personne.

### La méthode, en quatre étapes
Reprendre la frise de l'accueil.

### Exemple
`[À CONFIRMER F8 : un client dont le site et les contenus ont été faits ensemble, avec son accord (Le Stud ou FL Nutrition)]`

### Budget
Même texte que la page mini-documentaire. Emplacement prix réservé, vide.

### Bloc de fin de page

---

## reels.html

### Ouverture
`h1` : voir plan. Coupe : Des reels tournés chez vous, / montés comme des films
Chapeau : Des formats courts pour Instagram, tournés chez vous avec du vrai matériel, puis montés et étalonnés comme des films.
Bouton : **Parler de votre projet**

### Deux façons de travailler
**À l'unité.** Un sujet, un tournage, un reel et ses versions courtes. Pour un lancement, un événement, une réalisation à montrer.

**La journée de tournage.** Une journée chez vous, plusieurs reels avec le même habillage. Vous avez de quoi publier pendant plusieurs semaines.

### Ce qui est compris
- Le tournage, avec le matériel image et son
- Le montage, l'étalonnage et le mixage du son
- Une musique libre de droits
- Les fichiers au format vertical 9:16, prêts à publier
- En option : sous-titres, version horizontale pour votre site, photos

`[À CONFIRMER F11 : nombre de séries de retouches comprises]`

### Exemples
Grille : les 6 reels de `src/donnees/projets.json`.

### Budget
Un devis par projet, ligne par ligne. Dites-moi votre budget : on voit ensemble combien de reels il permet. Emplacement prix réservé, vide.

### Bloc de fin de page

---

## artisans.html

### Ouverture
`h1` : voir plan. Coupe : Artisans et commerçants : / montrez votre savoir-faire
Chapeau : Vos clients choisissent avec les yeux. Un reel de votre atelier, quelques belles photos de vos réalisations et une courte présentation suffisent souvent à faire la différence.
Bouton : **Parler de votre projet**

### Ce que je peux faire pour vous
**Le reel savoir-faire.** Je viens une demi-journée dans votre atelier ou sur votre chantier. Vous repartez avec un reel et ses versions courtes, prêts à publier.

**Les photos.** Vos réalisations, votre lieu, vous au travail. Des images que vous pourrez réutiliser partout : site, réseaux, devis, vitrine.

**La présentation filmée.** Une à deux minutes pour dire qui vous êtes et ce que vous faites, à mettre en haut de votre site et de votre fiche Google.

### Un devis clair
Je vous envoie un devis ligne par ligne, avec ce qui est compris et ce qui est en option. Dites-moi ce que vous pouvez y mettre : j'ajuste le projet à votre budget.

### Ils m'ont fait confiance
Grille des reels de `projets.json` dont `public` contient `artisan`.

### Où je travaille
Dans les Landes et au Pays basque, autour de Capbreton, Hossegor, Dax et Bayonne.

### Bloc de fin de page

---

## video-immobiliere.html

### Ouverture
`h1` : voir plan. Coupe : Vidéo immobilière : / biens, programmes neufs et chantiers
Chapeau : Des vidéos et des photos pour vendre un bien, présenter un programme neuf ou suivre un chantier. Pour les agences, les promoteurs et les architectes.
Bouton : **Parler de votre projet**

### Ce que je réalise
- La vidéo d'un bien, intérieur et extérieur
- La présentation d'un programme neuf, déclinée en reels
- Le suivi d'un chantier, de la première visite à la livraison
- Les photos du bien ou de la réalisation

### Exemples
Reel « Complexe immobilier » (identifiant dans `projets.json`).
`[À FOURNIR F6 : vidéo Gabena Architecture sur Bunny ou YouTube, et son année]`

### Bloc de fin de page

---

## projets.html

Chapeau : Des films, des reels et des sites réalisés pour des artistes, des entreprises et des artisans.

### Films
Cartes des entrées `type: "film"` de `projets.json` (façade YouTube). Lien « Lire l'étude de cas » quand `etude` est renseigné et que la page existe.

### Reels
Grille des entrées `type: "reel"`.

### Bloc de fin de page

---

## projets/optima-delwood.html

Page construite seulement si la fiche F12 de ce projet est remplie.
Structure commune aux études de cas :
- Ouverture : `h1` du plan, média (façade YouTube `2J7MZ--tcww`).
- `### Le contexte` : `[À FOURNIR F12]`
- `### Ce que j'ai fait` : `[À FOURNIR F12]`
- `### Ce qui a été livré` : liste, `[À FOURNIR F12]`
- `### Le résultat` : `[À FOURNIR F12]` (bloc absent s'il n'y a pas de fait vérifiable)
- Citation : `[À FOURNIR F3]`
- Lien vers l'offre correspondante (`mini-documentaire.html`) et bloc de fin de page.

## projets/ziwig.html

Même structure. Média : façade YouTube `B3PK27fVF2A`. Tous les textes : `[À FOURNIR F12]`. Accord du client : F8.

## projets/tasta-wood-solution.html

Même structure. Média : reel Bunny `0bd76f20-e0cf-4149-971b-f0f35a9305da`. Tous les textes : `[À FOURNIR F12]`. Accord du client : F8. Offre liée : `artisans.html`.

---

## a-propos.html

### Ouverture
`h1` : voir plan. Coupe : 20 ans d'audiovisuel, / dont 18 à France Télévisions
Chapeau : Je m'appelle Pierre Bargelès. Je suis vidéaste à Capbreton, dans les Landes.
Image : portrait (`[À FOURNIR F5 : portrait]`).

### La télévision d'abord
J'ai passé 18 ans à France Télévisions, en régie et sur les cars de production : journaux télévisés, émissions politiques, Tour de France, Roland-Garros, rugby, Jeux olympiques. J'y ai été chef d'équipement, truquiste, ingénieur vision, opérateur ralenti et chef d'exploitation antenne. On y apprend que l'image et le son doivent être justes du premier coup, et à l'heure.

### Les films aujourd'hui
Je réalise des films pour des entreprises, des artistes et des artisans des Landes et du Pays basque. J'écris, je tourne, je monte et j'étalonne moi-même. Vous n'avez qu'un interlocuteur, et rien ne se perd entre l'idée et le film.
`[À CONFIRMER F14 : année de début de l'activité indépendante, si Pierre veut l'afficher]`

### Les sites aussi
Je me suis formé au développement web. Je conçois donc aussi les sites qui accueillent mes images, et les automatisations qui publient vos contenus à votre place.

### Les outils
DaVinci Resolve · Premiere Pro · After Effects · Photoshop · Lightroom · Ableton Live · Webflow · Figma

### Lien
**Voir mon CV et mon portfolio** → `portfolio/`

### Bloc de fin de page

---

## contact.html

### Ouverture
Chapeau : Le plus simple est de m'appeler. Sinon, écrivez-moi : quelques lignes suffisent, même si le projet n'est pas encore clair.
Coordonnées : téléphone (lien `tel:`), e-mail (lien `mailto:`), Capbreton (40).

### Le formulaire (titre visible : « M'écrire »)
- **Vous êtes** (boutons radio) : Une entreprise ou une marque · Un artisan ou un commerçant · Un artiste ou une association · Autre
- **Votre projet** (liste) : Un mini-documentaire ou un film · Des reels · Des photos · Un site internet · Une communication complète · Je ne sais pas encore
- **Votre budget** (liste, facultatif) : Moins de 1 000 € · 1 000 à 3 000 € · Plus de 3 000 € · Je ne sais pas encore
- **Nom** (obligatoire) · **E-mail** (obligatoire) · **Téléphone** (obligatoire) · **Message**
- Bouton : **Envoyer le message**
- Sous le bouton : Ces informations servent uniquement à vous répondre. Voir la politique de confidentialité.
- Pendant l'envoi : Envoi en cours…
- Succès : Merci, votre message est parti. Je vous réponds rapidement.
- Erreur : Le message n'est pas parti. Réessayez, ou appelez-moi au 06 70 71 84 05.

Contrat technique : `ARCHITECTURE.md` §11.

---

## mentions-legales.html

`[À FOURNIR F7 : adresse à afficher, numéro SIRET, relecture par Pierre]`

Plan de la page, à remplir avec F7 :
- `### Éditeur du site` : Pierre Bargelès, entrepreneur individuel (EI) · adresse · SIRET · téléphone · e-mail · TVA non applicable, article 293 B du CGI
- `### Directeur de la publication` : Pierre Bargelès
- `### Hébergeur` : OVH SAS, 2 rue Kellermann, 59100 Roubaix, France (à vérifier par Pierre sur son espace client OVH)
- `### Propriété intellectuelle` : Les films, les photos et les textes de ce site sont la propriété de Pierre Bargelès ou de ses clients. Toute reproduction demande un accord écrit.
- `### Crédits` : Conception et réalisation du site : Pierre Bargelès.

## confidentialite.html

`[À FOURNIR F7 : durée de conservation des messages, relecture par Pierre]`

Plan de la page, à remplir avec F7 :
- `### Les données collectées` : celles du formulaire de contact (nom, e-mail, téléphone, message). Rien d'autre.
- `### À quoi elles servent` : à répondre à la demande. Elles ne sont ni vendues ni transmises.
- `### Combien de temps elles sont gardées` : durée fournie par Pierre.
- `### Où elles sont hébergées` : chez OVH, en France.
- `### Vidéos` : les reels sont diffusés par Bunny Stream ; les films YouTube ne se chargent qu'au clic sur l'image. Le site ne dépose aucun cookie de mesure d'audience.
- `### Vos droits` : accès, rectification, suppression, par simple e-mail. Réclamation possible auprès de la CNIL (cnil.fr).
