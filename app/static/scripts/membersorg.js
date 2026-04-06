let formToSubmit = null;

function requestDelete(button) {
    console.log("Delete requested"); // Debug line
    // Find the form that contains this button
    formToSubmit = button.closest('form');
    // Show the modal using the ID from the HTML above
    const modal = document.getElementById('deleteConfirmModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteConfirmModal');
    if (modal) {
        modal.style.display = 'none';
    }
    formToSubmit = null;
}

// Ensure the DOM is loaded before attaching the event listener
document.addEventListener('DOMContentLoaded', function() {
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function() {
            if (formToSubmit) {
                console.log("Submitting form...");
                formToSubmit.submit();
            }
        });
    }
});

// Close modal if user clicks outside the white box
window.onclick = function(event) {
    const deleteModal = document.getElementById('deleteConfirmModal');
    const addModal = document.getElementById('addMemberModal');
    
    if (event.target == deleteModal) closeDeleteModal();
    if (event.target == addModal) addModal.style.display = "none";
}