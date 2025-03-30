# Amazon S3 Integration Guide

This guide explains how to set up and use Amazon S3 with your Django application.

## Configuration

1. **Install required packages**:
   ```bash
   pip install boto3 django-storages python-dotenv
   ```

2. **Add 'storages' to INSTALLED_APPS** in settings.py (already done).

3. **Set up your AWS credentials**:
   - Open the `.env` file at the project root
   - Add your actual AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your-actual-access-key-id
   AWS_SECRET_ACCESS_KEY=your-actual-secret-access-key
   AWS_STORAGE_BUCKET_NAME=your-actual-bucket-name
   AWS_S3_REGION_NAME=your-actual-region-name (e.g., us-east-1)
   AWS_DEFAULT_ACL=private  # or public-read if needed
   ```

## Bucket Setup

1. **Create an S3 bucket** in your AWS console
2. **Set up proper permissions** for your bucket:
   - Enable appropriate CORS settings if accessing directly from frontend
   - Set up bucket policy for access control

## API Endpoints

The following API endpoints are available for S3 operations:

### Upload File
- **URL**: `/common_utils/s3/upload/`
- **Method**: POST
- **Authentication**: Required
- **Form Data**:
  - `file`: The file to upload
  - `folder`: (Optional) Subfolder to store file in (default: 'uploads')
- **Response**: JSON with file path and name

### Get Download URL
- **URL**: `/common_utils/s3/download/<path:file_path>/`
- **Method**: GET
- **Authentication**: Required
- **URL Params**:
  - `expiration`: (Optional) URL expiration time in seconds (default: 3600)
- **Response**: JSON with presigned URL

### List Files
- **URL**: `/common_utils/s3/list/`
- **Method**: GET
- **Authentication**: Required
- **URL Params**:
  - `prefix`: (Optional) Folder prefix to filter files
- **Response**: JSON with list of files

### Delete File
- **URL**: `/common_utils/s3/delete/<path:file_path>/`
- **Method**: DELETE
- **Authentication**: Required
- **Response**: Success or error message

## Multi-tenancy Support

Files are automatically organized by tenant schema name to maintain isolation between tenants.

## Example Usage in Vue Frontend

```typescript
// Example file upload component method
async uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder', 'documents');
  
  try {
    const response = await axios.post('/common_utils/s3/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
}

// Example to get download URL
async getDownloadUrl(filePath: string) {
  try {
    const response = await axios.get(`/common_utils/s3/download/${filePath}/`);
    return response.data.url;
  } catch (error) {
    console.error('Failed to get download URL:', error);
    throw error;
  }
}
``` 