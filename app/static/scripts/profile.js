document.addEventListener('DOMContentLoaded', function() {
    const cameraBtn = document.getElementById('camera-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const uploadForm = document.getElementById('upload-form-container');
    const fileBtn = document.getElementById('actual-file-btn');
    const fileChosen = document.getElementById('file-chosen');

    // Show form when camera icon is clicked
    cameraBtn.addEventListener('click', () => {
        uploadForm.style.display = 'block';
    });

    // Hide form when cancel is clicked
    cancelBtn.addEventListener('click', () => {
        uploadForm.style.display = 'none';
    });

    // Update text when a file is selected
    fileBtn.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            fileChosen.textContent = this.files[0].name;
        } else {
            fileChosen.textContent = "No file chosen";
        }
    });
});