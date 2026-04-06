document.addEventListener('DOMContentLoaded', function() {
    // Auto-scroll chat to bottom on load
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Optional: Confirm before posting a grade
    const gradeForm = document.querySelector('.grade-section form');
    if (gradeForm) {
        gradeForm.addEventListener('submit', function(e) {
            const gradeVal = document.querySelector('input[name="grade"]').value;
            if (!confirm(`Are you sure you want to finalize the grade at ${gradeVal}%?`)) {
                e.preventDefault();
            }
        });
    }
});