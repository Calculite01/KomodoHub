const createTask = document.getElementById("createtask");
const createTaskButton = document.getElementById("createTaskButton");
const closeTaskButton = document.getElementById("closeTaskButton");
createTask.style.display = "none";

createTaskButton.onclick = function(){
    console.log("test");
    createTask.style.display = "flex";
}

closeTaskButton.onclick = function() {
    // 1. Hide the modal
    createTask.style.display = "none";
    
    // 2. Find and reset the form fields
    const form = createTask.querySelector('form');
    if (form) {
        form.reset();
    }

    // 3. Clear all custom error messages
    const errorMessages = document.querySelectorAll('.error-text');
    errorMessages.forEach(error => {
        error.textContent = ''; // Remove the red text
    });

    // 4. Remove the red border/background from inputs
    const invalidInputs = document.querySelectorAll('.form-control.is-invalid');
    invalidInputs.forEach(input => {
        input.classList.remove('is-invalid');
    });

    // 5. Clear the image and file previews
    document.getElementById('image-preview-container').innerHTML = '';
    document.getElementById('doc-preview-container').innerHTML = '';

    console.log("Form fully reset and errors cleared.");
};

// Image Preview Logic
document.getElementById('image-input').addEventListener('change', function(event) {
    const container = document.getElementById('image-preview-container');
    container.innerHTML = ''; // Clear previous previews
    
    const files = event.target.files;
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgWrapper = document.createElement('div');
                imgWrapper.className = 'img-preview-wrapper';
                imgWrapper.innerHTML = `<img src="${e.target.result}" alt="preview">`;
                container.appendChild(imgWrapper);
            };
            reader.readAsDataURL(file);
        }
    });
});

// Document List Logic
document.getElementById('doc-input').addEventListener('change', function(event) {
    const container = document.getElementById('doc-preview-container');
    container.innerHTML = '';
    
    Array.from(event.target.files).forEach(file => {
        const docItem = document.createElement('div');
        docItem.className = 'doc-preview-item';
        docItem.innerHTML = `<i class="fa-solid fa-file-pdf"></i> <span>${file.name}</span>`;
        container.appendChild(docItem);
    });
});

const materialForm = document.querySelector('#createtask form');

materialForm.onsubmit = function(e) {
    let isValid = true;

    // Reset all previous errors
    document.querySelectorAll('.error-text').forEach(el => el.textContent = '');
    document.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));

    // 1. Title Validation
    const titleInput = document.getElementById('title-input');
    if (titleInput.value.trim() === "") {
        showError('title-error', 'Title is required.', titleInput);
        isValid = false;
    }

    // 2. Image Extension Validation
    const imageInput = document.getElementById('image-input');
    const validImageTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif'];
    if (imageInput.files.length > 0) {
        for (let file of imageInput.files) {
            if (!validImageTypes.includes(file.type)) {
                showError('image-error', `"${file.name}" is not a valid image.`, imageInput);
                isValid = false;
                break;
            }
        }
    }

    // 3. Document Extension Validation
    const docInput = document.getElementById('doc-input');
    const allowedDocExts = ['.pdf', '.docx', '.txt', '.zip'];
    if (docInput.files.length > 0) {
        for (let file of docInput.files) {
            const fileName = file.name.toLowerCase();
            const isExtValid = allowedDocExts.some(ext => fileName.endsWith(ext));
            if (!isExtValid) {
                showError('doc-error', `"${file.name}" is an unsupported file type.`, docInput);
                isValid = false;
                break;
            }
        }
    }

    if (!isValid) {
        e.preventDefault(); // Stop submission
    }
};

function showError(elementId, message, inputElement) {
    const errorSpan = document.getElementById(elementId);
    errorSpan.textContent = message;
    inputElement.classList.add('is-invalid');
}

let formToSubmit = null;

function openDeleteModal(formId) {
    formToSubmit = document.getElementById(formId);
    document.getElementById('delete-modal').style.display = 'flex';
}

function closeDeleteModal() {
    document.getElementById('delete-modal').style.display = 'none';
    formToSubmit = null;
}

function confirmDelete() {
    if (formToSubmit) {
        formToSubmit.submit();
    }
}

// Close if clicking outside the white box
window.onclick = function(event) {
    const modal = document.getElementById('delete-modal');
    if (event.target == modal) {
        closeDeleteModal();
    }
}