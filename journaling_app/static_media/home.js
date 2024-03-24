
// Function to determine current sections in the navbar
let navbarSections = document.querySelectorAll('#navbar .scrollable');
const navbarCurrentSections = () => {
    let position = window.scrollY + 200;
    navbarSections.forEach(navbarSection => {
        if (!navbarSection.hash) return;
        let section = document.querySelector(navbarSection.hash);
        if (!section) return;
        if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
            navbarSection.classList.add('current');
        } else {
            navbarSection.classList.remove('current');
        }
    });
};
window.addEventListener('load', navbarCurrentSections);
window.addEventListener('scroll', navbarCurrentSections);

// Function to scroll to different sections
const scrollable = (element) => {
    let header = document.querySelector('#header');
    let offset = header.offsetHeight;
    let elementPos = document.querySelector(element).offsetTop;

    if (!header.classList.contains('scrolled')) {
        offset -= 10;
    }

    window.scrollTo({ top: elementPos - offset, behavior: 'smooth' });
};

// Event listener for clicking on scrollable elements in the navbar
document.querySelectorAll('.scrollable').forEach(item => {
    item.addEventListener('click', function (e) {
        let hash = this.hash;
        if (document.querySelector(hash)) {
            e.preventDefault();

            let navbar = document.querySelector('#navbar');
            if (navbar.classList.contains('small-screen-navbar')) {
                navbar.classList.remove('small-screen-navbar');
                let navbarToggle = document.querySelector('.navbar-button');
                navbarToggle.classList.toggle('bi-list');
                navbarToggle.classList.toggle('bi-x');
            }
            scrollable(hash);
        }
    });
});

// Event listener to scroll to the section when the page is loaded and the URL has a hash
window.addEventListener('load', () => {
    if (window.location.hash && document.querySelector(window.location.hash)) {
        scrollable(window.location.hash);
    }
});

// Functionality related to the header scrolling behavior
let headerScroll = document.querySelector('#header');
if (headerScroll) {
    const scrolling = () => {
        if (window.scrollY > 100) {
            headerScroll.classList.add('scrolled');
        } else {
            headerScroll.classList.remove('scrolled');
        }
    };
    window.addEventListener('load', scrolling);
    window.addEventListener('scroll', scrolling);
}

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

// Event listener for toggling the navbar button between lines and cross icons
document.querySelector('.navbar-button').addEventListener('click', function (e) {
    document.querySelector('#navbar').classList.toggle('small-screen-navbar');
    this.classList.toggle('bi-list');
    this.classList.toggle('bi-x');
});

// Event listener for dropdown functionality in small-screen navbar
document.querySelectorAll('.navbar .dropdown > a').forEach(item => {
    item.addEventListener('click', function (e) {
        if (document.querySelector('#navbar').classList.contains('small-screen-navbar')) {
            e.preventDefault();
            this.nextElementSibling.classList.toggle('dropdown-current');
        }
    });
});

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
