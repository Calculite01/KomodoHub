function previewImages() {
    const previewContainer = document.getElementById('image-preview-container');
    const files = document.getElementById('image-upload').files;
    
    // Clear existing previews
    previewContainer.innerHTML = '';

    if (files) {
        [].forEach.call(files, readAndPreview);
    }

    function readAndPreview(file) {
        // Make sure it's an image
        if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
            return;
        }
        
        const reader = new FileReader();
        
        reader.addEventListener("load", function() {
            const div = document.createElement('div');
            div.className = 'preview-item';
            
            div.innerHTML = `
                <img src="${this.result}" title="${file.name}">
                <div class="remove-preview" onclick="clearInput()">×</div>
            `;
            
            previewContainer.appendChild(div);
        }, false);
        
        reader.readAsDataURL(file);
    }
}

// Simple function to clear if they change their mind
function clearInput() {
    document.getElementById('image-upload').value = '';
    document.getElementById('image-preview-container').innerHTML = '';
}

function openDeleteModal(deleteUrl) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('confirmDeleteForm');
    
    form.action = deleteUrl; // Set the form action to the specific message ID
    modal.style.display = 'flex'; // Show the modal
}

function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

// Close modal if user clicks outside the content box
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target == modal) {
        closeDeleteModal();
    }
}