<template>
  <div class="file-uploader">
    <div 
      class="drop-zone" 
      :class="{ 'drop-zone--active': isDragging, 'drop-zone--disabled': disabled }"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
    >
      <div v-if="loading" class="drop-zone__loading">
        <div class="inline-block h-6 w-6 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"></div>
        <span class="ml-2">Uploading...</span>
      </div>
      <div v-else class="drop-zone__prompt">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p class="text-sm text-gray-500 mt-2">Click to browse or drag and drop files here</p>
        <p v-if="accept" class="text-xs text-gray-400 mt-1">Accepted formats: {{ acceptDescription }}</p>
      </div>
    </div>
    
    <input 
      ref="fileInput"
      type="file"
      class="hidden"
      :accept="accept"
      :multiple="multiple"
      @change="onFileChange"
    />
    
    <div v-if="error" class="text-red-500 text-sm mt-2">
      {{ error }}
    </div>
    
    <div v-if="filePreview" class="mt-4">
      <div class="flex items-center bg-gray-50 p-3 rounded-md">
        <div v-if="isImage(filePreview)" class="flex-shrink-0 w-12 h-12 mr-3">
          <img :src="filePreview.url" class="w-full h-full object-cover rounded" />
        </div>
        <div v-else class="flex-shrink-0 w-12 h-12 mr-3 flex items-center justify-center bg-gray-200 rounded">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div class="flex-grow">
          <div class="text-sm font-medium text-gray-700">{{ filePreview.name }}</div>
          <div class="text-xs text-gray-500">{{ formatFileSize(filePreview.size) }}</div>
        </div>
        <button 
          @click.prevent="clearFile" 
          class="ml-2 p-1 text-gray-400 hover:text-red-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch } from 'vue';
import { fileService, type FileUploadResponse } from '@/service/fileService';

export default defineComponent({
  name: 'FileUploader',
  props: {
    fileType: {
      type: String,
      required: true,
      validator: (value: string) => ['images', 'documents', 'media', 'attachments', 'exports'].includes(value)
    },
    module: {
      type: String,
      required: true
    },
    accept: {
      type: String,
      default: ''
    },
    multiple: {
      type: Boolean,
      default: false
    },
    maxSize: {
      type: Number,
      default: 10 * 1024 * 1024 // 10MB default
    },
    disabled: {
      type: Boolean,
      default: false
    },
    resizeImages: {
      type: Boolean,
      default: true
    },
    maxImageWidth: {
      type: Number,
      default: 1200
    },
    maxImageHeight: {
      type: Number,
      default: 1200
    },
    imageQuality: {
      type: Number,
      default: 0.8
    }
  },
  emits: ['upload-success', 'upload-error', 'file-change'],
  setup(props, { emit }) {
    const fileInput = ref<HTMLInputElement | null>(null);
    const isDragging = ref(false);
    const loading = ref(false);
    const error = ref('');
    const filePreview = ref<{name: string, size: number, url: string} | null>(null);
    
    const acceptDescription = computed(() => {
      if (!props.accept) return '';
      return props.accept.split(',').map(type => 
        type.trim().replace('.', '').toUpperCase()
      ).join(', ');
    });
    
    const triggerFileInput = () => {
      if (props.disabled || loading.value) return;
      if (fileInput.value) fileInput.value.click();
    };
    
    const onDragOver = (e: DragEvent) => {
      if (props.disabled || loading.value) return;
      isDragging.value = true;
    };
    
    const onDragLeave = () => {
      isDragging.value = false;
    };
    
    const onDrop = async (e: DragEvent) => {
      if (props.disabled || loading.value) return;
      
      isDragging.value = false;
      error.value = '';
      
      const files = e.dataTransfer?.files;
      if (!files || files.length === 0) return;
      
      const file = files[0]; // Only handling single file for now
      processFile(file);
    };
    
    const onFileChange = (e: Event) => {
      const target = e.target as HTMLInputElement;
      if (!target.files || target.files.length === 0) return;
      
      const file = target.files[0];
      processFile(file);
      
      // Reset input so the same file can be uploaded again
      if (fileInput.value) fileInput.value.value = '';
    };
    
    const processFile = async (file: File) => {
      error.value = '';
      
      // Check file size
      if (file.size > props.maxSize) {
        error.value = `File size exceeds maximum allowed (${formatFileSize(props.maxSize)})`;
        emit('upload-error', error.value);
        return;
      }
      
      // Check file type if accept is specified
      if (props.accept && !isAcceptedFileType(file, props.accept)) {
        error.value = `File type not accepted. Please upload: ${acceptDescription.value}`;
        emit('upload-error', error.value);
        return;
      }
      
      // Create temporary preview
      createPreview(file);
      
      // If it's an image and resizing is enabled, resize it first
      let fileToUpload = file;
      if (props.resizeImages && isImageFile(file)) {
        try {
          fileToUpload = await resizeImage(file);
        } catch (err) {
          // Continue with original file if resize fails
        }
      }
      
      // Upload file
      await uploadFile(fileToUpload);
    };
    
    const isAcceptedFileType = (file: File, accept: string): boolean => {
      const fileType = file.type;
      const fileExtension = file.name.split('.').pop()?.toLowerCase();
      const acceptedTypes = accept.split(',').map(type => type.trim().toLowerCase());
      
      return acceptedTypes.some(type => {
        // Check mime type (e.g., image/*, image/png)
        if (type.includes('/*')) {
          const category = type.split('/')[0];
          return fileType.startsWith(category + '/');
        }
        // Check specific mime type
        if (type.includes('/')) {
          return fileType === type;
        }
        // Check extension (e.g., .png, .jpg)
        return type === `.${fileExtension}`;
      });
    };
    
    const createPreview = (file: File) => {
      // Create object URL for preview
      const url = URL.createObjectURL(file);
      filePreview.value = {
        name: file.name,
        size: file.size,
        url
      };
      
      emit('file-change', file);
    };
    
    const uploadFile = async (file: File) => {
      loading.value = true;
      
      try {
        const result: FileUploadResponse = await fileService.uploadFile(
          file, 
          props.fileType,
          props.module
        );
        
        if (result.success) {
          emit('upload-success', {
            path: result.path,
            url: result.url,
            file
          });
        } else {
          error.value = result.error || 'Upload failed';
          emit('upload-error', error.value);
        }
      } catch (err) {
        error.value = 'An error occurred during upload';
        emit('upload-error', error.value);
      } finally {
        loading.value = false;
      }
    };
    
    const clearFile = () => {
      if (filePreview.value?.url) {
        URL.revokeObjectURL(filePreview.value.url);
      }
      filePreview.value = null;
      emit('file-change', null);
    };
    
    const formatFileSize = (bytes: number): string => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    const isImage = (file: {name: string}) => {
      const ext = file.name.split('.').pop()?.toLowerCase();
      return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext || '');
    };
    
    const isImageFile = (file: File): boolean => {
      return file.type.startsWith('image/');
    };
    
    const resizeImage = (file: File): Promise<File> => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        
        img.onload = () => {
          // Release object URL
          URL.revokeObjectURL(img.src);
          
          // Calculate new dimensions while maintaining aspect ratio
          let width = img.width;
          let height = img.height;
          
          if (width > props.maxImageWidth) {
            height = (height * props.maxImageWidth) / width;
            width = props.maxImageWidth;
          }
          
          if (height > props.maxImageHeight) {
            width = (width * props.maxImageHeight) / height;
            height = props.maxImageHeight;
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
                { type: file.type, lastModified: Date.now() }
              );
              
              resolve(resizedFile);
            },
            file.type,
            props.imageQuality
          );
        };
        
        img.onerror = () => {
          URL.revokeObjectURL(img.src);
          reject(new Error('Error loading image'));
        };
      });
    };
    
    watch(() => props.disabled, (newVal) => {
      if (newVal && filePreview.value) {
        clearFile();
      }
    });
    
    return {
      fileInput,
      isDragging,
      loading,
      error,
      filePreview,
      acceptDescription,
      triggerFileInput,
      onDragOver,
      onDragLeave,
      onDrop,
      onFileChange,
      clearFile,
      formatFileSize,
      isImage
    };
  }
});
</script>

<style scoped>
.file-uploader {
  width: 100%;
}

.drop-zone {
  border: 2px dashed #e2e8f0;
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.drop-zone:hover {
  border-color: #94a3b8;
}

.drop-zone--active {
  border-color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.05);
}

.drop-zone--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.drop-zone__loading {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hidden {
  display: none;
}
</style> 