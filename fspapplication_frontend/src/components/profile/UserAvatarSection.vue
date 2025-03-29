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
        <div
          v-else
          class="h-full w-full bg-primary/20 flex items-center justify-center text-2xl font-bold text-primary"
        >
          {{ avatarInitials }}
        </div>
      </div>
    </div>
    
    <!-- User Name -->
    <h2 class="mt-4 text-xl font-bold text-gray-800 dark:text-white">
      {{ fullName }}
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

const userProfile = computed(() => completeUser.value?.profile || null);

// Calculate full name
const fullName = computed(() => {
  if (!completeUser.value) return 'User';
  return `${completeUser.value.first_name} ${completeUser.value.last_name}`.trim() || 'User';
});

// Generate initials for avatar fallback
const avatarInitials = computed(() => {
  if (!completeUser.value) return '?';
  
  const firstName = completeUser.value.first_name || '';
  const lastName = completeUser.value.last_name || '';
  
  if (!firstName && !lastName) return '?';
  
  return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
});
</script> 