let currentIndex = 0;
const slides = document.querySelectorAll(".carousel-item");
const intervalTime = 6000; // 6 seconds for each slide
let autoRotate; // Interval variable for auto-rotation

// Show the slide at the specified index
function showSlide(index) {
    if (index >= slides.length) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = slides.length - 1;
    } else {
        currentIndex = index;
    }

    document.querySelector(".carousel-list").style.transform = 
        `translateX(-${currentIndex * 100}%)`;
}

// Go to the next slide and reset auto-rotation
function nextSlide() {
    showSlide(currentIndex + 1);
    resetAutoRotate();
}

// Go to the previous slide and reset auto-rotation
function prevSlide() {
    showSlide(currentIndex - 1);
    resetAutoRotate();
}

// Automatically go to the next slide every interval
function startAutoRotate() {
    autoRotate = setInterval(nextSlide, intervalTime);
}

// Stop and restart the auto-rotation interval
function resetAutoRotate() {
    clearInterval(autoRotate);
    startAutoRotate();
}

// Start auto-rotation when the page loads
startAutoRotate();