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
        <!-- Address Autocomplete -->
        <div class="space-y-2 mb-2 relative">
          <AddressAutocomplete
            v-model="addressData"
            label="Search Address"
            placeholder="Type to search for an address"
            @update:modelValue="populateAddressFields"
          />
        </div>
      
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
          
        <!-- Hidden fields (latitude, longitude) -->
        <input type="hidden" v-model="formData.latitude">
        <input type="hidden" v-model="formData.longitude">
          
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
import type { Client } from '@/service/clientService';
import AddressAutocomplete from '@/components/common/AddressAutocomplete.vue';
import { convertObjectKeysToSnake } from '@/utils/caseConverter';

const props = defineProps<{
  clientData: Client;
  isSaving: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save', data: Partial<Client>): void;
}>();

// Create a form data object from client data props
const formData = ref<Partial<Client>>({
  streetNumber: props.clientData.streetNumber || '',
  streetName: props.clientData.streetName || '',
  suburb: props.clientData.suburb || '',
  city: props.clientData.city || '',
  state: props.clientData.state || '',
  postalCode: props.clientData.postalCode || '',
  country: props.clientData.country || '',
  latitude: props.clientData.latitude,
  longitude: props.clientData.longitude
});

// Address autocomplete data
const addressData = ref<any>({});

// Function to populate form fields from selected address
const populateAddressFields = (data: any) => {
  if (!data) {
    // console.error('No address data received'); // Removed debugging
    return;
  }
  
  // Copy the existing form data to avoid losing current values
  const newFormData = { ...formData.value };
  
  // Handle street components
  if (data.street && typeof data.street === 'string' && data.street.trim() !== '') {
    const street = data.street.trim();
    const streetParts = street.split(' ');
    
    // If the street has a number, use it as street number and the rest as street name
    if (streetParts.length > 1 && !isNaN(parseInt(streetParts[0]))) {
      newFormData.streetNumber = streetParts[0];
      newFormData.streetName = streetParts.slice(1).join(' ');
    } else {
      newFormData.streetName = street;
    }
  } else if (data.components) {
    // Use components directly if available
    newFormData.streetNumber = data.components.street_number || '';
    newFormData.streetName = data.components.route || '';
  }
  
  // Handle city/suburb, state and postal code
  if (data.city) {
    // Sometimes city contains city + state + postal code (e.g. "Caloundra QLD 4551")
    const cityParts = data.city.split(' ');
    
    // Check if Australian address
    const isAustralianAddress = 
      (data.country && data.country.toLowerCase().includes('australia')) || 
      (cityParts.length > 1 && ['nsw', 'qld', 'sa', 'tas', 'vic', 'wa', 'act', 'nt'].includes(cityParts[cityParts.length - 2]?.toLowerCase()));
    
    if (isAustralianAddress) {
      // For Australian addresses, parse "Caloundra QLD 4551" format
      let suburb = '';
      let state = '';
      let postalCode = '';
      
      // Last part might be postal code if it's a number
      if (cityParts.length > 0 && /^\d+$/.test(cityParts[cityParts.length - 1])) {
        postalCode = cityParts.pop() || ''; // Remove and store postal code
      }
      
      // Second to last part might be state if it's 2-3 uppercase letters
      if (cityParts.length > 0 && /^[A-Z]{2,3}$/.test(cityParts[cityParts.length - 1])) {
        state = cityParts.pop() || ''; // Remove and store state
      }
      
      // Remaining parts form the suburb name
      suburb = cityParts.join(' ');
      
      newFormData.suburb = suburb;
      newFormData.state = state || data.state;
      newFormData.postalCode = postalCode || data.postal_code;
      newFormData.city = ''; // Leave city blank for Australian addresses
    } else {
      // For non-Australian addresses
      newFormData.city = data.city;
      newFormData.suburb = ''; // Leave suburb blank for non-Australian addresses
      newFormData.state = data.state;
      newFormData.postalCode = data.postal_code;
    }
  }
  
  // Set country if available
  if (data.country) {
    newFormData.country = data.country;
  }
  
  // Store coordinates if available
  if (data.lat !== undefined && data.lat !== null) {
    newFormData.latitude = data.lat;
  }
  
  if (data.lng !== undefined && data.lng !== null) {
    newFormData.longitude = data.lng;
  }
  
  // Store Google Place ID if available
  if (data.place_id) {
    newFormData.googlePlaceId = data.place_id;
  }
  
  // Update form data
  formData.value = newFormData;
};

// Initialize form data when props change
const initForm = () => {
  if (props.clientData) {
    formData.value = {
      streetNumber: props.clientData.streetNumber || '',
      streetName: props.clientData.streetName || '',
      suburb: props.clientData.suburb || '',
      city: props.clientData.city || '',
      state: props.clientData.state || '',
      postalCode: props.clientData.postalCode || '',
      country: props.clientData.country || '',
      latitude: props.clientData.latitude,
      longitude: props.clientData.longitude
    };
  };
};

// Handle form submission
const saveChanges = () => {
  // Copy the form data to avoid mutating the original
  const dataToSave = { ...formData.value };
  
  // Helper function to convert empty strings to null
  const nullIfEmpty = (value: string | null | undefined) => {
    if (value === undefined || value === null || value.trim() === '') {
      return null;
    }
    return value;
  };
  
  // Ensure all fields are properly formatted
  const formattedData: Partial<Client> = {
    streetNumber: nullIfEmpty(dataToSave.streetNumber),
    streetName: nullIfEmpty(dataToSave.streetName),
    suburb: nullIfEmpty(dataToSave.suburb),
    city: nullIfEmpty(dataToSave.city),
    state: nullIfEmpty(dataToSave.state),
    postalCode: nullIfEmpty(dataToSave.postalCode),
    country: nullIfEmpty(dataToSave.country),
    latitude: dataToSave.latitude,
    longitude: dataToSave.longitude,
    googlePlaceId: nullIfEmpty(dataToSave.googlePlaceId)
  };
  
  // Format coordinates as numbers with correct decimal precision
  if (formattedData.latitude !== null && formattedData.latitude !== undefined) {
    if (typeof formattedData.latitude === 'string') {
      formattedData.latitude = parseFloat(formattedData.latitude);
    }
    if (!isNaN(formattedData.latitude)) {
      formattedData.latitude = parseFloat(formattedData.latitude.toFixed(6));
    } else {
      formattedData.latitude = null;
    }
  }
  
  if (formattedData.longitude !== null && formattedData.longitude !== undefined) {
    if (typeof formattedData.longitude === 'string') {
      formattedData.longitude = parseFloat(formattedData.longitude);
    }
    if (!isNaN(formattedData.longitude)) {
      formattedData.longitude = parseFloat(formattedData.longitude.toFixed(6));
    } else {
      formattedData.longitude = null;
    }
  }
  
  emit('save', formattedData);
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

// Watch for changes in clientData
watch(() => props.clientData, initForm, { immediate: true });
</script> 