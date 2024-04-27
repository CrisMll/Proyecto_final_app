//Componente creado para la aparicion del mensaje como un popup

const add_recipe = false;
const remove_recipe = false;

function popup(message) {
    const popup = document.getElementById("popup");
    popup.textContent = message;
    popup.style.display = "block";

    setTimeout(() => {
        popup.style.display = "none";
    }, 2000);
}

if (add_recipe === true) {
    window.onload = function () {
        const flashMessage = "¡Receta añadida!";
        if (flashMessage.length > 0) {
        popup(flashMessage);
        }
    };
}

if (remove_recipe === true) {
    window.onload = function () {
        const flashMessage = "¡Receta eliminada!";
        if (flashMessage.length > 0) {
        popup(flashMessage);
        }
    };
}