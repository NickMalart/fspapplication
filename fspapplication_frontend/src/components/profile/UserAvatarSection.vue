<template>
  <div class="flex flex-col items-center justify-center mb-6">
    <div class="relative">
      <!-- User Avatar -->
      <div class="h-24 w-24 rounded-full overflow-hidden border-4 border-white dark:border-gray-800 shadow-lg">
        <img
          v-if="completeUser?.avatar"
          :src="completeUser.avatar"
          :alt="`${fullName}'s avatar`"
          class="h-full w-full object-cover"
        />
        <img 
          v-else
          :src="`https://ui-avatars.com/api/?name=${completeUser?.firstName || ''}+${completeUser?.lastName || ''}&background=0D8ABC&color=fff`" 
          :alt="`${fullName}'s avatar`"
          class="h-full w-full object-cover"
        />
      </div>
    </div>
    
    <!-- User Name -->
    <h2 class="mt-4 text-xl font-bold text-gray-800 dark:text-white">
      {{ completeUser?.firstName || 'User' }} {{ completeUser?.lastName || '' }}
    </h2>
    
    <!-- User Email -->
    <p class="text-sm text-gray-500 dark:text-gray-400">
      {{ completeUser?.email || 'No email available' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/stores/userProfileStore';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { completeUser } = storeToRefs(userStore);

// Calculate full name
const fullName = computed(() => {
  if (!completeUser.value) return 'User';
  return `${completeUser.value.firstName} ${completeUser.value.lastName}`.trim() || 'User';
});
</script> 