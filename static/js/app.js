// Dark Mode Toggle
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("themeToggle");
    const body = document.body;

    // Load from localStorage
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark");
        toggle.checked = true;
    }

    toggle.addEventListener("change", () => {
        body.classList.toggle("dark");
        localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
    });
});
