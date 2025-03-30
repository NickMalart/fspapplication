<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <div class="relative">
      <!-- User Avatar with upload functionality -->
      <div 
        class="h-24 w-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg cursor-pointer group"
        @click="triggerFileInput"
      >
        <img
          v-if="tempAvatarUrl"
          :src="tempAvatarUrl"
          :alt="`${fullName}'s avatar`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <img
          v-else-if="avatarUrl"
          :src="avatarUrl"
          :alt="`${fullName}'s avatar`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
          referrerpolicy="no-referrer"
        />
        <img 
          v-else
          :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(user?.firstName || '')}-${encodeURIComponent(user?.lastName || '')}&background=0D8ABC&color=fff&size=128`" 
          :alt="`${fullName}'s avatar`"
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
    </div>
    
    <!-- Change avatar text with subtle styling for hint purposes -->
    <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
      Click Avatar to change
    </p>
    
    <!-- Error message if upload fails -->
    <p v-if="uploadError" class="mt-1 text-xs text-red-500">
      {{ uploadError }}
    </p>
    
    <!-- User Name -->
    <h2 class="mt-2 text-xl font-bold text-gray-800 dark:text-white">
      {{ user?.firstName || 'User' }} {{ user?.lastName || '' }}
    </h2>
    
    <!-- User Email -->
    <p class="text-sm text-gray-500 dark:text-gray-400">
      {{ user?.email || 'No email available' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useUserStore } from '@/stores/userProfileStore';
import { fileService } from '@/service/fileService';
import { CompleteUser } from '@/service/userProfileService';

// Define props for user data
const props = defineProps<{
  user?: CompleteUser | null;
}>();

const userStore = useUserStore();
const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const uploadError = ref('');
const tempAvatarUrl = ref<string | null>(null);

// Calculate full name
const fullName = computed(() => {
  if (!props.user) return 'User';
  return `${props.user.firstName} ${props.user.lastName}`.trim() || 'User';
});

// Create a computed property for the avatar URL
const avatarUrl = computed(() => {
  if (!props.user?.avatar) return null;
  
  const avatarPath = props.user.avatar;
  
  // If it's already a CloudFront URL, use it as-is
  if (avatarPath.startsWith('https://d1elaz1f509qmb.cloudfront.net/')) {
    return avatarPath;
  }
  
  // Otherwise, construct the CloudFront URL directly
  return fileService.getCloudFrontUrl(avatarPath);
});

// Trigger file input click
const triggerFileInput = () => {
  if (isUploading.value) return;
  fileInput.value?.click();
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
      tempAvatarUrl.value = e.target.result as string;
    }
  };
  reader.readAsDataURL(file);
  
  // Upload to S3
  isUploading.value = true;
  try {
    // First upload the file to S3
    console.log("Uploading file to S3...");
    const uploadResult = await fileService.uploadFile(
      file,
      'images',
      'profiles'
    );
    
    if (!uploadResult.success || !uploadResult.path) {
      throw new Error(uploadResult.error || 'Failed to upload avatar to S3');
    }
    
    console.log("File uploaded successfully to S3:", uploadResult);
    
    // Then update the user profile with the S3 path
    console.log("Updating user profile with avatar path:", uploadResult.path);
    const updateSuccess = await userStore.updateUserProfile({
      avatar: uploadResult.path // Store the path in the database
    });
    
    if (!updateSuccess) {
      throw new Error("Failed to update user profile with avatar path");
    }
    
    console.log("Profile updated successfully");
    
    // The avatar URL will update automatically through the computed property
    // when userProfile is updated
    
  } catch (error) {
    console.error('Error in avatar update process:', error);
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating avatar';
    
    // Clear temporary avatar
    tempAvatarUrl.value = null;
  } finally {
    isUploading.value = false;
  }
  
  // Reset input value to allow selecting the same file again
  if (fileInput.value) fileInput.value.value = '';
};
</script> 