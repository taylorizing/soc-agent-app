import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import traceback
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_VOLUME_PATH = '/Volumes/users/jason_taylor/agent_app_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'json', 'xml', 'zip'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_volume_directory():
    """Ensure the upload directory exists"""
    try:
        if not os.path.exists(UPLOAD_VOLUME_PATH):
            os.makedirs(UPLOAD_VOLUME_PATH, exist_ok=True)
        return True, "Directory ready"
    except Exception as e:
        return False, str(e)

def get_uploaded_files():
    """Get list of uploaded files from the volume"""
    try:
        if not os.path.exists(UPLOAD_VOLUME_PATH):
            return []
        
        files = []
        for filename in os.listdir(UPLOAD_VOLUME_PATH):
            filepath = os.path.join(UPLOAD_VOLUME_PATH, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return []

@app.route('/')
def index():
    """Main page with file upload form"""
    uploaded_files = get_uploaded_files()
    return render_template('index.html', 
                          upload_path=UPLOAD_VOLUME_PATH,
                          uploaded_files=uploaded_files,
                          allowed_extensions=', '.join(sorted(ALLOWED_EXTENSIONS)))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        # Check if file part exists
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({
                'success': False, 
                'error': f'File type not allowed. Allowed types: {", ".join(sorted(ALLOWED_EXTENSIONS))}'
            }), 400
        
        # Ensure volume directory exists
        success, message = ensure_volume_directory()
        if not success:
            return jsonify({
                'success': False, 
                'error': f'Failed to access volume directory: {message}'
            }), 500
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Add timestamp if file already exists
        filepath = os.path.join(UPLOAD_VOLUME_PATH, filename)
        if os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            filepath = os.path.join(UPLOAD_VOLUME_PATH, filename)
        
        # Save the file
        file.save(filepath)
        
        return jsonify({
            'success': True, 
            'message': f'File "{filename}" uploaded successfully',
            'filename': filename,
            'path': filepath
        }), 200
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Upload error: {error_trace}")
        return jsonify({
            'success': False, 
            'error': f'Upload failed: {str(e)}'
        }), 500

@app.route('/files')
def list_files():
    """API endpoint to list uploaded files"""
    try:
        files = get_uploaded_files()
        return jsonify({'success': True, 'files': files}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        success, message = ensure_volume_directory()
        return jsonify({
            'status': 'healthy' if success else 'degraded',
            'volume_path': UPLOAD_VOLUME_PATH,
            'volume_accessible': success,
            'message': message
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# if __name__ == '__main__':
#     # This is for local development only
#     # In Databricks, the app will be run by the platform
#     app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    flask_app.run(debug=True)

