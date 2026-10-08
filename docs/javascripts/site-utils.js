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
/* adminEmail, agentEmail, labPassword, customerEmail, customerPassword,      */
/* customerPhone.                                                             */
/* Optional data-fallback="..." sets the text shown before registration.       */
(function () {
  function populate() {
    var info = getLabUserInfo();
    replacePodPlaceholders(info);
    var nodes = document.querySelectorAll(".lab-var[data-var]");
    if (!nodes.length) return;
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
  function getLabUserInfo() {
    var raw = null;
    var info = null;
    try { raw = localStorage.getItem("labUserInfo"); } catch (err) {}
    if (raw) {
      try { info = JSON.parse(raw); } catch (err) {}
    }

    // localStorage is isolated by port. Retain only the non-sensitive POD
    // number in a host cookie so a local MkDocs preview can move from :8000
    // to another port without losing its POD-specific names.
    if (!info) info = {};
    if (!info.pod) info.pod = getLabPodCookie();
    return info;
  }
  function getLabPodCookie() {
    var match = document.cookie.match(/(?:^|;\s*)lab-pod=([^;]*)/);
    if (!match) return "";
    try { return decodeURIComponent(match[1]); } catch (err) { return ""; }
  }
  function formattedPod(pod) {
    var value = String(pod).trim();
    if (!value) return null;
    if (/^\d+$/.test(value)) value = value.padStart(2, "0");
    return "POD" + value;
  }
  function replacePodPlaceholders(info) {
    var pod = info && formattedPod(info.pod);
    var podNumber = pod && pod.replace(/^POD/, "");
    var content = document.querySelector("main");
    if (!pod || !content || !window.NodeFilter) return;
    var walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || /^(SCRIPT|STYLE|TEXTAREA)$/i.test(parent.tagName)) {
          return NodeFilter.FILTER_REJECT;
        }
        return /PODXX|<(?:your|you|yout)pod(?:number|name|nr)>|(?:your|you|yout)pod(?:number|name|nr)/i.test(node.nodeValue)
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      }
    });
    var textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    textNodes.forEach(function (node) {
      node.nodeValue = node.nodeValue
        .replace(/PODXX/g, pod)
        .replace(/<(?:your|you|yout)pod(?:number|name|nr)>/gi, podNumber)
        .replace(/(?:your|you|yout)pod(?:number|name|nr)/gi, podNumber);
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", populate);
  } else {
    populate();
  }
  // Material's instant-navigation API is not exposed consistently across
  // versions. Watch the rendered guide instead, so POD values are reapplied
  // whenever the page content is swapped without a full browser reload.
  if (window.MutationObserver && document.body) {
    var populateQueued = false;
    new MutationObserver(function (records) {
      var guideChanged = records.some(function (record) {
        return record.type === "childList" && Array.prototype.some.call(
          record.addedNodes,
          function (node) { return node.nodeType === 1; }
        );
      });
      if (!guideChanged || populateQueued) return;
      populateQueued = true;
      window.requestAnimationFrame(function () {
        populateQueued = false;
        populate();
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
  window.addEventListener("storage", function (e) {
    if (e.key === "labUserInfo" || e.key === null) populate();
  });
})();

/* ---------- Reveal Labs links once Lab Prework is completed ---------- */
/* The actual hiding is done in CSS (see stylesheets/extra.css), which applies */
/* before first paint — no flash. This script's only job is flipping           */
/* data-prework-done on <html> so that CSS rule lets the links show again.     */
/* Convenience/guidance only, not real access control — the Labs page is       */
/* still reachable by direct URL even while its links are hidden.              */
(function () {
  function hasCompletedPrework() {
    try {
      var info = JSON.parse(localStorage.getItem("labUserInfo") || "null");
      return !!(info && info.pod && info.customerId);
    } catch (err) {
      return false;
    }
  }
  function syncPreworkAttribute() {
    if (hasCompletedPrework()) {
      document.documentElement.setAttribute("data-prework-done", "");
    } else {
      document.documentElement.removeAttribute("data-prework-done");
    }
  }
  syncPreworkAttribute();
  window.addEventListener("storage", function (e) {
    if (e.key === "labUserInfo" || e.key === null) syncPreworkAttribute();
  });
  // Re-check periodically to survive MkDocs "instant navigation" DOM swaps,
  // which don't fire a normal page load / DOMContentLoaded.
  setInterval(syncPreworkAttribute, 1000);
})();
