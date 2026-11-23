# Refonte de pibes.fr

Site statique de Pierre Bargelès, vidéaste à Capbreton. Construit par `build.py` (Python, bibliothèque standard), contrôlé par `verifier.py`.

- `src/` : pages, partiels, CSS, JS, données des projets
- `statique/` : polices, images web (produites par `optimiser.py` depuis les originaux, qui restent sur l'ordinateur)
- `plan-site.json` : pages, titres, descriptions, redirections, budgets
- `SUIVI.md` : état des lots, questions en cours, journal

## Construire

    python3 build.py              # site final dans dist/ (à envoyer chez OVH)
    python3 build.py --staging    # site de test, noindex
    python3 build.py --apercu     # aperçu GitHub Pages dans apercu/
    python3 verifier.py --lot 8   # recette

L'aperçu est publié automatiquement sur GitHub Pages à chaque envoi sur `main` (`.github/workflows/apercu.yml`). Il n'est pas indexé par les moteurs de recherche. Le formulaire de contact n'y fonctionne pas (il a besoin du serveur OVH).
