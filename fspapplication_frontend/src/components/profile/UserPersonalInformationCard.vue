<template>
  <ComponentCard title="Personal Information">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-900 text-red-700 dark:text-red-300 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Data Display with Edit Button in Relative Position -->
    <div v-else class="relative">
      <!-- Edit Button -->
      <button 
        v-if="userProfile" 
        @click="isModalOpen = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="userProfile" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Phone Number</p>
          <p class="font-medium text-black dark:text-white">
            {{ userProfile.phone_number || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Date of Birth</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatDate(userProfile.date_of_birth) }}
          </p>
        </div>
      </div>
      <div v-else class="py-4 text-center text-gray-500">
        No profile information available
      </div>
    </div>

    <!-- Edit Modal -->
    <EditUserPersonalInformationModal
      v-if="isModalOpen && userProfile"
      :userData="userProfile"
      :isSaving="isSaving"
      @close="isModalOpen = false"
      @save="handleSave"
    />
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/userProfileStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';
import EditUserPersonalInformationModal from '@/components/profile/EditUserPersonalInformationModal.vue';

const userStore = useUserStore();
const { completeUser, loading, error } = storeToRefs(userStore);

const userProfile = computed(() => completeUser.value?.profile || null);
const isModalOpen = ref(false);
const isSaving = ref(false);

// Format date for display
const formatDate = (dateString: string | null) => {
  if (!dateString) return 'Not provided';
  
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric', 
      month: 'long', 
      day: 'numeric'
    }).format(date);
  } catch (e) {
    return dateString || 'Not provided';
  }
};

// Handle save from modal
const handleSave = async (formData: { phone_number: string | null, date_of_birth: string | null }) => {
  isSaving.value = true;
  
  try {
    await userStore.updateProfileData(formData);
    isModalOpen.value = false;
  } catch (error) {
    console.error('Failed to save changes:', error);
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await userStore.fetchUserProfile();
});
</script>
