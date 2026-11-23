/* contact.js : envoi du formulaire (ARCHITECTURE.md §11).
   Construit un FormData avec les six champs de form-handler.php seulement ;
   profil, projet et budget sont placés en tête de Message. */
(function () {
  "use strict";
  var form = document.getElementById("formulaire");
  if (!form) return;
  var etat = document.getElementById("etat-formulaire");
  var bouton = form.querySelector("button[type=submit]");
  var libelleBouton = bouton ? bouton.textContent : "";

  function valeur(nom) {
    var c = form.elements[nom];
    return c && c.value ? c.value.trim() : "";
  }
  function profil() {
    var coche = form.querySelector("input[name=profil]:checked");
    return coche ? coche.value : "";
  }
  function construire() {
    var entete = "[Profil : " + (profil() || "Non précisé") + "] " +
      "[Projet : " + (valeur("Subject") || "Non précisé") + "] " +
      "[Budget : " + (valeur("budget") || "Non précisé") + "]";
    var texte = valeur("Message");
    var d = new FormData();
    d.append("Name", valeur("Name"));
    d.append("Email", valeur("Email"));
    d.append("T-l-phone", valeur("T-l-phone"));
    d.append("Subject", valeur("Subject") || "Contact");
    d.append("Message", entete + (texte ? "\n\n" + texte : ""));
    d.append("honeypot", valeur("honeypot"));
    return d;
  }
  function dire(texte, erreur) {
    etat.textContent = texte;
    etat.className = "etat" + (erreur ? " etat-erreur" : "");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    bouton.disabled = true;
    bouton.textContent = "Envoi en cours…";
    dire("");
    fetch("form-handler.php", { method: "POST", body: construire() })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.success) {
          form.reset();
          dire("Merci, votre message est parti. Je vous réponds rapidement.");
        } else {
          dire("Le message n’est pas parti. Réessayez, ou appelez-moi au 06 70 71 84 05.", true);
        }
      })
      .catch(function () {
        dire("Le message n’est pas parti. Réessayez, ou appelez-moi au 06 70 71 84 05.", true);
      })
      .then(function () {
        bouton.disabled = false;
        bouton.textContent = libelleBouton;
      });
  });
  form.setAttribute("novalidate", "novalidate");
})();
