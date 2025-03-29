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

    <!-- Data Display -->
    <div v-else-if="userProfile" class="grid grid-cols-1 md:grid-cols-2 gap-6">
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

    <!-- Edit Button -->
    <div class="flex justify-end mt-6" v-if="userProfile && !isEditing">
      <button 
        @click="startEditing"
        class="inline-flex items-center justify-center gap-2.5 rounded-md bg-primary py-2 px-4 text-white hover:bg-opacity-90"
      >
        <span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </span>
        Edit
      </button>
    </div>

    <!-- Edit Form -->
    <form v-if="isEditing" @submit.prevent="saveChanges" class="mt-6 space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-2">
          <label class="text-sm text-gray-500 dark:text-gray-400">Phone Number</label>
          <input
            v-model="editForm.phone_number"
            type="text"
            class="w-full rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-white/[0.03] py-2 px-4 text-black dark:text-white outline-none focus:border-primary"
            placeholder="Enter phone number"
          />
        </div>
        <div class="space-y-2">
          <label class="text-sm text-gray-500 dark:text-gray-400">Date of Birth</label>
          <input
            v-model="editForm.date_of_birth"
            type="date"
            class="w-full rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-white/[0.03] py-2 px-4 text-black dark:text-white outline-none focus:border-primary"
          />
        </div>
      </div>

      <div class="flex items-center justify-end gap-4">
        <button 
          type="button"
          @click="cancelEditing"
          class="inline-flex items-center justify-center gap-2.5 rounded-md bg-gray-200 dark:bg-white/[0.03] py-2 px-4 text-black dark:text-white hover:bg-opacity-90"
        >
          Cancel
        </button>
        <button 
          type="submit"
          class="inline-flex items-center justify-center gap-2.5 rounded-md bg-primary py-2 px-4 text-white hover:bg-opacity-90"
          :disabled="isSaving"
        >
          <span v-if="isSaving" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
          {{ isSaving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </form>
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue';
import { useUserStore } from '@/stores/userProfileStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';

const userStore = useUserStore();
const { completeUser, loading, error } = storeToRefs(userStore);

const userProfile = computed(() => completeUser.value?.profile || null);
const isEditing = ref(false);
const isSaving = ref(false);

// Form for editing
const editForm = reactive({
  phone_number: '',
  date_of_birth: ''
});

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

// Start editing mode
const startEditing = () => {
  if (userProfile.value) {
    editForm.phone_number = userProfile.value.phone_number || '';
    editForm.date_of_birth = userProfile.value.date_of_birth || '';
  }
  isEditing.value = true;
};

// Cancel editing
const cancelEditing = () => {
  isEditing.value = false;
};

// Save changes
const saveChanges = async () => {
  isSaving.value = true;
  
  try {
    await userStore.updateProfileData({
      phone_number: editForm.phone_number || null,
      date_of_birth: editForm.date_of_birth || null
    });
    
    isEditing.value = false;
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
