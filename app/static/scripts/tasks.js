document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggle-form-btn');
    const cancelBtn = document.getElementById('cancel-form-btn');
    const formSection = document.getElementById('create-task-section');

    // Show Form
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            formSection.classList.remove('hidden');
            toggleBtn.style.display = 'none';
        });
    }

    // Hide Form
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            formSection.classList.add('hidden');
            toggleBtn.style.display = 'block';
        });
    }

    // Optional: Add "Click to Complete" sound or effect
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateX(5px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateX(0)';
        });
    });
});