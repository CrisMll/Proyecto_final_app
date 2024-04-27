//Componente creado para la aparicion del mensaje como un popup

function popup(message) {
    const popup = document.getElementById("popup");
    popup.textContent = message;
    popup.style.display = "block";

    setTimeout(() => {
        popup.style.display = "none";
    }, 2000);
}

window.onload = function() {
    const flashMessage = "¡Receta añadida!";
    if (flashMessage.length > 0) {
        popup(flashMessage);
    }
};

