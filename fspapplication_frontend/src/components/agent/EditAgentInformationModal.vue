<template>
  <div class="fixed inset-0 flex items-center justify-center p-5 overflow-y-auto modal z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>
    <div class="relative w-full max-w-[584px] rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-10">
      <!-- close btn -->
      <button 
        @click="$emit('close')" 
        class="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11"
      >
        <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z" fill=""></path>
        </svg>
      </button>
      
      <h4 class="mb-6 text-lg font-medium text-gray-800 dark:text-white/90">
        Edit Agent Information
      </h4>
      
      <form @submit.prevent="saveChanges" class="space-y-6">
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Agent Name</label>
          <input
            v-model="editForm.name"
            type="text"
            class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="Enter agent name"
          />
        </div>
        
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Phone</label>
          <input
            v-model="editForm.phone"
            type="text"
            class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="Enter phone number"
          />
        </div>
        
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Email</label>
          <input
            v-model="editForm.email"
            type="email"
            class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="Enter email address"
          />
        </div>
        
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Website</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
              <span class="text-sm text-gray-500 dark:text-gray-400">https://</span>
            </div>
            <input
              v-model="editForm.websiteInput"
              type="text"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent pl-16 pr-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="example.com"
            />
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Enter domain without https:// - it will be added automatically</p>
        </div>
        
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">ABN</label>
          <input
            v-model="editForm.abn"
            type="text"
            class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="Enter ABN"
          />
        </div>

        <div class="flex items-center justify-end gap-3 mt-6">
          <button 
            type="button"
            @click="$emit('close')"
            class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
          >
            Close
          </button>
          <button 
            type="submit"
            class="flex justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600"
            :disabled="isSaving"
          >
            <span v-if="isSaving" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, defineEmits, onMounted, watch } from 'vue';
import type { Agent } from '@/service/agentService';

const props = defineProps<{
  agentData: Agent;
  isSaving: boolean;
}>();

const emit = defineEmits(['close', 'save']);

// Initialize form data
const editForm = reactive({
  name: '',
  phone: '',
  email: '',
  websiteInput: '',
  abn: '',
  get website() {
    if (!this.websiteInput) return '';
    return this.websiteInput.startsWith('http') ? this.websiteInput : `https://${this.websiteInput}`;
  }
});

// Initialize form data when props change
const initForm = () => {
  if (props.agentData) {
    editForm.name = props.agentData.name || '';
    editForm.phone = props.agentData.phone || '';
    editForm.email = props.agentData.email || '';
    
    // Strip https:// from website for display in input
    if (props.agentData.website) {
      editForm.websiteInput = props.agentData.website.replace(/^https?:\/\//, '');
    } else {
      editForm.websiteInput = '';
    }
    
    editForm.abn = props.agentData.abn || '';
  }
};

// Save changes
const saveChanges = () => {
  const formData = {
    name: editForm.name || undefined,
    phone: editForm.phone || undefined,
    email: editForm.email || undefined,
    website: editForm.website || undefined,
    abn: editForm.abn || undefined
  };
  
  emit('save', formData);
};

// Initialize on mount and when agentData changes
onMounted(initForm);
watch(() => props.agentData, initForm, { immediate: true });
</script>

<style scoped>
/* Form input focus styling */
input:focus, select:focus {
  outline: none;
}
</style> 