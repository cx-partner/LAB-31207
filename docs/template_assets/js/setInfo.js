(function () {
    var encodedInfo = window.location.search.slice(1);
    if (!encodedInfo) return;

    try {
        var info = JSON.parse(atob(encodedInfo));
        Object.keys(info).forEach(function (key) {
            sessionStorage.setItem(key, info[key]);
        });
        window.history.replaceState(null, "", window.location.pathname + window.location.hash);
    } catch (err) {
        console.warn("Ignoring an invalid lab information query.");
    }
})();
