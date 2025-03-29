<template>
  <div class="fixed inset-0 flex items-center justify-center overflow-y-auto modal z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>
    <div class="relative z-10 bg-white dark:bg-boxdark rounded-lg shadow-lg w-full max-w-md mx-4 p-6">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-lg font-bold text-black dark:text-white">Edit Personal Information</h3>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <form @submit.prevent="saveChanges" class="space-y-6">
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

        <div class="flex items-center justify-end gap-4 mt-6">
          <button 
            type="button"
            @click="$emit('close')"
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, defineEmits, defineProps } from 'vue';

const props = defineProps({
  userData: {
    type: Object,
    required: true
  },
  isSaving: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'save']);

const editForm = reactive({
  phone_number: props.userData.phone_number || '',
  date_of_birth: props.userData.date_of_birth || ''
});

const saveChanges = () => {
  emit('save', {
    phone_number: editForm.phone_number || null,
    date_of_birth: editForm.date_of_birth || null
  });
};
</script> 