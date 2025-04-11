# Tigris S3 Integration Guide

This guide explains how to set up and use Tigris Object Storage (S3 compatible) with your Django application using `django-storages` and `boto3`.

## Configuration

1. **Install required packages**:
   ```bash
   pip install boto3 django-storages python-dotenv
   ```
   *Note: `django-storages` should already be installed.* 

2. **Ensure `'storages'` is in `INSTALLED_APPS`** in `fspapplication_backend/fspapplication_backend/settings.py` (should already be present).

3. **Configure Tigris Credentials**: 
   - Open or create the `.env` file in the `fspapplication_backend` directory.
   - Add your Tigris S3 credentials and endpoint details:

   ```dotenv
   # TIGRIS Configuration
   TIGRIS_ACCESS_KEY_ID=your-actual-tigris-access-key-id
   TIGRIS_SECRET_ACCESS_KEY=your-actual-tigris-secret-access-key
   TIGRIS_STORAGE_BUCKET_NAME=your-actual-tigris-bucket-name
   TIGRIS_REGION_NAME=your-actual-tigris-region-name # (e.g., 'auto' or specific region if applicable)
   TIGRIS_ENDPOINT_URL_S3=your-tigris-s3-endpoint-url # (e.g., fly.storage.tigris.dev)
   TIGRIS_DEFAULT_ACL=private # Or 'public-read' if objects should be public by default
   ```

4. **Update Django Settings (`settings.py`)**: 
   Ensure your `fspapplication_backend/fspapplication_backend/settings.py` file loads these environment variables and configures `django-storages` correctly. Key settings include:

   ```python
   # Default file storage
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

   # Static files (if using Tigris for static assets)
   # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

   # TIGRIS S3 configuration using environment variables
   TIGRIS_ACCESS_KEY_ID = os.environ.get('TIGRIS_ACCESS_KEY_ID')
   TIGRIS_SECRET_ACCESS_KEY = os.environ.get('TIGRIS_SECRET_ACCESS_KEY')
   TIGRIS_STORAGE_BUCKET_NAME = os.environ.get('TIGRIS_STORAGE_BUCKET_NAME')
   TIGRIS_REGION_NAME = os.environ.get('TIGRIS_REGION_NAME')
   TIGRIS_ENDPOINT_URL_S3 = os.environ.get('TIGRIS_ENDPOINT_URL_S3') # Crucial for non-AWS S3
   TIGRIS_DEFAULT_ACL = os.environ.get('TIGRIS_DEFAULT_ACL', 'private')
   
   # These settings are used by django-storages/boto3, even if named AWS*
   AWS_ACCESS_KEY_ID = TIGRIS_ACCESS_KEY_ID 
   AWS_SECRET_ACCESS_KEY = TIGRIS_SECRET_ACCESS_KEY
   AWS_STORAGE_BUCKET_NAME = TIGRIS_STORAGE_BUCKET_NAME
   AWS_S3_REGION_NAME = TIGRIS_REGION_NAME
   AWS_S3_ENDPOINT_URL = TIGRIS_ENDPOINT_URL_S3 # IMPORTANT: Use the Tigris endpoint
   AWS_DEFAULT_ACL = TIGRIS_DEFAULT_ACL
   AWS_S3_ADDRESSING_STYLE = 'path' # Often needed for non-AWS S3
   # AWS_S3_SIGNATURE_VERSION = 's3v4' # Usually default, but specify if needed
   
   # Optional: Object parameters like Cache-Control
   AWS_S3_OBJECT_PARAMETERS = {
       'CacheControl': 'max-age=86400',
   }
   # You might also use TIGRIS_S3_OBJECT_PARAMETERS in your custom client if preferred
   # TIGRIS_S3_OBJECT_PARAMETERS = AWS_S3_OBJECT_PARAMETERS 
   ```
   *Note: `django-storages` often expects settings prefixed with `AWS_`. By setting these based on your `TIGRIS_` variables, you ensure compatibility.*

## Tigris Bucket Setup

1. **Create a bucket** in your Tigris project dashboard or via the Tigris CLI.
2. **Set up CORS**: Configure CORS settings for your bucket if your frontend needs to interact directly with the storage (e.g., for direct uploads or accessing files via browser JS). Allow origins like your frontend development and production URLs.
3. **Bucket Policy/Permissions**: Ensure the credentials you use have the necessary permissions (e.g., `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, `s3:ListBucket`, `s3:HeadBucket`).

## API Endpoints (`files` app)

The `files` app provides API endpoints for managing uploads:

* **Upload File**: `POST /files/upload/`
* **List Files**: `GET /files/list/`
* **Delete File**: `DELETE /files/delete/`
* **Get Download URL**: `GET /files/download/` (or `GET /files/download/<path:file_path>/`)
* **Diagnostics**: `GET /files/diagnostics/`

Refer to `fspapplication_backend/files/urls.py` and `fspapplication_backend/files/views.py` for details on request/response formats.

## `TigrisClient` Utility (`files/tigris_utils.py`)

This utility class provides a wrapper around `boto3` specifically configured for your Tigris setup. It handles:
* Initializing the `boto3` client with Tigris credentials and endpoint.
* Uploading, downloading (via presigned URLs), and deleting files.
* Generating presigned URLs for secure access.
* Constructing public URLs (use with caution).
* Checking required settings.

## Multi-tenancy Support

The `FileUploadView` automatically organizes files into tenant-specific paths within the bucket using the tenant's schema name (or a derived ID), ensuring data isolation (e.g., `<tenant_schema_name>/<file_type>/<module>/<filename>`).

## Example Usage in Vue Frontend

```typescript
import axios from 'axios'; // Assuming axios is configured with auth headers

// Example file upload component method
async function uploadFile(file: File, fileType: string = 'document', module: string = 'general') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);
  formData.append('module', module);
  
  try {
    // Use the correct API endpoint from your files app
    const response = await axios.post('/files/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        // Ensure Authorization header is included if using token auth
      }
    });
    
    if (response.data.success) {
        console.log('Upload successful:', response.data);
        return response.data; // Contains path, url, id
    } else {
        console.error('Upload failed:', response.data.error);
        throw new Error(response.data.error || 'Upload failed');
    }
  } catch (error: any) {
    console.error('Upload request failed:', error.response?.data || error.message);
    throw error;
  }
}

// Example to get a temporary download URL for a private file
async function getDownloadUrl(filePath: string, expirationSeconds: number = 3600) {
  try {
    // Use the correct API endpoint
    const response = await axios.get('/files/download/', {
        params: { 
            path: filePath, 
            expiration: expirationSeconds
        }
        // Ensure Authorization header is included
    });
    if (response.data.success) {
        console.log('Presigned URL:', response.data.url);
        return response.data.url;
    } else {
        console.error('Failed to get download URL:', response.data.error);
        throw new Error(response.data.error || 'Failed to get URL');
    }
  } catch (error: any) {
    console.error('Get download URL request failed:', error.response?.data || error.message);
    throw error;
  }
}
```

### Environment Variables

Create a `.env` file in the `fspapplication_backend` directory and add the following Tigris S3 credentials:

```dotenv
TIGRIS_ACCESS_KEY_ID=your-actual-tigris-access-key-id
TIGRIS_SECRET_ACCESS_KEY=your-actual-tigris-secret-access-key
TIGRIS_STORAGE_BUCKET_NAME=your-actual-tigris-bucket-name
TIGRIS_REGION_NAME=your-actual-tigris-region-name (e.g., auto)
TIGRIS_ENDPOINT_URL_S3=your-tigris-s3-endpoint-url (e.g., fly.storage.tigris.dev)
TIGRIS_DEFAULT_ACL=private  # or public-read if needed
```

### Django Settings (`settings.py`) 