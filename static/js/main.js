document.addEventListener("DOMContentLoaded", function () {
  const themeSwitcher = document.getElementById("theme-switcher");
  const body = document.body;
  const themeIcon = themeSwitcher.querySelector("i");
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) {
    body.classList.add(savedTheme);
    if (savedTheme === "light-mode") {
      themeIcon.classList.remove("bxs-sun");
      themeIcon.classList.add("bxs-moon");
    }
  }

  themeSwitcher.addEventListener("click", function () {
    body.classList.toggle("light-mode");
    if (body.classList.contains("light-mode")) {
      localStorage.setItem("theme", "light-mode");
      themeIcon.classList.remove("bxs-sun");
      themeIcon.classList.add("bxs-moon");
    } else {
      localStorage.removeItem("theme");
      themeIcon.classList.remove("bxs-moon");
      themeIcon.classList.add("bxs-sun");
    }
  });
});
