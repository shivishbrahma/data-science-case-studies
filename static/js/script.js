const THEMES = [
    { "name": "Dracula", "value": "dracula", "is_light": false },
    { "name": "GitHub Light", "value": "github-light", "is_light": true },
    { "name": "GitHub Dark", "value": "github-dark", "is_light": false },
]

function setTheme(theme, select) {
    const nbkEle = document.querySelector(".jp-Notebook");
    const themeData = THEMES.find((themeData) => themeData.value === theme);
    nbkEle.setAttribute("data-theme", themeData.value);
    nbkEle.setAttribute("data-jp-theme-light", themeData.is_light ? "true" : "false");
    console.log("Theme changed to " + theme);
    if(select.value === theme) return;
    select.value = theme;
}

(() => {
    const headerElement = document.querySelector("#jp-Notebook-header");

    console.log("Notebook Script loaded successfully.");
    // Create a select element for themes
    const themeSelect = document.createElement("select");
    themeSelect.classList.add("theme-selector");
    themeSelect.title = "Select Theme";
    themeSelect.name = "themes";
    Object.values(THEMES).forEach((theme) => {
        const option = document.createElement("option");
        option.value = theme.value;
        option.textContent = theme.name;
        themeSelect.appendChild(option);
    });

    themeSelect.addEventListener("change", (event) => {
        setTheme(event.target.value, event.target);
    });
    // Check if the current theme is dark or light
    const isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
    // Set the initial theme
    setTheme(isDarkMode ? "github-dark" : "github-light", themeSelect);

    headerElement.appendChild(themeSelect);
})();
