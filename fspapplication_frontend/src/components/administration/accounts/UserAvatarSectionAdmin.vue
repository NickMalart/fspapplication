<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <!-- Loading state -->
    <div v-if="loadingUser" class="flex flex-col items-center justify-center h-64">
      <div class="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
      <p class="text-sm text-gray-500 dark:text-gray-400">Loading user data...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="userError" class="flex flex-col items-center justify-center h-64">
      <div class="text-red-500 mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <p class="text-sm text-red-500">{{ userError }}</p>
      <button 
        @click="fetchUserData"
        class="mt-4 px-3 py-1 text-xs bg-primary text-white rounded-md hover:bg-primary-dark transition-colors"
      >
        Retry
      </button>
    </div>

    <!-- User profile content -->
    <template v-else-if="currentUser">
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
            :src="`https://ui-avatars.com/api/?name=${encodeURIComponent(currentUser?.firstName || '')}-${encodeURIComponent(currentUser?.lastName || '')}&background=0D8ABC&color=fff&size=128`" 
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

        <!-- Remove avatar button - only show if an avatar exists -->
        <button 
          v-if="avatarUrl" 
          @click.stop="removeAvatar"
          class="absolute -bottom-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 transition-colors"
          title="Remove avatar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
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
        {{ currentUser?.firstName || 'User' }} {{ currentUser?.lastName || '' }}
      </h2>
      
      <!-- User Role Badge -->
      <div class="mt-1 px-2 py-1 bg-primary bg-opacity-10 text-primary text-xs rounded-full">
        {{ currentUser?.userType || 'User' }}
      </div>
      
      <!-- User Email -->
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
        {{ currentUser?.email || 'No email available' }}
      </p>
      
      <!-- User Status -->
      <div class="mt-2 flex items-center">
        <span 
          class="h-2 w-2 rounded-full mr-1" 
          :class="currentUser?.isActive ? 'bg-green-500' : 'bg-red-500'"
        ></span>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {{ currentUser?.isActive ? 'Active' : 'Inactive' }}
        </span>
      </div>
      
      <!-- Admin actions -->
      <div class="mt-4 flex gap-2">
        <button 
          @click="toggleUserStatus"
          class="px-3 py-1 text-xs rounded-md font-medium transition-colors"
          :class="currentUser?.isActive 
            ? 'bg-red-100 text-red-700 hover:bg-red-200 dark:bg-red-900 dark:text-red-300 dark:hover:bg-red-800' 
            : 'bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-900 dark:text-green-300 dark:hover:bg-green-800'"
        >
          {{ currentUser?.isActive ? 'Deactivate' : 'Activate' }}
        </button>
        <button 
          @click="resetPassword"
          class="px-3 py-1 text-xs bg-blue-100 text-blue-700 hover:bg-blue-200 rounded-md font-medium transition-colors dark:bg-blue-900 dark:text-blue-300 dark:hover:bg-blue-800"
        >
          Reset Password
        </button>
      </div>
    </template>
    
    <!-- No user or loading fallback -->
    <div v-else class="flex flex-col items-center justify-center h-64">
      <p class="text-sm text-gray-500 dark:text-gray-400">No user selected</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue';
import { fileService } from '@/service/fileService';
import { userProfileAdminService } from '@/service/userProfileAdminService';
import { useUserProfileAdminStore } from '@/stores/userProfileAdminStore';
import type { UserProfileAdmin } from '@/stores/userProfileAdminStore';

// Define props
const props = defineProps<{
  userId?: string; // Accept userId to fetch data
  user?: UserProfileAdmin | null; // Or accept user directly if already fetched
}>();

const emit = defineEmits<{
  (e: 'update:user', user: UserProfileAdmin): void;
  (e: 'status-toggle'): void;
  (e: 'reset-password'): void;
}>();

const userStore = useUserProfileAdminStore();
const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const uploadError = ref('');
const tempAvatarUrl = ref<string | null>(null);
const loadingUser = ref(false);
const userError = ref<string | null>(null);
const localUser = ref<UserProfileAdmin | null>(null);

// Computed property to use either passed user or locally fetched user
const currentUser = computed(() => props.user || localUser.value);

// Watch for userId changes to fetch user data
watch(() => props.userId, fetchUserData, { immediate: true });

// Fetch user data if userId is provided
async function fetchUserData() {
  if (!props.userId) return;
  
  // Skip if we already have the user data passed as prop
  if (props.user) return;
  
  loadingUser.value = true;
  userError.value = null;
  
  try {
    localUser.value = await userProfileAdminService.getUserProfile(props.userId);
  } catch (error) {
    userError.value = error instanceof Error ? error.message : 'Failed to load user data';
    console.error('Error fetching user:', error);
  } finally {
    loadingUser.value = false;
  }
}

// Fetch user data on mount if userId is provided
onMounted(() => {
  if (props.userId && !props.user) {
    fetchUserData();
  }
});

// Calculate full name
const fullName = computed(() => {
  if (!currentUser.value) return 'User';
  return `${currentUser.value.firstName} ${currentUser.value.lastName}`.trim() || 'User';
});

// Create a computed property for the avatar URL
const avatarUrl = computed(() => {
  if (!currentUser.value?.avatar) return null;
  
  const avatarPath = currentUser.value.avatar;
  
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

// Remove avatar function
const removeAvatar = async (event: Event) => {
  // Prevent the click from triggering the file input
  event.stopPropagation();
  
  if (!currentUser.value) return;
  
  // Show loading state
  isUploading.value = true;
  uploadError.value = '';
  
  try {
    // Update user profile with null avatar path via admin service
    const updatedUser = await userProfileAdminService.patchUserProfile(currentUser.value.id, { avatar: null });
    
    // Update local user if we're managing it
    if (localUser.value) {
      localUser.value = updatedUser;
    }
    
    // Emit updated user
    emit('update:user', updatedUser);
    
    // Clear any temporary avatar preview
    tempAvatarUrl.value = null;
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while removing avatar';
  } finally {
    isUploading.value = false;
  }
};

// Handle file selection
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length || !currentUser.value) return;
  
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
      // Preview is temporary, no need to update yet
      tempAvatarUrl.value = e.target.result as string;
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
      'profiles'
    );
    
    if (!uploadResult.success || !uploadResult.path) {
      throw new Error(uploadResult.error || 'Failed to upload avatar to S3');
    }
    
    // Then update the user profile with the S3 path via admin service
    const updatedUser = await userProfileAdminService.patchUserProfile(currentUser.value.id, { avatar: uploadResult.path });
    
    // Update local user if we're managing it
    if (localUser.value) {
      localUser.value = updatedUser;
    }
    
    // Emit updated user
    emit('update:user', updatedUser);
    
  } catch (error) {
    uploadError.value = error instanceof Error ? error.message : 'An error occurred while updating avatar';
    
    // Clear temporary avatar
    tempAvatarUrl.value = null;
  } finally {
    isUploading.value = false;
  }
  
  // Reset input value to allow selecting the same file again
  if (fileInput.value) fileInput.value.value = '';
};

// Toggle user active status
const toggleUserStatus = async () => {
  if (!currentUser.value) return;
  
  try {
    const newStatus = !currentUser.value.isActive;
    const updatedUser = await userProfileAdminService.updateUserStatus(currentUser.value.id, newStatus);
    
    // Update local user if we're managing it
    if (localUser.value) {
      localUser.value = updatedUser;
    }
    
    // Emit updated user and status toggle event
    emit('update:user', updatedUser);
    emit('status-toggle');
  } catch (error) {
    console.error('Failed to update user status:', error);
  }
};

// Reset user password
const resetPassword = () => {
  emit('reset-password');
};
</script>
