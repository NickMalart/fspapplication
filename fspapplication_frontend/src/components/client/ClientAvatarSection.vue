<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <div class="relative">
      <!-- Client Logo with upload functionality -->
      <div 
        class="h-24 w-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg cursor-pointer group"
        @click="triggerFileInput"
      >
        <img
          v-if="tempLogoUrl"
          :src="tempLogoUrl"
          :alt="`${clientName}'s logo`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <img
          v-else-if="client?.logo"
          :src="fileService.getCloudFrontUrl(client.logo)"
          :alt="`${clientName}'s logo`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <div v-else class="h-full w-full flex items-center justify-center bg-primary-600"
             :style="{ backgroundColor: generateInitialBgColor(client?.name || '') }">
          <span class="text-white text-3xl font-bold">
            {{ clientInitial }}
          </span>
        </div>
        <!-- Subtle glow effect on hover -->
        <div class="absolute inset-0 bg-primary bg-opacity-20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
      </div>
      <!-- Hidden file input -->
      <input 
        type="file" 
        ref="fileInput" 
        class="hidden" 
        accept="image/*" 
        @change="handleFileChange"
      />
      
      <!-- Loading indicator -->
      <div v-if="isUploading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70 dark:bg-gray-800 dark:bg-opacity-70 rounded-full">
        <div class="h-6 w-6 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>

      <!-- Remove logo button - only show if a logo exists -->
      <button 
        v-if="client?.logo" 
        @click.stop="removeLogo"
        class="absolute -bottom-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 transition-colors"
        title="Remove logo"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Change logo text with subtle styling for hint purposes -->
    <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
      Click to change client logo
    </p>
    
    <!-- Error message if upload fails -->
    <p v-if="uploadError" class="mt-1 text-xs text-red-500">
      {{ uploadError }}
    </p>
    
    <!-- Client Name -->
    <h2 class="mt-2 text-xl font-bold text-gray-800 dark:text-white">
      {{ client?.name || 'Client Name' }}
    </h2>
    
    <!-- Client ABN -->
    <p v-if="client?.abn" class="text-sm text-gray-500 dark:text-gray-400">
      ABN: {{ client.abn }}
    </p>
    
    <!-- Client Website -->
    <p v-if="client?.website" class="text-sm text-gray-500 dark:text-gray-400">
      <a :href="client.website" target="_blank" rel="noopener noreferrer" class="hover:text-primary-600">
        {{ client.website }}
      </a>
    </p>
    
    <!-- Client Status Badge -->
    <div class="mt-2 flex items-center">
      <span class="h-2 w-2 rounded-full mr-1" :class="client?.isActive ? 'bg-green-500' : 'bg-red-500'"></span>
      <span class="text-xs text-gray-500 dark:text-gray-400">
        {{ client?.isActive ? 'Active' : 'Inactive' }}
      </span>
    </div>

    <!-- Admin actions -->
    <div class="mt-4 flex gap-2">
      <button 
        @click="toggleClientStatus"
        class="px-2 py-0.5 text-[11px] rounded font-medium transition-colors"
        :class="client?.isActive 
          ? 'bg-red-100 text-red-700 hover:bg-red-200' 
          : 'bg-green-100 text-green-700 hover:bg-green-200'"
      >
        {{ client?.isActive ? 'Deactivate' : 'Activate' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { fileService } from '@/service/fileService';
import { Client } from '@/service/clientService';
import { clientService } from '@/service/clientService';
import { useClientStore } from '@/stores/clientStore';

// Define props for client data
const props = defineProps<{
  client?: Client | null;
}>();

const emit = defineEmits(['logo-updated', 'status-updated']);

const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const uploadError = ref('');
const tempLogoUrl = ref<string | null>(null);

const clientStore = useClientStore();

// Calculate client name
const clientName = computed(() => {
  return props.client?.name || 'Client';
});

// Get client initial for placeholder
const clientInitial = computed(() => {
  if (!props.client?.name) return 'C';
  return props.client.name.charAt(0).toUpperCase();
});

// Function to generate consistent color based on client name
const generateInitialBgColor = (name: string) => {
  const colors = [
    '#1E88E5', '#43A047', '#E53935', '#5E35B1', '#FB8C00', 
    '#00897B', '#3949AB', '#8E24AA', '#D81B60', '#039BE5'
  ];
  
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  return colors[Math.abs(hash) % colors.length];
};

// Trigger file input click
const triggerFileInput = () => {
  if (isUploading.value) return;
  fileInput.value?.click();
};

// Handle file selection
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length || !props.client?.id) return;
  
  const file = target.files[0];
  
  // Basic validation
  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Please select an image file';
    return;
  }
  
  if (file.size > 5 * 1024 * 1024) { // 5MB limit
    uploadError.value = 'Image size must be less than 5MB';
    return;
  }
  
  // Clear any previous errors
  uploadError.value = '';
  
  // Create a temporary preview
  const reader = new FileReader();
  reader.onload = (e) => {
    if (e.target?.result) {
      tempLogoUrl.value = e.target.result as string;
    }
  };
  reader.readAsDataURL(file);
  
  // Upload to S3
  isUploading.value = true;
  try {
    // First upload the file to S3
    const uploadResult = await fileService.uploadFile(
      file,
      'images',
      'client'
    );
    
    if (!uploadResult.success || !uploadResult.path) {
      throw new Error(uploadResult.error || 'Failed to upload logo to S3');
    }

    // Get the S3 path from the upload result
    const s3Path = uploadResult.path;

    // Update client with the S3 path using the store
    try {
      const updatedClient = await clientStore.updateClientLogo(props.client.id, s3Path);

      // Emit the update to parent component with the full updated client
      emit('logo-updated', updatedClient);

      // Clear the temporary preview since we'll now use the saved path
      tempLogoUrl.value = null;
    } catch (error) {
      throw new Error('Failed to update client with new logo');
    }
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating logo';
    tempLogoUrl.value = null;
  } finally {
    isUploading.value = false;
  }
  
  // Reset input value to allow selecting the same file again
  if (fileInput.value) fileInput.value.value = '';
};

// Remove logo function
const removeLogo = async (event: Event) => {
  event.stopPropagation();
  
  if (!props.client?.id) return;
  
  isUploading.value = true;
  uploadError.value = '';
  
  try {
    // Update client in the database with null logo using the store
    const updatedClient = await clientStore.updateClientLogo(props.client.id, null);

    // Emit the update to parent component with the full updated client
    emit('logo-updated', updatedClient);
    
    // Clear any temporary logo preview
    tempLogoUrl.value = null;
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while removing logo';
  } finally {
    isUploading.value = false;
  }
};

// Toggle client status
const toggleClientStatus = async () => {
  if (!props.client?.id) return;
  
  try {
    const updatedClient = await clientService.updateClientStatus(
      props.client.id,
      !props.client.isActive
    );
    
    // Emit the update to parent component
    emit('status-updated', { id: props.client.id, isActive: updatedClient.isActive });
  } catch (error) {
    console.error('Failed to update client status:', error);
  }
};
</script> 