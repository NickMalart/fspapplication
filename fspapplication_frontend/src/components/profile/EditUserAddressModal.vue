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
        Edit Address Information
      </h4>
      
      <form @submit.prevent="saveChanges" class="space-y-6">
        <!-- Street Number & Name -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="md:col-span-1 space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Street Number</label>
            <input 
              v-model="formData.streetNumber"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter street number"
            />
          </div>
          <div class="md:col-span-2 space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Street Name</label>
            <input 
              v-model="formData.streetName"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter street name"
            />
          </div>
        </div>
        
        <!-- Suburb & City -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Suburb</label>
            <input 
              v-model="formData.suburb"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter suburb"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">City</label>
            <input 
              v-model="formData.city"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter city"
            />
          </div>
        </div>
        
        <!-- State & Postal Code -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">State/Province</label>
            <input 
              v-model="formData.state"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter state/province"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Postal Code</label>
            <input 
              v-model="formData.postalCode"
              type="text" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter postal code"
            />
          </div>
        </div>
        
        <!-- Country -->
        <div class="space-y-2">
          <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Country</label>
          <input 
            v-model="formData.country"
            type="text" 
            class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            placeholder="Enter country"
          />
        </div>
          
        <!-- Hidden fields (latitude, longitude, googlePlaceId) -->
        <input type="hidden" v-model="formData.latitude">
        <input type="hidden" v-model="formData.longitude">
        <input type="hidden" v-model="formData.googlePlaceId">
          
        <!-- Form Actions -->
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
import { ref, onMounted, watch } from 'vue';
import { ProfileData } from '@/service/userProfileService';

const props = defineProps<{
  userData: ProfileData;
  isSaving: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save', data: Partial<ProfileData>): void;
}>();

// Create a form data object from user data props
const formData = ref<Partial<ProfileData>>({
  streetNumber: props.userData.streetNumber || '',
  streetName: props.userData.streetName || '',
  suburb: props.userData.suburb || '',
  city: props.userData.city || '',
  state: props.userData.state || '',
  postalCode: props.userData.postalCode || '',
  country: props.userData.country || '',
  latitude: props.userData.latitude,
  longitude: props.userData.longitude,
  googlePlaceId: props.userData.googlePlaceId
});

// Initialize form data when props change
const initForm = () => {
  if (props.userData) {
    formData.value = {
      streetNumber: props.userData.streetNumber || '',
      streetName: props.userData.streetName || '',
      suburb: props.userData.suburb || '',
      city: props.userData.city || '',
      state: props.userData.state || '',
      postalCode: props.userData.postalCode || '',
      country: props.userData.country || '',
      latitude: props.userData.latitude,
      longitude: props.userData.longitude,
      googlePlaceId: props.userData.googlePlaceId
    };
    
    console.log('Initialized address form data:', formData.value);
  }
};

// Handle form submission
const saveChanges = () => {
  console.log('Saving address changes:', formData.value);
  emit('save', formData.value);
};

// Add keyboard event listener for Escape key
onMounted(() => {
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
      emit('close');
    }
  };
  
  window.addEventListener('keydown', handleKeyDown);
  initForm();
  
  // Clean up event listener on component unmount
  return () => {
    window.removeEventListener('keydown', handleKeyDown);
  };
});

// Watch for changes in userData
watch(() => props.userData, initForm, { immediate: true });
</script>
