import apiClient from './api';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';

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
   * Upload a file to the server
   * @param file The file to upload
   * @param fileType The type of file (images, documents, etc.)
   * @param module The module the file belongs to (profiles, posts, etc.)
   * @returns Promise with upload result
   */
  async uploadFile(
    file: File,
    fileType: string,
    module: string
  ): Promise<FileUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('file_type', fileType);
      formData.append('module', module);

      const response = await apiClient.post('/files/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true,
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
      let url = `${API_URL}/files/list/`;
      const params: Record<string, string> = {};
      
      if (fileType) params.file_type = fileType;
      if (module) params.module = module;

      const response = await apiClient.get(url, { params });
      
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
   * Get CloudFront URL for a file path
   * @param path The file path
   * @returns Full CloudFront URL
   */
  getCloudFrontUrl(path: string): string {
    const cleanPath = this.normalizePath(path);
    return `https://d1elaz1f509qmb.cloudfront.net/${cleanPath}`;
  }
}; 