import apiClient from './api';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';
// Read the Tigris public domain from environment variables
const TIGRIS_PUBLIC_DOMAIN = import.meta.env.VITE_TIGRIS_PUBLIC_DOMAIN || '';

export interface FileUploadResponse {
  success: boolean;
  path?: string;        // The object key/path in the bucket
  url?: string;         // Presigned URL for temporary access
  fileUrl?: string;     // Potentially direct URL (if public), may differ from display URL
  id?: number;          // DB record ID
  error?: string;
  // Add fields returned by FileUploadSerializer
  originalFilename?: string;
  fileType?: string;
  module?: string;
  contentType?: string;
  fileSize?: number;
  createdBy?: number;
  createdAt?: string;
  filename?: string; // Base filename derived from path
}

export interface FileListItem {
  // Based on FileUploadSerializer fields
  id: number;
  path: string;
  originalFilename: string;
  fileType: string;
  module: string;
  contentType: string | null;
  fileSize: number;
  createdBy: number | null;
  createdAt: string;
  url: string | null; // Presigned URL
  filename: string | null;
  fileUrl: string | null; // Direct/Public URL from backend
}

export interface FileDownloadResponse {
  success: boolean;
  url?: string; // This will be the presigned URL from the backend
  error?: string;
}

// Interface for image resize options
export interface ImageResizeOptions {
  maxWidth?: number;
  maxHeight?: number;
  quality?: number; // 0 to 1 (e.g., 0.85 for 85% quality)
  outputFormat?: 'image/jpeg' | 'image/png' | 'image/webp'; // Specify output format
}

export const fileService = {
  /**
   * Resizes an image client-side before upload.
   * Helps reduce upload size and server processing.
   * 
   * @param file The original image file.
   * @param options Resize options (maxWidth, maxHeight, quality, outputFormat).
   * @returns Promise resolving to the resized File object.
   */
  async resizeImage(file: File, options: ImageResizeOptions = {}): Promise<File> {
    if (!file.type.startsWith('image/')) {
      console.warn('Attempted to resize a non-image file. Returning original.');
      return file;
    }

    const maxWidth = options.maxWidth || 800; // Default max width
    const maxHeight = options.maxHeight || 800; // Default max height
    const quality = options.quality !== undefined ? options.quality : 0.85; // Default quality

    // Default to JPEG unless PNG is specified or original is PNG (to preserve transparency)
    const outputFormat = options.outputFormat || (file.type === 'image/png' ? 'image/png' : 'image/jpeg');

    return new Promise((resolve, reject) => {
      const img = new Image();
      const objectUrl = URL.createObjectURL(file);
      img.src = objectUrl;

      img.onload = () => {
        URL.revokeObjectURL(objectUrl); // Clean up object URL

        let { width, height } = img;
        const aspectRatio = width / height;

        // Calculate new dimensions maintaining aspect ratio
        if (width > maxWidth) {
          width = maxWidth;
          height = width / aspectRatio;
        }
        if (height > maxHeight) {
          height = maxHeight;
          width = height * aspectRatio;
        }

        // Round dimensions to whole pixels
        width = Math.round(width);
        height = Math.round(height);

        // Optimization: If the image is already small enough and format matches, return original
        if (img.width <= width && img.height <= height && file.type === outputFormat) {
          console.log('Image is already within target dimensions and format. Skipping resize.');
          resolve(file);
          return;
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        if (!ctx) {
          reject(new Error('Failed to get 2D context from canvas'));
          return;
        }

        // Draw image onto canvas (resizing occurs here)
        ctx.drawImage(img, 0, 0, width, height);

        // Convert canvas to blob with specified format and quality
        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error('Canvas to Blob conversion failed'));
              return;
            }
            // Create a new File object from the blob
            const resizedFile = new File([blob], file.name, {
              type: outputFormat,
              lastModified: Date.now(),
            });

            console.log(
              `Resized image from ${this.formatFileSize(file.size)} ` +
              `to ${this.formatFileSize(resizedFile.size)} ` +
              `(Format: ${outputFormat}, Quality: ${quality})`
            );
            resolve(resizedFile);
          },
          outputFormat,
          quality
        );
      };

      img.onerror = (error) => {
        URL.revokeObjectURL(objectUrl);
        console.error('Error loading image for resizing:', error);
        reject(new Error('Image loading failed'));
      };
    });
  },

  /**
   * Formats file size in bytes to a human-readable string (KB, MB, GB).
   * 
   * @param bytes File size in bytes.
   * @returns Formatted file size string.
   */
  formatFileSize(bytes: number): string {
    if (bytes < 0) return 'Invalid size';
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']; // Added TB
    const i = Math.max(0, Math.floor(Math.log(bytes) / Math.log(k)));
    // Ensure we don't exceed the sizes array bounds
    const unitIndex = Math.min(i, sizes.length - 1); 
    // Use toFixed(1) for KB and above for better readability
    const precision = unitIndex === 0 ? 0 : 1; 
    return `${parseFloat((bytes / Math.pow(k, unitIndex)).toFixed(precision))} ${sizes[unitIndex]}`;
  },

  /**
   * Uploads a file to the backend API.
   * Optionally resizes images before uploading.
   * 
   * @param file The File object to upload.
   * @param fileType Category for the file (e.g., 'images', 'documents').
   * @param module Module the file belongs to (e.g., 'avatars', 'invoices').
   * @param resizeOptions Options for resizing if the file is an image. Pass `null` to disable resizing.
   * @returns Promise resolving to the FileUploadResponse from the backend.
   */
  async uploadFile(
    file: File,
    fileType: string,
    module: string,
    resizeOptions?: ImageResizeOptions | null // Allow null to explicitly disable resize
  ): Promise<FileUploadResponse> {
    let fileToUpload = file;

    // Resize image if it's an image and resizeOptions are provided (not null)
    if (file.type.startsWith('image/') && resizeOptions !== null) {
      try {
        console.log('Attempting to resize image before upload...');
        fileToUpload = await this.resizeImage(file, resizeOptions || undefined);
      } catch (resizeError) {
        console.error('Image resizing failed, uploading original file:', resizeError);
        // Fallback to uploading the original file if resizing fails
      }
    }

    const formData = new FormData();
    formData.append('file', fileToUpload, file.name); // Use original filename
    formData.append('file_type', fileType);
    formData.append('module', module);
    // Removed 'use_chunked_upload' as it seemed unused in backend

    console.log(`Uploading file: ${fileToUpload.name}, Type: ${fileType}, Module: ${module}, Size: ${this.formatFileSize(fileToUpload.size)}`);

    try {
      // Use the generic apiClient for the request
      const response = await apiClient.post<FileUploadResponse>(`${API_URL}/files/upload/`, formData, {
        headers: {
          // Content-Type is automatically set by browser for FormData
          // 'Content-Type': 'multipart/form-data', 
        },
        // Ensure credentials (like cookies or auth tokens) are sent if needed by the backend
        withCredentials: true, 
      });
      
      console.log('Upload API response received:', response.data);
      // Convert keys before returning
      return convertObjectKeysToCamel(response.data) as FileUploadResponse;

    } catch (error: unknown) {
      console.error('File upload failed:', error);
      // Provide a more detailed error object
      const errorMessage = apiClient.isAxiosError(error) 
        ? error.response?.data?.error || error.message 
        : (error instanceof Error ? error.message : 'Unknown upload error');
        
      return {
        success: false,
        error: errorMessage,
      };
    }
  },

  /**
   * Lists files stored for the current tenant.
   * Can be filtered by fileType and module.
   * 
   * @param fileType Optional filter by file type (e.g., 'images').
   * @param module Optional filter by module (e.g., 'avatars').
   * @returns Promise resolving to an array of FileListItem objects.
   */
  async listFiles(
    fileType?: string,
    module?: string
  ): Promise<FileListItem[]> {
    const params: Record<string, string> = {};
    if (fileType) params.file_type = fileType;
    if (module) params.module = module;

    try {
      const response = await apiClient.get<{ files: any[] }>(`${API_URL}/files/list/`, { params });
      // Convert keys and ensure dates are parsed correctly if needed
      return (response.data.files || []).map(file => convertObjectKeysToCamel(file)) as FileListItem[];
    } catch (error) {
      console.error('Failed to list files:', error);
      return []; // Return empty array on failure
    }
  },

  /**
   * Deletes a file from storage using its path.
   * 
   * @param filePath The full path (object key) of the file in the bucket.
   * @returns Promise resolving to an object indicating success or failure.
   */
  async deleteFile(filePath: string): Promise<{ success: boolean; error?: string }> {
    console.log(`Requesting deletion of file path: ${filePath}`);
    try {
      // Backend expects path in the request body data
      await apiClient.delete(`${API_URL}/files/delete/`, {
        data: { path: filePath }
      });
      console.log(`File deleted successfully: ${filePath}`);
      return { success: true };
    } catch (error: unknown) {
      console.error(`Failed to delete file ${filePath}:`, error);
      const errorMessage = apiClient.isAxiosError(error)
        ? error.response?.data?.error || error.message
        : (error instanceof Error ? error.message : 'Unknown deletion error');
      return {
        success: false,
        error: errorMessage,
      };
    }
  },

  /**
   * Retrieves a temporary, secure (presigned) URL for accessing a file.
   * Ideal for downloading private files or displaying images securely.
   * 
   * @param path The full path (object key) of the file in the bucket.
   * @param expiration Optional expiration time in seconds (default from backend: 3600).
   * @returns Promise resolving to the presigned URL string, or null if failed.
   */
  async getDownloadUrl(path: string, expiration?: number): Promise<string | null> {
    const params: Record<string, string | number> = { path };
    if (expiration !== undefined) {
      params.expiration = expiration;
    }
    try {
      const response = await apiClient.get<FileDownloadResponse>(`${API_URL}/files/download/`, {
        params,
        withCredentials: true, // Ensure auth is sent
      });

      if (response.data.success && response.data.url) {
        return response.data.url;
      }
      console.error(`Failed to get download URL from backend for path: ${path}`, response.data.error);
      return null;
    } catch (error) {
      console.error(`Error fetching download URL for path: ${path}`, error);
      return null;
    }
  },

  /**
   * Constructs a potentially public URL for a file using the configured Tigris public domain.
   * This URL format typically follows: https://<bucket_name>.<endpoint_domain>/<file_path>
   * WARNING: This function *assumes* the file has public read access. 
   * Use getDownloadUrl() for secure access to private files.
   * 
   * @param path The file path (object key) within the bucket.
   * @returns The constructed public URL string, or null if domain is not configured.
   */
  getPublicFileUrl(path: string): string | null {
    if (!TIGRIS_PUBLIC_DOMAIN) {
      console.warn('VITE_TIGRIS_PUBLIC_DOMAIN is not configured in environment variables. Cannot generate public URL.');
      return null;
    }
    if (!path) {
      return null; // Don't generate URL for empty path
    }
    
    // Ensure path doesn't have a leading slash for URL construction
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;
    
    // Construct the URL using the virtual-hosted style domain
    // Ensure the domain doesn't already include https://
    const domain = TIGRIS_PUBLIC_DOMAIN.replace(/^https?:\/\//, '');
    const url = `https://${domain}/${cleanPath}`;
    // console.log(`Generated public URL: ${url}`); // Optional debug log
    return url;
  }
}; 