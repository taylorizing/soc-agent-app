// File input handling
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const fileInputWrapper = document.querySelector('.file-input-wrapper');
const uploadForm = document.getElementById('uploadForm');
const uploadBtn = document.getElementById('uploadBtn');
const messageDiv = document.getElementById('message');
const refreshBtn = document.getElementById('refreshBtn');
const filesList = document.getElementById('filesList');

// Update file name display when file is selected
fileInput.addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        const file = this.files[0];
        const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
        fileName.textContent = `${file.name} (${sizeInMB} MB)`;
        fileInputWrapper.classList.add('has-file');
    } else {
        fileName.textContent = 'Choose a file or drag it here';
        fileInputWrapper.classList.remove('has-file');
    }
});

// Drag and drop handling
const fileInputLabel = document.querySelector('.file-input-label');

fileInputLabel.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    this.style.borderColor = '#667eea';
    this.style.background = '#f5f7ff';
});

fileInputLabel.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    if (!fileInputWrapper.classList.contains('has-file')) {
        this.style.borderColor = '#ddd';
        this.style.background = '#fafafa';
    }
});

fileInputLabel.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }
});

// Form submission
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!fileInput.files || !fileInput.files[0]) {
        showMessage('Please select a file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    // Show loading state
    setLoading(true);
    hideMessage();
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message, 'success');
            // Reset form
            uploadForm.reset();
            fileName.textContent = 'Choose a file or drag it here';
            fileInputWrapper.classList.remove('has-file');
            // Refresh file list
            await refreshFileList();
        } else {
            showMessage(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showMessage('Upload failed: ' + error.message, 'error');
    } finally {
        setLoading(false);
    }
});

// Refresh button handler
refreshBtn.addEventListener('click', async function() {
    refreshBtn.style.transform = 'rotate(360deg)';
    await refreshFileList();
    setTimeout(() => {
        refreshBtn.style.transform = '';
    }, 300);
});

// Helper functions
function setLoading(isLoading) {
    uploadBtn.disabled = isLoading;
    const btnText = uploadBtn.querySelector('.btn-text');
    const btnSpinner = uploadBtn.querySelector('.btn-spinner');
    
    if (isLoading) {
        btnText.textContent = 'Uploading...';
        btnSpinner.style.display = 'block';
    } else {
        btnText.textContent = 'Upload File';
        btnSpinner.style.display = 'none';
    }
}

function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }
}

function hideMessage() {
    messageDiv.style.display = 'none';
}

async function refreshFileList() {
    try {
        const response = await fetch('/files');
        const data = await response.json();
        
        if (data.success) {
            renderFileList(data.files);
        }
    } catch (error) {
        console.error('Failed to refresh file list:', error);
    }
}

function renderFileList(files) {
    if (!files || files.length === 0) {
        filesList.innerHTML = `
            <div class="empty-state">
                <p>No files uploaded yet</p>
            </div>
        `;
        return;
    }
    
    filesList.innerHTML = files.map(file => `
        <div class="file-item">
            <div class="file-icon">📄</div>
            <div class="file-info">
                <div class="file-name">${escapeHtml(file.name)}</div>
                <div class="file-meta">
                    <span>${(file.size / 1024).toFixed(2)} KB</span>
                    <span>•</span>
                    <span>${escapeHtml(file.modified)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-refresh file list every 30 seconds
setInterval(refreshFileList, 30000);

