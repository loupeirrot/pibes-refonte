/* video.js : façade YouTube, grilles de reels (aperçus et lecteur plein écran),
   vidéo d'ouverture. Chargé sur les gabarits accueil, offre, realisations, etude.
   Sans ce script, chaque vignette reste un lien vers la vidéo : rien n'est caché.
   Aucune vidéo, aucun lecteur tiers n'est chargé avant que le visiteur le demande,
   sauf les aperçus muets des reels, chargés seulement quand la vignette est à l'écran. */
(function () {
  "use strict";

  var BUNNY_BIBLIOTHEQUE = "801824";
  var BUNNY_CDN = "vz-25e90935-e10.b-cdn.net";
  var APERCU_DUREE = 8;      // secondes lues en boucle
  var APERCU_MAX = 2;        // aperçus en lecture en même temps
  var APERCU_SEUIL = 0.35;   // part de la vignette visible pour lancer l'aperçu

  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var economie = !!(navigator.connection && navigator.connection.saveData);
  var html = document.documentElement;

  var ICONES = {
    prec: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12.5 4.5 7 10l5.5 5.5"/></svg>',
    suiv: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7.5 4.5 13 10l-5.5 5.5"/></svg>',
    fermer: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 5l10 10M15 5 5 15"/></svg>'
  };

  /* ======================================================================
     FILMS : la façade (image + bouton) est remplacée par le lecteur au clic
     ====================================================================== */
  document.querySelectorAll("[data-youtube]").forEach(function (lien) {
    lien.addEventListener("click", function (e) {
      e.preventDefault();
      var id = lien.getAttribute("data-youtube");
      var cadre = document.createElement("iframe");
      cadre.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1&rel=0&playsinline=1";
      cadre.title = lien.getAttribute("data-titre") || "Lecteur YouTube";
      cadre.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      cadre.allowFullscreen = true;
      cadre.referrerPolicy = "strict-origin-when-cross-origin";
      lien.replaceWith(cadre);
      cadre.focus();
    });
  });

  /* ======================================================================
     VIDÉO D'OUVERTURE : <video preload="none" data-src="…">
     La source n'est posée qu'après le chargement de la page, et jamais si le
     visiteur demande moins d'animations ou économise ses données.
     ====================================================================== */
  var videosOuverture = document.querySelectorAll("video[data-src]");
  if (videosOuverture.length && !reduit && !economie) {
    window.addEventListener("load", function () {
      videosOuverture.forEach(function (v) {
        v.muted = true;
        v.playsInline = true;
        var petit = v.getAttribute("data-src-petit");
        v.src = (petit && window.innerWidth < 768) ? petit : v.getAttribute("data-src");
        v.addEventListener("playing", function () { v.classList.add("joue"); }, { once: true });
        var essai = v.play();
        if (essai && essai.catch) essai.catch(function () { /* l'image poster reste affichée */ });
      });
    });
  }

  /* ======================================================================
     REELS : une grille par .grille-reels, générée par build.py depuis projets.json
     ====================================================================== */
  var grilles = Array.prototype.slice.call(document.querySelectorAll(".grille-reels"));
  if (!grilles.length) return;

  var etats = [];
  var apercusPermis = !reduit && !economie;
  var lecteurOuvert = false;

  grilles.forEach(function (grille) {
    var liens = Array.prototype.slice.call(grille.querySelectorAll("a.reel"));
    liens.forEach(function (lien, i) {
      var e = {
        lien: lien,
        liste: liens,
        index: i,
        id: lien.getAttribute("data-video"),
        zoom: lien.querySelector(".reel-zoom"),
        avance: lien.querySelector(".reel-avance"),
        video: null, ratio: 0, joue: false, survol: false, echec: false
      };
      etats.push(e);
      lien.addEventListener("click", function (ev) {
        ev.preventDefault();
        ouvrirLecteur(liens, i);
      });
      lien.addEventListener("pointerenter", function (ev) {
        if (ev.pointerType === "mouse") { e.survol = true; repartir(); }
      });
      lien.addEventListener("pointerleave", function () {
        if (e.survol) { e.survol = false; repartir(); }
      });
    });
  });

  /* ---------- Aperçus animés : 8 secondes muettes, 2 au plus ---------- */
  function creerVideo(e) {
    var v = document.createElement("video");
    // attributs et propriétés : les deux sont nécessaires pour la lecture en ligne sur iPhone
    ["muted", "playsinline", "loop", "disablepictureinpicture"].forEach(function (a) { v.setAttribute(a, ""); });
    v.setAttribute("preload", "none");
    v.setAttribute("tabindex", "-1");
    v.setAttribute("aria-hidden", "true");
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.disableRemotePlayback = true;
    v.src = "https://" + BUNNY_CDN + "/" + e.id + "/play_360p.mp4";
    v.addEventListener("playing", function () { if (e.joue) e.lien.classList.add("en-lecture"); });
    v.addEventListener("timeupdate", function () {
      if (v.currentTime >= APERCU_DUREE) v.currentTime = 0;
      e.avance.style.transform = "scaleX(" + Math.min(v.currentTime / APERCU_DUREE, 1) + ")";
    });
    v.addEventListener("error", function () { abandonner(e); repartir(); });
    e.zoom.appendChild(v);
    return v;
  }

  /* Si la lecture échoue, la vidéo est retirée : la vignette reste affichée */
  function abandonner(e) {
    e.echec = true;
    e.joue = false;
    e.lien.classList.remove("en-lecture", "principal");
    if (e.video) { e.video.remove(); e.video = null; }
  }

  function jouer(e) {
    if (e.joue) return;
    e.joue = true;
    if (!e.video) e.video = creerVideo(e);
    var essai = e.video.play();
    if (essai && essai.catch) essai.catch(function (err) {
      if (err && err.name === "AbortError") return;           // simple pause pendant le chargement
      if (err && err.name === "NotAllowedError") apercusPermis = false; // économie d'énergie sur iPhone
      abandonner(e);
      repartir();
    });
  }

  function arreter(e) {
    if (!e.joue) return;
    e.joue = false;
    e.lien.classList.remove("en-lecture");
    if (e.video) e.video.pause();
  }

  /* Répartit les places : la vignette survolée, puis celles déjà en lecture, puis les plus visibles.
     Seule la première porte la barre de progression ambre (un seul élément ambre par écran). */
  function repartir() {
    var actif = apercusPermis && !lecteurOuvert && !document.hidden;
    var choisis = !actif ? [] : etats
      .filter(function (e) { return !e.echec && (e.survol || e.ratio >= APERCU_SEUIL); })
      .sort(function (a, b) {
        return (b.survol - a.survol) || (b.joue - a.joue) || (b.ratio - a.ratio) || (etats.indexOf(a) - etats.indexOf(b));
      })
      .slice(0, APERCU_MAX);
    etats.forEach(function (e) {
      if (choisis.indexOf(e) !== -1) jouer(e); else arreter(e);
      e.lien.classList.toggle("principal", choisis[0] === e);
    });
  }

  if ("IntersectionObserver" in window) {
    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        var e = etats.find(function (x) { return x.lien === entree.target; });
        e.ratio = entree.isIntersecting ? entree.intersectionRatio : 0;
        e.lien.classList.toggle("visible", entree.isIntersecting);
      });
      repartir();
    }, { threshold: [0, APERCU_SEUIL, 0.6, 0.85, 1] });
    etats.forEach(function (e) { observateur.observe(e.lien); });
  }
  document.addEventListener("visibilitychange", repartir);

  /* ---------- Lecteur plein écran : lecteur Bunny chargé au clic, avec le son ---------- */
  var lecteur = null, scene, titre, sous, liste = [], courant = 0, declencheur = null;

  function construireLecteur() {
    lecteur = document.createElement("dialog");
    lecteur.className = "lecteur";
    lecteur.setAttribute("aria-label", "Lecteur de reels");
    lecteur.innerHTML =
      '<div class="scene"></div>' +
      '<div class="commandes">' +
      '<button class="rond lecteur-prec" type="button" aria-label="Reel précédent">' + ICONES.prec + '</button>' +
      '<p class="infos" aria-live="polite"><strong></strong><span></span></p>' +
      '<button class="rond lecteur-suiv" type="button" aria-label="Reel suivant">' + ICONES.suiv + '</button>' +
      '<button class="rond fermer" type="button" aria-label="Fermer le lecteur">' + ICONES.fermer + '</button>' +
      '</div>';
    document.body.appendChild(lecteur);
    scene = lecteur.querySelector(".scene");
    titre = lecteur.querySelector(".infos strong");
    sous = lecteur.querySelector(".infos span");
    lecteur.querySelector(".lecteur-prec").addEventListener("click", function () { charger(courant - 1); });
    lecteur.querySelector(".lecteur-suiv").addEventListener("click", function () { charger(courant + 1); });
    lecteur.querySelector(".fermer").addEventListener("click", function () { lecteur.close(); });
    // fermeture, y compris par Échap : l'iframe retirée coupe le son
    lecteur.addEventListener("close", function () {
      scene.innerHTML = "";
      html.classList.remove("sans-defilement");
      lecteurOuvert = false;
      repartir();
      if (declencheur) declencheur.focus();
    });
    document.addEventListener("keydown", function (ev) {
      if (!lecteurOuvert) return;
      if (ev.key === "ArrowLeft") charger(courant - 1);
      if (ev.key === "ArrowRight") charger(courant + 1);
    });
    // un clic dans l'iframe lui donne le clavier : on le reprend pour garder Échap et les flèches
    window.addEventListener("blur", function () {
      if (!lecteurOuvert || !window.matchMedia("(hover: hover)").matches) return;
      setTimeout(function () {
        if (document.activeElement && document.activeElement.tagName === "IFRAME" && !document.fullscreenElement) {
          document.activeElement.blur();
          window.focus();
        }
      }, 0);
    });
  }

  function charger(i) {
    courant = (i + liste.length) % liste.length;
    var lien = liste[courant];
    var cadre = document.createElement("iframe");
    cadre.src = "https://iframe.mediadelivery.net/embed/" + BUNNY_BIBLIOTHEQUE + "/" +
      encodeURIComponent(lien.getAttribute("data-video")) + "?autoplay=true&preload=true&responsive=true";
    cadre.title = "Lecteur vidéo : " + lien.getAttribute("data-titre");
    cadre.allow = "accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture; fullscreen";
    cadre.allowFullscreen = true;
    scene.innerHTML = "";
    scene.appendChild(cadre);
    titre.textContent = lien.getAttribute("data-titre");
    sous.textContent = lien.getAttribute("data-sous") + " · " + (courant + 1) + " / " + liste.length;
  }

  function ouvrirLecteur(liens, i) {
    if (!lecteur) construireLecteur();
    if (typeof lecteur.showModal !== "function") {
      window.location.href = liens[i].href; // navigateur trop ancien : page du lecteur Bunny
      return;
    }
    declencheur = liens[i];
    liste = liens;
    lecteurOuvert = true;
    repartir();
    html.classList.add("sans-defilement");
    charger(i);
    lecteur.showModal();
    lecteur.querySelector(".fermer").focus();
  }
})();
