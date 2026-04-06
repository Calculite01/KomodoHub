function toggleForm() {
    const formArea = document.getElementById('create-area');
    if (formArea.style.display === 'none' || formArea.style.display === '') {
        formArea.style.display = 'block';
        formArea.scrollIntoView({ behavior: 'smooth' });
    } else {
        formArea.style.display = 'none';
    }
}

// 2. Image Preview Logic for the "Create" Form
function previewImages() {
    const previewContainer = document.getElementById('image-preview-container');
    const fileInput = document.getElementById('image-upload'); // Ensure ID matches your form
    
    if (!previewContainer) return;

    previewContainer.innerHTML = ''; // Clear previous previews

    if (fileInput.files) {
        Array.from(fileInput.files).forEach(file => {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const wrapper = document.createElement('div');
                wrapper.className = 'image-wrapper';
                
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '8px';
                
                wrapper.appendChild(img);
                previewContainer.appendChild(wrapper);
            }
            
            reader.readAsDataURL(file);
        });
    }
}

// 3. Delete Confirmation Modal Logic
function openDeleteModal(deleteUrl) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('confirmDeleteForm');
    
    if (modal && form) {
        form.action = deleteUrl; // Update form action to the specific activity ID
        modal.style.display = 'flex'; // Show modal using flex for centering
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    }
}

// 4. Global Click Listener (Close modal if clicking outside the box)
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeDeleteModal();
    }
};

// 5. Escape Key Listener (Close modal on 'Esc')
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeDeleteModal();
    }
});

function previewDocuments() {
    const container = document.getElementById('doc-preview-container');
    const fileInput = document.getElementById('doc-upload');
    if (!container || !fileInput.files) return;

    container.innerHTML = ''; 
    Array.from(fileInput.files).forEach(file => {
        const docNameTag = document.createElement('div');
        docNameTag.style = "background: #f1f5f9; padding: 5px 12px; border-radius: 4px; font-size: 0.85rem; color: #475569; border: 1px solid #e2e8f0; display: inline-block; margin-right: 5px; margin-bottom: 5px;";
        docNameTag.innerHTML = `<i class="fa-solid fa-file-lines"></i> ${file.name}`;
        container.appendChild(docNameTag);
    });
}

// Toggle the creation form visibility
function toggleForm() {
    const el = document.getElementById('create-area');
    if (el) {
        el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
    }
}

// Open Delete Modal and set form action
function openDeleteModal(url) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('confirmDeleteForm');
    if (modal && form) {
        form.action = url;
        modal.style.display = 'flex';
    }
}

// Close Delete Modal
function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Handle Image Previews
function previewImages() {
    const container = document.getElementById('image-preview-container');
    const input = document.getElementById('image-upload');
    if (!container || !input) return;

    container.innerHTML = '';
    if (input.files) {
        Array.from(input.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'preview-thumbnail';
                container.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }
}

// Close modal when clicking outside content
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeDeleteModal();
    }
};

function previewImages() {
    const container = document.getElementById('image-preview-container');
    const input = document.getElementById('image-upload');
    if (!container || !input) return;

    container.innerHTML = '';
    if (input.files) {
        Array.from(input.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                // Match the style of the gallery thumbnails
                img.style = "width: 70px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;";
                container.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }
}