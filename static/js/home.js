// Functionality related to the return button that jumps to the top of the page
let returnButton = document.querySelector('.return-button');
if (returnButton) {
    const toggleReturnButton = () => {
        if (window.scrollY > 100) {
            returnButton.classList.add('current');
        } else {
            returnButton.classList.remove('current');
        }
    };
    window.addEventListener('load', toggleReturnButton);
    window.addEventListener('scroll', toggleReturnButton);
}

// Initialization of AOS (Animate On Scroll) library for scroll animations
function aos_init() {
    AOS.init({
        duration: 750,
        easing: "ease-in-out",
        once: true
    });
}
window.addEventListener('load', () => {
    aos_init();
});
