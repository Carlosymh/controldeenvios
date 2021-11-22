const navToggle = document.querySelector(".menu")
const navMenu = document.querySelector(".nav_menu")

navToggle.addEventListener("click", () => {
    navMenu.classList.toggle("nav_menu_visual");
});
