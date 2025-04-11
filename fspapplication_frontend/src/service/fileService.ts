import apiClient from './api';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

// const API_URL = import.meta.env.VITE_API_URL || '/api'; // Remove unused constant

export interface FileUploadResponse {
  success: boolean;
  path?: string;
  url?: string;
  id?: number;
  error?: string;
}

export interface FileListItem {
  key: string;
  url: string;
  filename: string;
  fileType: string;
  module: string;
  lastModified: Date;
  size: number;
}

export interface FileDownloadResponse {
  success: boolean;
  url?: string;
  error?: string;
}

// Interface for image resize options
export interface ImageResizeOptions {
  maxWidth?: number;
  maxHeight?: number;
  quality?: number;
  outputFormat?: string;
}

export const fileService = {
  /**
   * Normalizes a file path to be used with CloudFront
   * Removes /dev prefix, localhost URLs, and standardizes the path
   * 
   * @param path The file path to normalize
   * @returns Normalized path suitable for CloudFront
   */
  normalizePath(path: string): string {
    if (!path) return '';
    
    let cleanPath = path;
    
    // Remove any domain or protocol parts if present
    if (cleanPath.includes('://')) {
      cleanPath = new URL(cleanPath).pathname;
    }
    
    // Remove /dev prefix if present
    cleanPath = cleanPath.replace(/^\/dev\//, '');
    
    // Remove any leading slash
    cleanPath = cleanPath.startsWith('/') ? cleanPath.substring(1) : cleanPath;
    
    return cleanPath;
  },

  /**
   * Resizes an image client-side before upload to reduce server load and bandwidth
   * 
   * @param file The original file to resize
   * @param options Resize options (width, height, quality)
   * @returns Promise that resolves to the resized file
   */
  async resizeImage(file: File, options: ImageResizeOptions = {}): Promise<File> {
    // Skip resizing if not an image
    if (!file.type.startsWith('image/')) {
      return file;
    }
    
    const maxWidth = options.maxWidth || 800;
    const maxHeight = options.maxHeight || 800;
    const quality = options.quality || 0.85;
    
    // Preserve original format for PNG to maintain transparency
    const outputFormat = options.outputFormat || 
                         (file.type === 'image/png' ? 'image/png' : 'image/jpeg');
    
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = URL.createObjectURL(file);
      
      img.onload = () => {
        // Release object URL
        URL.revokeObjectURL(img.src);
        
        // Calculate new dimensions while maintaining aspect ratio
        let width = img.width;
        let height = img.height;
        
        if (width > maxWidth) {
          height = (height * maxWidth) / width;
          width = maxWidth;
        }
        
        if (height > maxHeight) {
          width = (width * maxHeight) / height;
          height = maxHeight;
        }
        
        // Skip resizing if image is already smaller than target dimensions
        if (img.width <= maxWidth && img.height <= maxHeight && file.type === outputFormat) {
          console.log('Image already smaller than target size, skipping resize');
          resolve(file);
          return;
        }
        
        // Create canvas for resizing
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        
        // Draw and resize image on canvas
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          reject(new Error('Could not get canvas context'));
          return;
        }
        
        // For PNG files, ensure the canvas is transparent before drawing
        if (outputFormat === 'image/png') {
          ctx.clearRect(0, 0, width, height);
        }
        
        ctx.drawImage(img, 0, 0, width, height);
        
        // Convert to blob with reduced quality
        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error('Canvas to Blob conversion failed'));
              return;
            }
            
            // Create new file from blob
            const resizedFile = new File(
              [blob],
              file.name,
              { type: outputFormat, lastModified: Date.now() }
            );
            
            // Use the formatFileSize method from this object
            const formatSize = fileService.formatFileSize;
            console.log(`Resized image from ${formatSize(file.size)} to ${formatSize(resizedFile.size)}`);
            resolve(resizedFile);
          },
          outputFormat,
          quality
        );
      };
      
      img.onerror = () => {
        URL.revokeObjectURL(img.src);
        reject(new Error('Error loading image'));
      };
    });
  },
  
  /**
   * Format file size in a human-readable format
   * @param bytes File size in bytes
   * @returns Formatted string (e.g., "2.5 MB")
   */
  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  /**
   * Upload a file to the server with automatic image resizing
   * @param file The file to upload
   * @param fileType The type category for the file
   * @param module The module the file belongs to
   * @param resizeOptions Optional image resize options (if it's an image)
   * @returns Promise with the upload response
   */
  async uploadFile(
    file: File,
    fileType: string,
    module: string,
    resizeOptions?: ImageResizeOptions
  ): Promise<FileUploadResponse> {
    try {
      // Automatically resize images before upload
      let fileToUpload = file;
      
      if (file.type.startsWith('image/') && resizeOptions !== null) {
        try {
          fileToUpload = await this.resizeImage(file, resizeOptions || undefined);
        } catch (err) {
          console.error('Error resizing image:', err);
          // Continue with original file if resize fails
        }
      }
      
      const formData = new FormData();
      formData.append('file', fileToUpload);
      formData.append('file_type', fileType);
      formData.append('module', module);
      formData.append('use_chunked_upload', 'true');

      const response = await apiClient.post('/files/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true
      });

      return response.data;
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { error?: string } }, message?: string };
      return {
        success: false,
        error: axiosError.response?.data?.error || axiosError.message || 'Failed to upload file',
      };
    }
  },

  /**
   * List files for the tenant, optionally filtered by file type and module
   * 
   * @param fileType - Optional type filter (images, documents, etc.)
   * @param module - Optional module filter
   * @returns Promise with array of file objects
   */
  async listFiles(
    fileType?: string,
    module?: string
  ): Promise<FileListItem[]> {
    try {
      // Use relative path with apiClient
      const endpoint = 'files/list/'; 
      const params: Record<string, string> = {};
      
      if (fileType) params.file_type = fileType;
      if (module) params.module = module;

      // Pass relative endpoint and params to apiClient
      const response = await apiClient.get(endpoint, { params });
      
      return convertObjectKeysToCamel(response.data.files || []);
    } catch (error) {
      return [];
    }
  },

  /**
   * Delete a file by its path
   * 
   * @param filePath - Full S3 path of the file to delete
   * @returns Promise with success status
   */
  async deleteFile(filePath: string): Promise<{ success: boolean; error?: string }> {
    try {
      await apiClient.delete('/files/delete/', {
        data: { path: filePath }
      });
      
      return { success: true };
    } catch (error) {
      if (apiClient.isAxiosError(error) && error.response) {
        return {
          success: false,
          error: error.response.data.detail || 'File deletion failed',
        };
      }
      return {
        success: false,
        error: 'File deletion failed',
      };
    }
  },

  /**
   * Get a URL for downloading a file
   * @param path The path of the file to download
   * @returns Promise with download URL
   */
  async getDownloadUrl(path: string): Promise<string | null> {
    try {
      const response = await apiClient.get('/files/download/', {
        params: { path },
        withCredentials: true,
      });

      if (response.data.success && response.data.url) {
        return response.data.url;
      }
      return null;
    } catch (error) {
      return null;
    }
  },

  /**
   * Get the public URL for a file stored in Tigris using the custom asset domain.
   * @param path The relative path of the file as stored (e.g., 'images/company/logo.png')
   * @returns The full public URL (e.g., 'https://frosty-bird-4733.fly.storage.tigris.dev/dev/images/company/logo.png')
   */
  getPublicFileUrl(path: string): string {
    if (!path) {
      // Return a default or placeholder image URL if the path is empty
      return '/images/logo/default-company-logo.png'; 
    }

    // Use the base Tigris domain from environment
    const baseDomain = import.meta.env.VITE_TIGRIS_ENDPOINT || 'https://frosty-bird-4733.fly.storage.tigris.dev';

    // Ensure the base path includes 'dev' if it's not already present
    const cleanPath = path.startsWith('dev/') ? path : `dev/${path}`;

    // Construct the full URL
    return `${baseDomain}/${cleanPath}`;
  }
}; 