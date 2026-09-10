

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
})();
</script>
