<template>
  <BaseModal 
    title="Edit Personal Information"
    :isLoading="isSaving"
    @close="closeModal"
    @save="saveChanges"
  >
    <!-- Modal content goes here as the default slot -->
    <form @submit.prevent="saveChanges" class="space-y-6">
      <div class="space-y-2">
        <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Phone Number</label>
        <input
          v-model="editForm.phoneNumber"
          type="text"
          class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
          placeholder="Enter phone number"
        />
      </div>
      
      <!-- Other form fields -->
    </form>
    
    <!-- Optional custom footer (instead of default buttons) -->
    <!-- <template #footer>
      <custom-buttons />
    </template> -->
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import BaseModal from '@/components/Common/UI/BaseModal.vue';

const isSaving = ref(false);
const editForm = reactive({
  phoneNumber: '',
  // Other fields
});

const saveChanges = () => {
  isSaving.value = true;
  // Save logic here
  // When done:
  isSaving.value = false;
};

const closeModal = () => {
  // Your close logic
};
</script> 