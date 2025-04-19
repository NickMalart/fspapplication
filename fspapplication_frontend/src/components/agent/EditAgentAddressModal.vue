<template>
  <div class="fixed inset-0 flex items-center justify-center p-5 overflow-y-auto modal z-99999">
    <!-- Backdrop -->
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>
    <!-- Modal Content -->
    <div class="relative w-full max-w-[584px] rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-10">
      <!-- Close Button (Copied from EditClientAddressModal) -->
      <button 
        @click="$emit('close')" 
        class="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11"
      >
        <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z" fill=""></path>
        </svg>
      </button>

      <!-- Modal Title -->
      <h4 class="mb-6 text-lg font-medium text-gray-800 dark:text-white/90">
        Edit Agent Address
      </h4>

      <!-- Form -->
      <form @submit.prevent="submitForm" novalidate class="space-y-6">
        <!-- Address Autocomplete -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Search Address</label>
          <AddressAutocomplete
            :id="'agent-address-search'" 
            label="" 
            placeholder="Start typing to search..."
            :modelValue="addressData" 
            @update:modelValue="handleAddressUpdate" 
          />
        </div>
        
        <!-- Address Fields -->
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label for="streetNumber" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Street Number</label>
            <input 
              type="text" 
              id="streetNumber" 
              v-model="formData.streetNumber" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter street number"
            />
          </div>
          <div>
            <label for="streetName" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Street Name</label>
            <input 
              type="text" 
              id="streetName" 
              v-model="formData.streetName" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter street name"
            />
          </div>
          <div>
            <label for="suburb" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Suburb</label>
            <input 
              type="text" 
              id="suburb" 
              v-model="formData.suburb" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter suburb"
            />
          </div>
          <div>
            <label for="city" class="block text-sm font-medium text-gray-700 dark:text-gray-300">City</label>
            <input 
              type="text" 
              id="city" 
              v-model="formData.city" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter city"
            />
          </div>
          <div>
            <label for="state" class="block text-sm font-medium text-gray-700 dark:text-gray-300">State/Province</label>
            <input 
              type="text" 
              id="state" 
              v-model="formData.state" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter state/province"
            />
          </div>
          <div>
            <label for="postalCode" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Postal Code</label>
            <input 
              type="text" 
              id="postalCode" 
              v-model="formData.postalCode" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter postal code"
            />
          </div>
          <div class="sm:col-span-2">
            <label for="country" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Country</label>
            <input 
              type="text" 
              id="country" 
              v-model="formData.country" 
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              placeholder="Enter country"
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-4 text-sm text-red-600 dark:text-red-400">
          {{ errorMessage }}
        </div>

        <!-- Buttons (Copied structure/classes from EditClientAddressModal) -->
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
import { ref, reactive, watch } from 'vue';
// import Modal from '@/components/ui/BaseModal.vue'; // Remove BaseModal import
import AddressAutocomplete from '@/components/common/AddressAutocomplete.vue';
import type { Agent } from '@/service/agentService';

// Interface for the data received from AddressAutocomplete
interface AddressData {
  formatted_address?: string;
  components?: { 
    street_number?: string;
    route?: string; 
    locality?: string; 
    sublocality?: string;
    administrative_area_level_1?: string; 
    country?: string;
    postal_code?: string;
    [key: string]: string | undefined; 
  };
  street?: string;
  city?: string;
  state?: string;
  country?: string;
  postal_code?: string;
  lat?: number | null;
  lng?: number | null;
  place_id?: string; 
}

// Define props
const props = defineProps<{
  agentData: Agent;
  isSaving: boolean;
}>();

// Add a watcher for the isSaving prop
watch(() => props.isSaving, (newValue, oldValue) => {
  console.log(`--- EditAgentAddressModal: isSaving prop changed from ${oldValue} to ${newValue} ---`);
});

// Log initial value on setup
console.log(`--- EditAgentAddressModal: Initial isSaving prop value: ${props.isSaving} ---`);

// Define emits
const emit = defineEmits(['close', 'save']);

// Reactive form data, initialized with agentData
const formData = reactive<Partial<Agent>>({
  streetNumber: props.agentData.streetNumber || '',
  streetName: props.agentData.streetName || '',
  suburb: props.agentData.suburb || '',
  city: props.agentData.city || '',
  state: props.agentData.state || '',
  postalCode: props.agentData.postalCode || '',
  country: props.agentData.country || '',
  latitude: props.agentData.latitude || null,
  longitude: props.agentData.longitude || null,
});

const addressData = ref({}); // To bind with AddressAutocomplete's modelValue
const errorMessage = ref<string | null>(null);

// Watch for prop changes to reset form if needed
watch(() => props.agentData, (newData) => {
  Object.assign(formData, {
    streetNumber: newData.streetNumber || '',
    streetName: newData.streetName || '',
    suburb: newData.suburb || '',
    city: newData.city || '',
    state: newData.state || '',
    postalCode: newData.postalCode || '',
    country: newData.country || '',
    latitude: newData.latitude || null,
    longitude: newData.longitude || null,
  });
  addressData.value = {}; // Clear autocomplete state
  errorMessage.value = null; // Clear error
}, { deep: true });

// Handle address update from autocomplete
const handleAddressUpdate = (data: AddressData | null) => {
  if (!data) {
    errorMessage.value = 'Could not fetch address details.';
    return;
  }
  errorMessage.value = null;
  addressData.value = data; // Keep addressData ref updated

  // Update form fields based on received data - Using logic from EditClientAddressModal
  const newFormData = { ...formData }; // Copy existing form data

  // Handle street components
  if (data.street && typeof data.street === 'string' && data.street.trim() !== '') {
    const street = data.street.trim();
    const streetParts = street.split(' ');
    if (streetParts.length > 1 && !isNaN(parseInt(streetParts[0]))) {
      newFormData.streetNumber = streetParts[0];
      newFormData.streetName = streetParts.slice(1).join(' ');
    } else {
      newFormData.streetName = street;
      newFormData.streetNumber = ''; // Clear street number if only street name is found
    }
  } else if (data.components) {
    newFormData.streetNumber = data.components.street_number || '';
    newFormData.streetName = data.components.route || '';
  }
  
  // Handle city/suburb, state and postal code
  // Prioritize components if available
  newFormData.suburb = data.components?.sublocality || '';
  newFormData.city = data.components?.locality || '';
  newFormData.state = data.components?.administrative_area_level_1 || '';
  newFormData.postalCode = data.components?.postal_code || '';
  newFormData.country = data.components?.country || '';

  // Fallback and parse top-level city field if needed (especially for formats like Australian)
  if ((!newFormData.suburb && !newFormData.city) || !newFormData.state || !newFormData.postalCode) {
      if (data.city && typeof data.city === 'string') {
          const cityField = data.city.trim();
          const cityParts = cityField.split(' ');
          
          const isAustralianAddress = 
              (data.country && data.country.toLowerCase().includes('australia')) || 
              (cityParts.length > 1 && /^[A-Z]{2,3}$/.test(cityParts[cityParts.length - 2])); // Check second last part for state code

          if (isAustralianAddress) {
              let parsedSuburb = '';
              let parsedState = '';
              let parsedPostalCode = '';
              let tempParts = [...cityParts]; // Create a copy to modify

              // Last part might be postal code
              if (tempParts.length > 0 && /^\d+$/.test(tempParts[tempParts.length - 1])) {
                  parsedPostalCode = tempParts.pop() || '';
              }
              // Second to last part might be state
              if (tempParts.length > 0 && /^[A-Z]{2,3}$/.test(tempParts[tempParts.length - 1])) {
                  parsedState = tempParts.pop() || '';
              }
              // Remaining is suburb
              parsedSuburb = tempParts.join(' ');

              newFormData.suburb = newFormData.suburb || parsedSuburb;
              newFormData.state = newFormData.state || parsedState;
              newFormData.postalCode = newFormData.postalCode || parsedPostalCode;
              newFormData.city = ''; // Clear city for AU addresses when suburb is found
          } else {
              // Non-Australian or unparsable format, use top-level fields as fallback
              newFormData.city = newFormData.city || data.city || '';
              newFormData.state = newFormData.state || data.state || '';
              newFormData.postalCode = newFormData.postalCode || data.postal_code || '';
          }
      } else {
         // Use other top-level fields if city parsing didn't yield results
         newFormData.state = newFormData.state || data.state || '';
         newFormData.postalCode = newFormData.postalCode || data.postal_code || '';
      }
  }
  
  // Use top-level country as final fallback
  newFormData.country = newFormData.country || data.country || '';

  // Update coordinates
  newFormData.latitude = data.lat !== undefined ? data.lat : null;
  newFormData.longitude = data.lng !== undefined ? data.lng : null;

  // Update the actual form data reactive object
  Object.assign(formData, newFormData);
};

// Submit form data
const submitForm = () => {
  errorMessage.value = null; // Clear previous error
  if (!formData.streetName && !formData.city) {
      errorMessage.value = 'Please provide at least a street name or city.';
      return;
  }
  console.log("--- EditAgentAddressModal: submitForm called ---");
  console.log("Emitting save event with data:", JSON.stringify(formData, null, 2));
  emit('save', { ...formData });
};
</script> 