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
            v-model="editForm.phoneNumber"
            type="text"
            class="w-full rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-white/[0.03] py-2 px-4 text-black dark:text-white outline-none focus:border-primary"
            placeholder="Enter phone number"
          />
        </div>
        <div class="space-y-2">
          <label class="text-sm text-gray-500 dark:text-gray-400">Date of Birth</label>
          <div class="relative">
            <input
              v-model="editForm.dateOfBirth"
              type="date"
              class="w-full rounded-md border border-gray-200 dark:border-gray-800 bg-white dark:bg-white/[0.03] py-2 px-4 text-black dark:text-white outline-none focus:border-primary appearance-none"
              :max="maxDate"
            />
            <div class="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <p class="text-xs text-gray-400 mt-1">Format: MM/DD/YYYY</p>
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
import { reactive, defineEmits, defineProps, computed, onMounted, watch } from 'vue';

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

// Initialize form data
const editForm = reactive({
  phoneNumber: '',
  dateOfBirth: ''
});

// Set max date to today (prevent future dates)
const maxDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

// Initialize form data when props change
const initForm = () => {
  if (props.userData) {
    editForm.phoneNumber = props.userData.phoneNumber || '';
    
    // Format date if it exists
    if (props.userData.dateOfBirth) {
      try {
        const date = new Date(props.userData.dateOfBirth);
        if (!isNaN(date.getTime())) {
          editForm.dateOfBirth = date.toISOString().split('T')[0];
        } else {
          editForm.dateOfBirth = '';
        }
      } catch (e) {
        console.error('Error parsing date:', e);
        editForm.dateOfBirth = '';
      }
    } else {
      editForm.dateOfBirth = '';
    }
    
    console.log('Initialized form data:', editForm);
  }
};

// Save changes
const saveChanges = () => {
  const formData = {
    phoneNumber: editForm.phoneNumber || null,
    dateOfBirth: editForm.dateOfBirth || null
  };
  
  console.log('Saving form data:', formData);
  emit('save', formData);
};

// Initialize on mount and when userData changes
onMounted(initForm);
watch(() => props.userData, initForm, { immediate: true });
</script>

<style scoped>
/* Improve date picker styling for different browsers */
input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  cursor: pointer;
}
</style> 