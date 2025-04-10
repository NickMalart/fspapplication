<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <div class="relative">
      <!-- Company Logo with upload functionality -->
      <div 
        class="h-24 w-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg cursor-pointer group"
        @click="triggerFileInput"
      >
        <img
          v-if="tempLogoUrl"
          :src="tempLogoUrl"
          :alt="`${companyName}'s logo`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <img
          v-else-if="logoUrl"
          :src="logoUrl"
          :alt="`${companyName}'s logo`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <img
          v-else
          src="/images/logo/default-company-logo.png"
          alt="Default Company Logo"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
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
        v-if="logoUrl" 
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
      Click to change company logo
    </p>
    
    <!-- Error message if upload fails -->
    <p v-if="uploadError" class="mt-1 text-xs text-red-500">
      {{ uploadError }}
    </p>
    
    <!-- Company Name -->
    <h2 class="mt-2 text-xl font-bold text-gray-800 dark:text-white">
      {{ company?.name || 'Company Name' }}
    </h2>
    
    <!-- Company Website -->
    <p v-if="company?.website" class="text-sm text-gray-500 dark:text-gray-400">
      {{ company.website }}
    </p>
    
    <!-- Brand Colors Section -->
    <div class="mt-4 flex flex-col items-center gap-3">
      <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300">Brand Colors</h3>
      
      <div class="flex items-center gap-4">
        <!-- Primary Color -->
        <div class="flex flex-col items-center">
          <label class="mb-1 text-xs text-gray-500 dark:text-gray-400">Primary</label>
          <div class="relative group">
            <div 
              class="h-8 w-8 rounded-full border border-gray-300 dark:border-gray-600 shadow cursor-pointer"
              :style="{ backgroundColor: company?.primaryColor || '#3B82F6' }"
              @click="primaryColorInput?.click()"
            ></div>
            <input 
              ref="primaryColorInput"
              type="color" 
              class="sr-only"
              :value="company?.primaryColor || '#3B82F6'"
              @change="updatePrimaryColor"
            />
          </div>
          <span class="mt-1 text-xs">{{ company?.primaryColor || '#3B82F6' }}</span>
        </div>
        
        <!-- Secondary Color -->
        <div class="flex flex-col items-center">
          <label class="mb-1 text-xs text-gray-500 dark:text-gray-400">Secondary</label>
          <div class="relative group">
            <div 
              class="h-8 w-8 rounded-full border border-gray-300 dark:border-gray-600 shadow cursor-pointer"
              :style="{ backgroundColor: company?.secondaryColor || '#1E40AF' }"
              @click="secondaryColorInput?.click()"
            ></div>
            <input 
              ref="secondaryColorInput"
              type="color" 
              class="sr-only"
              :value="company?.secondaryColor || '#1E40AF'"
              @change="updateSecondaryColor"
            />
          </div>
          <span class="mt-1 text-xs">{{ company?.secondaryColor || '#1E40AF' }}</span>
        </div>
      </div>
      
      <!-- Color update feedback -->
      <p v-if="colorUpdateStatus" class="mt-1 text-xs" :class="colorUpdateStatus === 'success' ? 'text-green-500' : 'text-red-500'">
        {{ colorUpdateStatus === 'success' ? 'Colors updated successfully' : 'Failed to update colors' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { usecompanyStore } from '@/stores/companyStore';
import { fileService } from '@/service/fileService';
import type { CompanyProfile } from '@/service/companyService';

// Define props for company data
const props = defineProps<{
  company?: CompanyProfile | null;
}>();

const companyStore = usecompanyStore();
const fileInput = ref<HTMLInputElement | null>(null);
const primaryColorInput = ref<HTMLInputElement | null>(null);
const secondaryColorInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const uploadError = ref('');
const tempLogoUrl = ref<string | null>(null);
const colorUpdateStatus = ref<'success' | 'error' | null>(null);

// Calculate company name
const companyName = computed(() => {
  return props.company?.name || 'Company';
});

// Get company initial for placeholder
const companyInitial = computed(() => {
  if (!props.company?.name) return 'C';
  return props.company.name.charAt(0).toUpperCase();
});

// Create a computed property for the logo URL
const logoUrl = computed(() => {
  if (!props.company?.logo) return null;
  
  const logoPath = props.company.logo;
  
  // If it's already a CloudFront URL, use it as-is
  if (logoPath.startsWith('https://d1elaz1f509qmb.cloudfront.net/')) {
    return logoPath;
  }
  
  // Otherwise, construct the CloudFront URL directly
  return fileService.getCloudFrontUrl(logoPath);
});

// Trigger file input click
const triggerFileInput = () => {
  if (isUploading.value) return;
  fileInput.value?.click();
};

// Remove logo function
const removeLogo = async (event: Event) => {
  // Prevent the click from triggering the file input
  event.stopPropagation();
  
  // Show loading state
  isUploading.value = true;
  uploadError.value = '';
  
  try {
    // Update company profile with null logo path
    await companyStore.updateCompanyProfile({
      logo: null // Setting logo to null will remove it
    });
    
    // Clear any temporary logo preview
    tempLogoUrl.value = null;
    
    // Update favicon to default
    updateFavicon(null);
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while removing logo';
  } finally {
    isUploading.value = false;
  }
};

// Function to update favicon
const updateFavicon = (logoPath: string | null) => {
  const favicon = document.getElementById('favicon') as HTMLLinkElement;
  if (favicon) {
    if (logoPath) {
      // Use the company logo
      favicon.href = fileService.getCloudFrontUrl(logoPath);
    } else {
      // Reset to default logo
      favicon.href = '/images/logo/default-company-logo.png';
    }
  }
};

// Handle file selection
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length) return;
  
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
      // Preview is temporary, no need to update Pinia yet
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
      'company',
      { maxWidth: 800, maxHeight: 800, quality: 0.85 }
    );
    
    if (!uploadResult.success || !uploadResult.path) {
      throw new Error(uploadResult.error || 'Failed to upload logo to S3');
    }
    
    // Then update the company profile with the S3 path
    await companyStore.updateCompanyProfile({
      logo: uploadResult.path // Store the path in the database
    });
    
    // Update favicon immediately
    updateFavicon(uploadResult.path);
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating logo';
    
    // Clear temporary logo
    tempLogoUrl.value = null;
  } finally {
    isUploading.value = false;
  }
  
  // Reset input value to allow selecting the same file again
  if (fileInput.value) fileInput.value.value = '';
};

// Update primary color
const updatePrimaryColor = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.value) return;
  
  colorUpdateStatus.value = null;
  
  try {
    const success = await companyStore.updateCompanyProfile({
      primaryColor: target.value
    });
    
    colorUpdateStatus.value = success ? 'success' : 'error';
    
    // Clear status after 3 seconds
    setTimeout(() => {
      colorUpdateStatus.value = null;
    }, 3000);
    
  } catch (error) {
    colorUpdateStatus.value = 'error';
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating primary color';
  }
};

// Update secondary color
const updateSecondaryColor = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.value) return;
  
  colorUpdateStatus.value = null;
  
  try {
    const success = await companyStore.updateCompanyProfile({
      secondaryColor: target.value
    });
    
    colorUpdateStatus.value = success ? 'success' : 'error';
    
    // Clear status after 3 seconds
    setTimeout(() => {
      colorUpdateStatus.value = null;
    }, 3000);
    
  } catch (error) {
    colorUpdateStatus.value = 'error';
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating secondary color';
  }
};
</script> 