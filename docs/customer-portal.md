# Customer Portal

Create a new account, or look up and update an existing one using your Customer ID and PIN.

<p><a href="app.html" target="_blank">Open in a new tab ↗</a></p>

<iframe id="customerPortalFrame" src="app.html" style="width:100%; min-height:500px; border:none;" title="Customer Portal"></iframe>

<script>
(function () {
  var frame = document.getElementById("customerPortalFrame");
  function resizeFrame() {
    var top = frame.getBoundingClientRect().top;
    var available = window.innerHeight - top - 24;
    frame.style.setProperty("height", Math.max(500, available) + "px", "important");
  }
  resizeFrame();
  window.addEventListener("resize", resizeFrame);
  window.addEventListener("load", resizeFrame);
  setTimeout(resizeFrame, 300); // catch late layout shifts (fonts, etc.)
})();
</script>

<script>
(function () {
  function currentScheme() {
    return document.documentElement.getAttribute("data-md-color-scheme") ||
      (document.body && document.body.getAttribute("data-md-color-scheme")) || "";
  }
  function sync() {
    var scheme = currentScheme();
    if (scheme) localStorage.setItem("cp-theme", scheme);
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
</script>
