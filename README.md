# SOC Agent App - File Upload to Unity Catalog

A Flask-based Databricks app that provides a web interface for uploading files to Unity Catalog volumes.

## Features

- 📁 **File Upload Interface** - Modern, intuitive drag-and-drop file upload
- 🔒 **File Type Validation** - Supports common file types (documents, images, data files)
- 📊 **File Management** - View all uploaded files with metadata (size, upload time)
- 💾 **Unity Catalog Integration** - Files are stored directly in Unity Catalog volumes
- ✅ **Real-time Updates** - Auto-refresh file list every 30 seconds
- 🎨 **Beautiful UI** - Modern, responsive design

## Target Volume

Files are uploaded to: `/Volumes/users/jason_taylor/agent_app_uploads`

## Supported File Types

- Documents: txt, pdf, doc, docx
- Spreadsheets: xls, xlsx, csv
- Images: png, jpg, jpeg, gif
- Data: json, xml
- Archives: zip

Maximum file size: 16 MB

## Local Development

### Prerequisites

- Python 3.8 or higher
- Access to Databricks workspace

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:8080
```

## Deployment to Databricks

### Using Databricks CLI

1. Ensure you have the Databricks CLI installed and configured:
```bash
databricks auth login --host https://e2-demo-west.cloud.databricks.com
```

2. Deploy the app bundle:
```bash
databricks bundle deploy
```

3. Access your app through the Databricks workspace UI under "Apps"

### Manual Deployment

1. Create a Unity Catalog volume (if not exists):
```sql
CREATE VOLUME IF NOT EXISTS users.jason_taylor.agent_app_uploads;
```

2. Upload all files to Databricks workspace
3. Configure as a Databricks App in your workspace

## Project Structure

```
soc-agent-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── databricks.yml        # Databricks bundle configuration
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Client-side logic
└── README.md             # This file
```

## API Endpoints

### `GET /`
Main page with upload interface

### `POST /upload`
Upload a file to Unity Catalog volume
- **Body**: multipart/form-data with 'file' field
- **Response**: JSON with success status and file details

### `GET /files`
List all uploaded files
- **Response**: JSON array of file objects with name, size, and modified date

### `GET /health`
Health check endpoint
- **Response**: JSON with app status and volume accessibility

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask sessions (default: 'dev-secret-key-change-in-production')

## Security Considerations

- File types are validated against an allowlist
- Filenames are sanitized using `secure_filename()`
- Duplicate filenames are automatically renamed with timestamps
- Maximum file size is enforced (16 MB)

## Troubleshooting

### Volume Access Issues

If you encounter permission errors accessing the Unity Catalog volume:

1. Verify the volume exists:
```sql
SHOW VOLUMES IN users.jason_taylor;
```

2. Check volume permissions:
```sql
SHOW GRANTS ON VOLUME users.jason_taylor.agent_app_uploads;
```

3. Grant necessary permissions if needed:
```sql
GRANT WRITE FILES ON VOLUME users.jason_taylor.agent_app_uploads TO `<principal>`;
```

### File Upload Failures

- Ensure file size is under 16 MB
- Verify file type is in the allowed extensions list
- Check that the Unity Catalog volume path is accessible

## License

MIT License

