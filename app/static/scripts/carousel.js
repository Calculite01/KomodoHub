document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('track');
    const images = document.querySelectorAll('.carousel-track img');

    let current = 0;
    const total = images.length;

    function updateSlide() {
        track.style.transform = `translateX(-${current * 100}%)`;
    }

    document.getElementById('next').addEventListener('click', () => {
        current = (current + 1) % total;
        updateSlide();
    });

    document.getElementById('prev').addEventListener('click', () => {
        current = (current - 1 + total) % total;
        updateSlide();
    });

    setInterval(() => {
        current = (current + 1) % total;
        updateSlide();
    }, 4000);
});