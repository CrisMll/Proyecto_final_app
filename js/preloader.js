window.addEventListener('load', () => {
    const preloader = document.querySelector('.preloader');
    const MIN_DISPLAY_TIME = 3000; 

    
    if (!sessionStorage.getItem('preloaderShown')) {
        
        setTimeout(() => {
            preloader.classList.add('preloader-hidden');
            preloader.parentNode.removeChild(preloader);
            sessionStorage.setItem('preloaderShown', 'true');
        }, MIN_DISPLAY_TIME);
    } else {
        
        preloader.classList.add('preloader-hidden');
        preloader.parentNode.removeChild(preloader);
    }
});