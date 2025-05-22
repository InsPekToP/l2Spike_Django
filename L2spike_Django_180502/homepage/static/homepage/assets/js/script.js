//NAVBAR

'use strict';

const navbar = document.querySelector("[data-navbar]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");
const navbarToggler = document.querySelector("[data-nav-toggler]");

navbarToggler.addEventListener("click", function () {
    navbar.classList.toggle("active");
    this.classList.toggle("active");
});


for (let i= 0; i<navbarLinks.length; i++){
    navbarLinks[i].addEventListener("click", function(){
        navbar.classList.remove("active");
        navbarToggler.classList.remove("active");
    });
}



//SEARCH TOGGLE

const searchToglers = document.querySelectorAll("[data-search-toggler]");
const searchBox = document.querySelector("[data-search-box]");

for (let i = 0; i<searchToglers.length; i++){
    searchToglers[i].addEventListener("click", function(){
        searchBox.classList.toggle("active");
    });
}



// HEADER end BACK TO TOP

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function() {
    if (window.scrollY >= 400){
        header.classList.add("active");
        backTopBtn.classList.add("active");
    }else{
        header.classList.remove("active");
        backTopBtn.classList.remove("active");
    }
});



document.addEventListener('DOMContentLoaded', () => {
    const playButton = document.getElementById('playButton');
    if (!playButton) return; // Если кнопки нет — прерываем выполнение скрипта

    playButton.addEventListener('click', function () {
        const videoWrapper = document.getElementById('videoWrapper');

        // Вставляем iframe с автозапуском
        videoWrapper.innerHTML = `
            <iframe width="100%" height="100%"
                src="https://www.youtube.com/embed/Mr3ywMTaqoU?autoplay=1&rel=0&showinfo=0"
                frameborder="0" 
                allow="autoplay; encrypted-media" 
                allowfullscreen
                class="img-cover">
            </iframe>
        `;
    });
});



// ABOUT

document.querySelectorAll('.accordion-button').forEach(button => {
    button.addEventListener('click', () => {
        const accordionBody = button.nextElementSibling;

        document.querySelectorAll('.accordion-body').forEach(body => {
            if (body !== accordionBody) {
                body.classList.remove('show');
            }
        });

        document.querySelectorAll('.accordion-button').forEach(btn => {
            if (btn !== button) {
                btn.classList.remove('active');
            }
        });

        accordionBody.classList.toggle('show');
        button.classList.toggle('active');
    });
});