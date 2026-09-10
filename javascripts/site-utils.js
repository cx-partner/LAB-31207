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

/* ---------- Hide the "Labs" nav link until Lab Prework is completed ---------- */
/* This is convenience/guidance only, not real access control — the Labs page  */
/* is still reachable by direct URL even while hidden from the nav.            */
(function () {
  function hasCompletedPrework() {
    try {
      var info = JSON.parse(localStorage.getItem("labUserInfo") || "null");
      return !!(info && info.pod && info.customerId);
    } catch (err) {
      return false;
    }
  }
  function toggleLabsNav() {
    var done = hasCompletedPrework();
    document.querySelectorAll("a").forEach(function (a) {
      var label = (a.textContent || "").trim().toLowerCase();
      var href = (a.getAttribute("href") || "").toLowerCase();
      var isLabsLink = label === "labs" || href.indexOf("labs/") !== -1 || href.indexOf("labs.md") !== -1 || href === "labs";
      if (!isLabsLink) return;
      var container = a.closest("li") || a;
      container.style.display = done ? "" : "none";
    });
  }
  toggleLabsNav();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", toggleLabsNav);
  }
  window.addEventListener("storage", function (e) {
    if (e.key === "labUserInfo" || e.key === null) toggleLabsNav();
  });
  // Re-check periodically to survive MkDocs "instant navigation" DOM swaps,
  // which don't fire a normal page load / DOMContentLoaded.
  setInterval(toggleLabsNav, 1000);
})();
