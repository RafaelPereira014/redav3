let currentIndex = 0;
const intervalTime = 10000; // 10 seconds
let isFirstMove = true;

function moveSlide(direction) {
    const slides = document.querySelectorAll('.carousel-item');
    const totalSlides = slides.length;

    currentIndex = (currentIndex + direction + totalSlides) % totalSlides;

    // Adjusting offset calculation for leftward slide
    const offset = -currentIndex * 100;
    const moveDirection = direction === -1 ? 'right' : 'left'; // Determine the direction of movement

    if (!isFirstMove) {
        document.querySelector('.carousel-inner').style.transition = `transform 0.5s ease-in-out ${moveDirection}`;
    } else {
        isFirstMove = false;
    }

    document.querySelector('.carousel-inner').style.transform = `translateX(${offset}%)`;
}

function startCarousel() {
    setInterval(() => {
        moveSlide(1);
    }, intervalTime);
}

startCarousel();