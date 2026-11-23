/* site.js : chargé sur toutes les pages (defer).
   Menu mobile, barre d'action mobile, tête de lecture de la frise.
   Aucune apparition au défilement : le contenu est visible sans ce script. */
(function () {
  "use strict";
  var html = document.documentElement;
  html.classList.add("js");
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- Menu plein écran (sous 1080 px) ---------- */
  var bouton = document.querySelector(".menu-bouton");
  var menu = document.getElementById("menu");
  var entete = document.querySelector(".entete");
  var large = window.matchMedia("(min-width: 1080px)");

  function basculer(ouvert, rendreFocus) {
    if (!bouton || !menu) return;
    bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    bouton.querySelector(".menu-bouton-texte").textContent = ouvert ? "Fermer" : "Menu";
    menu.classList.toggle("ouvert", ouvert);
    entete.classList.toggle("menu-ouvert", ouvert);
    html.classList.toggle("sans-defilement", ouvert);
    if (ouvert) {
      var premier = menu.querySelector("a");
      if (premier) premier.focus({ preventScroll: true });
    } else if (rendreFocus) {
      bouton.focus();
    }
  }

  if (bouton && menu) {
    bouton.addEventListener("click", function () {
      basculer(bouton.getAttribute("aria-expanded") !== "true", true);
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) basculer(false, false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && bouton.getAttribute("aria-expanded") === "true") basculer(false, true);
    });
    var auChangement = function () { if (large.matches) basculer(false, false); };
    if (large.addEventListener) large.addEventListener("change", auChangement);
    else if (large.addListener) large.addListener(auChangement);
  }

  /* ---------- Barre d'action mobile ----------
     Visible une fois l'ouverture passée, masquée quand le bloc de fin de page
     ou le pied de page est à l'écran (ils portent déjà les mêmes actions). */
  var barre = document.getElementById("barre-mobile");
  var ouverture = document.querySelector(".ouverture") || document.getElementById("haut");
  var fins = [document.getElementById("appel"), document.getElementById("pied")].filter(Boolean);
  if (barre && ouverture && "IntersectionObserver" in window) {
    var ouvertureVue = true;
    var finsVues = new Set();
    new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.target === ouverture) ouvertureVue = e.isIntersecting;
        else if (e.isIntersecting) finsVues.add(e.target);
        else finsVues.delete(e.target);
      });
      barre.classList.toggle("visible", !ouvertureVue && finsVues.size === 0);
    }).observe(ouverture);
    var obsFins = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.isIntersecting) finsVues.add(e.target);
        else finsVues.delete(e.target);
      });
      barre.classList.toggle("visible", !ouvertureVue && finsVues.size === 0);
    });
    fins.forEach(function (f) { obsFins.observe(f); });
  }

  /* ---------- Frise : la tête de lecture suit le défilement ----------
     Chaque .frise contient des .clip (data-libelle="01", ou data-debut / data-fin
     pour des années) et une .tete. Le calcul ne tourne que quand la frise est à l'écran.
     Masquée si l'utilisateur a demandé moins d'animations. */
  document.querySelectorAll(".frise").forEach(function (frise) {
    var tete = frise.querySelector(".tete");
    var libelle = tete && tete.querySelector("span");
    var clips = Array.prototype.slice.call(frise.querySelectorAll(".clip"));
    if (!tete || !clips.length || !("IntersectionObserver" in window)) return;
    var enAttente = false;
    function placer() {
      enAttente = false;
      if (reduit.matches) return;
      var zone = frise.getBoundingClientRect();
      var y = Math.max(0, Math.min(zone.height - 2, window.innerHeight * 0.55 - zone.top));
      var clip = clips.find(function (c) { return y < c.offsetTop + c.offsetHeight; }) || clips[clips.length - 1];
      if (libelle) {
        if (clip.dataset.debut && clip.dataset.fin) {
          var avance = Math.max(0, Math.min(1, (y - clip.offsetTop) / clip.offsetHeight));
          var fin = Number(clip.dataset.fin);
          libelle.textContent = Math.round(fin - avance * (fin - Number(clip.dataset.debut)));
        } else {
          libelle.textContent = clip.dataset.libelle || "";
        }
      }
      clips.forEach(function (c) { c.classList.toggle("en-cours", c === clip); });
      tete.style.transform = "translateY(" + y + "px)";
    }
    function demander() {
      if (enAttente) return;
      enAttente = true;
      window.requestAnimationFrame(placer);
    }
    frise.classList.add("frise-active");
    new IntersectionObserver(function (entrees) {
      var visible = entrees[0].isIntersecting;
      var action = visible ? "addEventListener" : "removeEventListener";
      window[action]("scroll", demander, { passive: true });
      window[action]("resize", demander, { passive: true });
      if (visible) demander();
    }).observe(frise);
  });
})();
