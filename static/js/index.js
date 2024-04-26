// index.js

let slideIndex = 0;

function showSlides() {
    const slides = document.querySelectorAll('.carousel-item');
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    slides[slideIndex - 1].style.display = "flex";
    setTimeout(showSlides, 3000);
}

function prevSlide() {
    const slides = document.querySelectorAll('.carousel-item');
    if (slideIndex === 1) {
        slideIndex = slides.length;
    } else {
        slideIndex--;
    }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "flex";
}

function nextSlide() {
    const slides = document.querySelectorAll('.carousel-item');
    if (slideIndex === slides.length) {
        slideIndex = 1;
    } else {
        slideIndex++;
    }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "flex";
}

showSlides();

function f() {
    document.getElementsByClassName('dropdown')[0].classList.toggle('down');
    document.getElementsByClassName('arrow')[0].classList.toggle('gone');
    if (document.getElementsByClassName('dropdown')[0].classList.contains('down')) {
      setTimeout(function() {
        document.getElementsByClassName('dropdown')[0].style.overflow = 'visible'
      }, 500)
    } else {
      document.getElementsByClassName('dropdown')[0].style.overflow = 'hidden'
    }
  }


