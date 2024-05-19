
//? Función para el botón de volver en la sección
function goBack() {
    window.history.back();
}

//? Funcion para copiar el email de la sección de contacto

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

let isClicked = false;

function copyEmail() {
    let url = document.getElementById('emailLink');
    let button = document.getElementById('copyEmail');
    navigator.clipboard.writeText(url.innerText);

    // Control del tooltip y el mensaje
    let tooltip = bootstrap.Tooltip.getInstance(button);
    tooltip.hide();
    button.setAttribute('data-bs-original-title', 'Email copiado');
    tooltip = new bootstrap.Tooltip(button); // 
    tooltip.show();

    isClicked = true;
}
document.getElementById('copyEmail').addEventListener('click', copyEmail);

document.getElementById('copyEmail').addEventListener('mouseout', function () {
    if (isClicked) {
        let button = document.getElementById('copyEmail');
        let tooltip = bootstrap.Tooltip.getInstance(button);
        tooltip.hide();
        button.setAttribute('data-bs-original-title', 'Click para copiar');
        tooltip = new bootstrap.Tooltip(button);

        isClicked = false;
    }
});


//? Manejo del interruptor del modo oscuro permanente en la sesion

function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark');
    
    if (body.classList.contains('dark')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

//? Cargar el estado del modo oscuro cuando se carga la página
document.addEventListener('DOMContentLoaded', (event) => {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark');
        document.getElementById('dark-mode-toggle').checked = true;
    } else {
        document.body.classList.remove('dark');
        document.getElementById('dark-mode-toggle').checked = false;
    }
});



//? Boton volver arriba

document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("back-to-top");

    window.addEventListener("scroll", function() {
        if (window.scrollY > 10) { 
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    });

    btn.addEventListener("click", function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth' 
        });
    });
});
