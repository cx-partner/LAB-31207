/* ---------- Mirror the site's light/dark scheme into localStorage ---------- */
/* Loaded on every page (see mkdocs.yml extra_javascript) so any embedded app  */
/* can follow the toggle regardless of which page it was clicked on.          */
(function () {
  function currentScheme() {
    return document.documentElement.getAttribute("data-md-color-scheme") ||
      (document.body && document.body.getAttribute("data-md-color-scheme")) || "";
  }
  function sync() {
    var scheme = currentScheme();
    if (scheme) {
      try { localStorage.setItem("cp-theme", scheme); } catch (err) {}
    }
  }
  sync();
  if (window.MutationObserver) {
    new MutationObserver(sync).observe(document.documentElement, {
      attributes: true, attributeFilter: ["data-md-color-scheme"]
    });
    if (document.body) {
      new MutationObserver(sync).observe(document.body, {
        attributes: true, attributeFilter: ["data-md-color-scheme"]
      });
    }
  }
})();

/* ---------- Populate lab-guide placeholders with this attendee's values ---------- */
/* Usage in any docs page:                                                     */
/*   <span class="lab-var" data-var="pod"></span>                              */
/*   <span class="lab-var" data-var="adminEmail"></span>                       */
/* Supported data-var keys: pod, email, firstName, lastName, partner,        */
/* adminEmail, agentEmail, labPassword, customerEmail, customerPassword.      */
/* Optional data-fallback="..." sets the text shown before registration.       */
(function () {
  function populate() {
    var nodes = document.querySelectorAll(".lab-var[data-var]");
    if (!nodes.length) return;
    var raw = null;
    try { raw = localStorage.getItem("labUserInfo"); } catch (err) { return; }
    var info = null;
    if (raw) {
      try { info = JSON.parse(raw); } catch (err) { info = null; }
    }
    nodes.forEach(function (el) {
      var key = el.getAttribute("data-var");
      if (info && info[key] != null && info[key] !== "") {
        el.textContent = info[key];
        el.classList.remove("lab-var-missing");
      } else {
        el.textContent = el.getAttribute("data-fallback") || "— register for your POD first —";
        el.classList.add("lab-var-missing");
      }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", populate);
  } else {
    populate();
  }
  window.addEventListener("storage", function (e) {
    if (e.key === "labUserInfo" || e.key === null) populate();
  });
})();
