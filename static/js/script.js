function setTheme(theme) {
    const bodyElement = document.querySelector(".jp-Notebook");
    bodyElement.setAttribute("data-theme", theme.split(":")[0]);
    bodyElement.setAttribute("data-jp-theme-light", theme.includes("light") ? "true" : "false");
}

(() => {
    const bodyElement = document.querySelector(".jp-Notebook");

    console.log("Notebook Script loaded successfully.");
    // Create a select element for themes
    const themes = ["dracula", "github-light", "github-dark"];

    const themeSelect = document.createElement("select");
    themeSelect.classList.add("theme-selector");
    themeSelect.title = "Select Theme";
    themeSelect.name = "themes";
    themes.forEach((theme) => {
        const option = document.createElement("option");
        option.value = theme;
        option.textContent = theme
            .split("-")
            .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
        themeSelect.appendChild(option);
    });

    themeSelect.addEventListener("change", () => {
        setTheme(themeSelect.value);
    });
    // On page load, set the theme to the first option
    setTheme(themes[0]);

    bodyElement.appendChild(themeSelect);
})();
