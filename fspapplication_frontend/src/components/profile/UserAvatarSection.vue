<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <div class="relative">
      <!-- User Avatar with upload functionality -->
      <div 
        class="h-24 w-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg cursor-pointer group"
        @click="triggerFileInput"
      >
        <img
          v-if="completeUser?.avatar"
          :src="completeUser.avatar"
          :alt="`${fullName}'s avatar`"
          class="h-full w-full object-cover transition-opacity group-hover:opacity-80"
        />
        <img 
          v-else
          :src="`https://ui-avatars.com/api/?name=${completeUser?.firstName || ''}+${completeUser?.lastName || ''}&background=0D8ABC&color=fff`" 
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
    </div>
    
    <!-- Change avatar text with subtle styling for hint purposes -->
    <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
      Click Avatar to change
    </p>
    
    <!-- User Name -->
    <h2 class="mt-2 text-xl font-bold text-gray-800 dark:text-white">
      {{ completeUser?.firstName || 'User' }} {{ completeUser?.lastName || '' }}
    </h2>
    
    <!-- User Email -->
    <p class="text-sm text-gray-500 dark:text-gray-400">
      {{ completeUser?.email || 'No email available' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useUserStore } from '@/stores/userProfileStore';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { completeUser } = storeToRefs(userStore);
const fileInput = ref<HTMLInputElement | null>(null);

// Calculate full name
const fullName = computed(() => {
  if (!completeUser.value) return 'User';
  return `${completeUser.value.firstName} ${completeUser.value.lastName}`.trim() || 'User';
});

// Trigger file input click
const triggerFileInput = () => {
  fileInput.value?.click();
};

// Handle file selection
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length) return;
  
  const file = target.files[0];
  const reader = new FileReader();
  
  reader.onload = (e) => {
    // Update the avatar preview
    if (completeUser.value && e.target?.result) {
      completeUser.value.avatar = e.target.result as string;
      
      // In a real implementation, you would upload the file to a server here
      console.log('Avatar file selected:', file.name);
    }
  };
  
  reader.readAsDataURL(file);
};
</script> 