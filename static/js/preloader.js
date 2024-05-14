window.addEventListener('load', () => {
    const preloader = document.querySelector('.preloader');
    const MIN_DISPLAY_TIME = 4000; // Mínimo tiempo de visualización en milisegundos

    // Comprueba si el preloader ya se ha mostrado en esta sesión
    if (!sessionStorage.getItem('preloaderShown')) {
        // Muestra el preloader durante un mínimo de tiempo
        setTimeout(() => {
            preloader.classList.add('preloader-hidden');
            preloader.parentNode.removeChild(preloader);
            sessionStorage.setItem('preloaderShown', 'true');
        }, MIN_DISPLAY_TIME);
    } else {
        // Si el preloader ya se ha mostrado en esta sesión, ocúltalo inmediatamente
        preloader.classList.add('preloader-hidden');
        preloader.parentNode.removeChild(preloader);
    }
});