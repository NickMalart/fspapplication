<template>
  <div class="fixed inset-0 flex items-center justify-center p-5 overflow-y-auto modal z-99999">
    <!-- Backdrop overlay -->
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>
    
    <!-- Modal container -->
    <div class="relative w-full max-w-[584px] rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-10">
      <!-- Close button -->
      <button 
        @click="$emit('close')" 
        class="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11"
      >
        <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z" fill=""></path>
        </svg>
      </button>
      
      <!-- Modal title -->
      <h4 class="mb-6 text-lg font-medium text-gray-800 dark:text-white/90">
        {{ title }}
      </h4>
      
      <!-- Modal content - uses default slot -->
      <div class="space-y-6">
        <slot></slot>
      </div>
      
      <!-- Modal footer -->
      <div class="flex items-center justify-end gap-3 mt-6">
        <slot name="footer">
          <button 
            type="button"
            @click="$emit('close')"
            class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
          >
            {{ cancelButtonText }}
          </button>
          <button 
            @click="$emit('save')"
            class="flex justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
            {{ isLoading ? loadingText : submitButtonText }}
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Modal Title'
  },
  cancelButtonText: {
    type: String,
    default: 'Close'
  },
  submitButtonText: {
    type: String,
    default: 'Save Changes'
  },
  loadingText: {
    type: String,
    default: 'Saving...'
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  maxWidth: {
    type: String,
    default: '584px'
  }
});

const emit = defineEmits(['close', 'save']);
</script>

<style scoped>
/* Add any modal-specific styles here */
</style> 