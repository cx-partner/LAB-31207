# Lab Prework

Complete this before the hands-on labs: get your POD assigned, then your test customer record will be provisioned automatically.

<div class="admonition warning" id="preworkRequiredBanner" style="display:none;">
  <p class="admonition-title">Prework required</p>
  <p>You need to complete the Lab Prework before starting the Labs. Please finish the steps below first.</p>
</div>

<p><a href="app.html" target="_blank">Open in a new tab ↗</a></p>

<iframe id="labPreworkFrame" src="app.html" style="width:100%; min-height:500px; border:none;" title="Lab Prework"></iframe>

<script>
(function () {
  var frame = document.getElementById("labPreworkFrame");
  function resizeFrame() {
    var top = frame.getBoundingClientRect().top;
    var available = window.innerHeight - top - 24;
    frame.style.setProperty("height", Math.max(500, available) + "px", "important");
  }
  resizeFrame();
  window.addEventListener("resize", resizeFrame);
  window.addEventListener("load", resizeFrame);
  setTimeout(resizeFrame, 300);

  if (window.location.search.indexOf("prework_required=1") !== -1) {
    var banner = document.getElementById("preworkRequiredBanner");
    if (banner) banner.style.display = "block";
  }
})();
</script>
