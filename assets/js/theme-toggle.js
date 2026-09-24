/* Light/dark toggle. head.html has already set html[data-theme] before first
   paint; this only handles clicks and live system changes. The storage key and
   values match the blog, so the choice is shared on functionhx.github.io. */
(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme-toggle");
  var themeColor = document.querySelector('meta[name="theme-color"]');
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function storedSetting() {
    try {
      return localStorage.getItem("theme");
    } catch (e) {
      return null;
    }
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    if (button) button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    if (themeColor) themeColor.setAttribute("content", theme === "dark" ? "#1c1c1d" : "#ffffff");
  }

  apply(root.getAttribute("data-theme") === "dark" ? "dark" : "light");

  if (media && media.addEventListener) {
    media.addEventListener("change", function (event) {
      var setting = storedSetting();
      if (setting !== "dark" && setting !== "light") apply(event.matches ? "dark" : "light");
    });
  }

  if (button) {
    button.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      try {
        localStorage.setItem("theme", next);
      } catch (e) {}
      apply(next);
    });
  }
})();
