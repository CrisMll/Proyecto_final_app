
//? Utilidades
//Función para el botón de volver en la sección
function goBack() {
    window.history.back();
}

// Funcion para copiar el email de la sección de contacto

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


const copyEmailButton = document.getElementById('copyEmail');

if (copyEmailButton) {
    copyEmailButton.addEventListener('click', copyEmail);
    copyEmailButton.addEventListener('mouseout', function () {
        if (isClicked) {
            let button = document.getElementById('copyEmail');
            let tooltip = bootstrap.Tooltip.getInstance(button);
            tooltip.hide();
            button.setAttribute('data-bs-original-title', 'Click para copiar');
            tooltip = new bootstrap.Tooltip(button);

            isClicked = false;
        }
    });
}

// Boton volver arriba

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

//? Funciones de cookies modo oscuro

// Manejo del interruptor del modo oscuro permanente en la sesion, modo large y modo movil
function setCookie(cookieName, cookieValue, daysToExpire) {
    const currentDate = new Date();
    currentDate.setTime(currentDate.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
    const expires = "expires=" + currentDate.toUTCString();
    document.cookie = `${cookieName}=${cookieValue};${expires};path=/`;
}

function getCookie(cookieName) {
    const nameEquals = cookieName + "=";
    const allCookies = document.cookie.split(';');
    for (let cookie of allCookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(nameEquals)) {
            return cookie.substring(nameEquals.length);
        }
    }
    return null;
}

function deleteCookie(cookieName) {
    document.cookie = `${cookieName}=; Max-Age=-99999999;path=/`;
}

function applyDarkMode() {
    document.body.classList.add('dark');
    document.getElementById('darkModeToggleLg').checked = true;
    document.getElementById('darkModeToggleSm').checked = true;
}

function removeDarkMode() {
    document.body.classList.remove('dark');
    document.getElementById('darkModeToggleLg').checked = false;
    document.getElementById('darkModeToggleSm').checked = false;
}

function checkDarkMode() {
    console.log("checkDarkMode function is executing");
    const darkModeEnabled = getCookie('darkMode');
    if (darkModeEnabled === 'enabled') {
        applyDarkMode();
    } else {
        removeDarkMode();
    }
}

function toggleDarkMode() {
    console.log("toggleDarkMode function is executing");
    const darkModeEnabled = getCookie('darkMode');
    if (darkModeEnabled === 'enabled') {
        setCookie('darkMode', 'disabled', 7);
        removeDarkMode();
    } else {
        setCookie('darkMode', 'enabled', 7);
        applyDarkMode();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOMContentLoaded event is firing");
    document.getElementById('darkModeToggleLg').addEventListener('change', toggleDarkMode);
    document.getElementById('darkModeToggleSm').addEventListener('change', toggleDarkMode);
    checkDarkMode();
});