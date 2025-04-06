<!-- Warehouse Create Modal -->
<template>
  <BaseModal 
    v-if="show"
    :title="`Create New Warehouse for ${clientName}`"
    :isLoading="isLoading"
    :submitButtonText="'Create Warehouse'"
    :loadingText="'Creating...'"
    :modalSize="'max-w-2xl'"  
    @close="$emit('close')"
    @save="handleSubmit"
  >
    <!-- Scrollable Content Area -->
    <div class="max-h-[calc(100vh-15rem)] overflow-y-auto pr-2"> 
      <!-- Form starts here -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Error alert -->
        <div v-if="error" class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-900 text-red-700 dark:text-red-300 px-4 py-3 rounded relative mb-4">
          {{ error }}
        </div>
        
        <!-- Basic Information -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Basic Information</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Name*</label>
              <input 
                type="text" 
                id="name" 
                v-model="formData.name" 
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="isPrimary" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Type</label>
              <select 
                id="isPrimary" 
                v-model="formData.isPrimary"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              >
                <option :value="false">Secondary Warehouse</option>
                <option :value="true">Primary Warehouse</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Description</label>
              <textarea 
                id="description" 
                v-model="formData.description" 
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              ></textarea>
            </div>
          </div>
        </div>
        
        <!-- Location Information -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Location Information</h4>
          
          <!-- Address Autocomplete -->
          <div class="mb-4">
            <AddressAutocomplete 
              label="Search Address"
              placeholder="Start typing to search..."
              id="warehouse-address-autocomplete"
              @update:modelValue="handleAddressUpdate"
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="streetNumber" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Street Number</label>
              <input 
                type="text" 
                id="streetNumber" 
                v-model="formData.streetNumber"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="streetName" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Street Name</label>
              <input 
                type="text" 
                id="streetName" 
                v-model="formData.streetName"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="suburb" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Suburb</label>
              <input 
                type="text" 
                id="suburb" 
                v-model="formData.suburb"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="city" class="block text-sm font-medium text-gray-700 dark:text-gray-300">City</label>
              <input 
                type="text" 
                id="city" 
                v-model="formData.city"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="state" class="block text-sm font-medium text-gray-700 dark:text-gray-300">State/Province</label>
              <input 
                type="text" 
                id="state" 
                v-model="formData.state"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="postalCode" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Postal Code</label>
              <input 
                type="text" 
                id="postalCode" 
                v-model="formData.postalCode"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="country" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Country</label>
              <input 
                type="text" 
                id="country" 
                v-model="formData.country"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <!-- Latitude and Longitude fields are removed from UI but values are still stored -->
            <!--
            <div>
              <label for="latitude" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Latitude</label>
              <input 
                type="number" 
                step="0.000001"
                id="latitude" 
                v-model="formData.latitude"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="longitude" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Longitude</label>
              <input 
                type="number" 
                step="0.000001"
                id="longitude" 
                v-model="formData.longitude"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            -->
          </div>
        </div>
        
        <!-- Contact Information -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Contact Information</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="contactName" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contact Name</label>
              <input 
                type="text" 
                id="contactName" 
                v-model="formData.contactName"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="contactPhone" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contact Phone</label>
              <input 
                type="tel" 
                id="contactPhone" 
                v-model="formData.contactPhone"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="contactEmail" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Contact Email</label>
              <input 
                type="email" 
                id="contactEmail" 
                v-model="formData.contactEmail"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
          </div>
        </div>
        
        <!-- Warehouse Details -->
        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Warehouse Details</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="operatingHours" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Operating Hours</label>
              <input 
                type="text" 
                id="operatingHours" 
                v-model="formData.operatingHours"
                placeholder="e.g. Mon-Fri 9am-5pm"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div>
              <label for="storageCapacity" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Storage Capacity</label>
              <input 
                type="text" 
                id="storageCapacity" 
                v-model="formData.storageCapacity"
                placeholder="e.g. 1000 sq ft, 500 pallets"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              />
            </div>
            <div class="md:col-span-2">
              <label for="specialInstructions" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Special Instructions</label>
              <textarea 
                id="specialInstructions" 
                v-model="formData.specialInstructions" 
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              ></textarea>
            </div>
          </div>
        </div>
      </form>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import BaseModal from '@/components/ui/BaseModal.vue'; // Import BaseModal
import AddressAutocomplete from '@/components/common/AddressAutocomplete.vue'; // Import AddressAutocomplete

const API_URL = import.meta.env.VITE_API_URL || '/api';

const props = defineProps<{
  show: boolean;
  clientId: string;
  clientName: string;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'warehouse-created', warehouse: any): void;
}>();

// Form data state
const formData = ref({
  name: '',
  description: '',
  streetNumber: '',
  streetName: '',
  suburb: '',
  city: '',
  state: '',
  postalCode: '',
  country: '',
  latitude: null as number | null,
  longitude: null as number | null,
  contactName: '',
  contactPhone: '',
  contactEmail: '',
  isPrimary: true,
  operatingHours: '',
  storageCapacity: '',
  specialInstructions: '',
  isActive: true
});

// Type for the address data received from AddressAutocomplete
interface AddressData {
  formattedAddress?: string;
  components?: { 
    streetNumber?: string;
    route?: string; // Often used for street name
    locality?: string; // Often used for city
    sublocality?: string; // Often used for suburb
    administrativeAreaLevel1?: string; // Often used for state
    country?: string;
    postalCode?: string;
    [key: string]: string | undefined; // Allow other component types
  };
  street?: string; // Potentially formatted street
  city?: string;
  state?: string;
  country?: string;
  postalCode?: string;
  lat?: number | null;
  lng?: number | null;
  placeId?: string; 
}

const isLoading = ref(false);
const error = ref('');

// Reset form when modal is opened
watch(() => props.show, (newVal) => {
  if (newVal) {
    resetForm();
  }
});

const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    streetNumber: '',
    streetName: '',
    suburb: '',
    city: '',
    state: '',
    postalCode: '',
    country: '',
    latitude: null,
    longitude: null,
    contactName: '',
    contactPhone: '',
    contactEmail: '',
    isPrimary: true,
    operatingHours: '',
    storageCapacity: '',
    specialInstructions: '',
    isActive: true
  };
  error.value = '';
};

// Handle address update from AddressAutocomplete
const handleAddressUpdate = (addressData: AddressData) => {
  console.log("Received address data:", addressData);
  
  // Extract components, handling potential undefined
  const components = addressData.components || {};

  // Reset address fields to ensure clean data
  formData.value.streetNumber = '';
  formData.value.streetName = '';
  formData.value.suburb = '';
  formData.value.city = '';
  formData.value.state = '';
  formData.value.postalCode = '';
  formData.value.country = '';

  // Populate fields from components if available (using camelCase internally)
  if (components.streetNumber) {
    formData.value.streetNumber = components.streetNumber;
  }
  
  if (components.route) {
    formData.value.streetName = components.route;
  }
  
  // Extract from street if components aren't available
  if (addressData.street && !components.streetNumber && !components.route) {
    // Try to split the street into number and name
    const streetParts = addressData.street.trim().split(' ');
    if (streetParts.length > 1 && /^\d+$/.test(streetParts[0])) {
      formData.value.streetNumber = streetParts[0];
      formData.value.streetName = streetParts.slice(1).join(' ');
    } else {
      // If can't split, put everything in street name
      formData.value.streetName = addressData.street;
    }
  }
  
  // Handle suburb (sublocality)
  if (components.sublocality) {
    formData.value.suburb = components.sublocality;
  }
  
  // For Australian addresses, parse city to extract suburb, state and postal code
  // Example format: "Chippendale NSW 2008"
  if (addressData.city) {
    const cityString = addressData.city;
    const cityParts = cityString.trim().split(' ');
    
    if (cityParts.length >= 2) {
      // Check if the last part is a postal code (numbers only)
      const lastPart = cityParts[cityParts.length - 1];
      if (/^\d+$/.test(lastPart)) {
        formData.value.postalCode = lastPart;
        cityParts.pop(); // Remove postal code from parts
      }
      
      // Check if the second-to-last part looks like a state (e.g., NSW, VIC, QLD)
      if (cityParts.length >= 2) {
        const stateCandidate = cityParts[cityParts.length - 1];
        if (stateCandidate.length <= 3 && stateCandidate === stateCandidate.toUpperCase()) {
          formData.value.state = stateCandidate;
          cityParts.pop(); // Remove state from parts
        }
      }
      
      // The rest is the suburb/city
      if (cityParts.length > 0) {
        formData.value.suburb = cityParts.join(' ');
      }
    } else {
      // If simple format, use as city
      formData.value.city = cityString;
    }
  }
  
  // Use locality as city if suburb has been populated from above and city isn't set yet
  if (components.locality && !formData.value.city && formData.value.suburb) {
    formData.value.city = components.locality;
  } else if (components.locality && !formData.value.suburb) {
    // If suburb isn't set yet, use locality as suburb
    formData.value.suburb = components.locality;
  }
  
  // Prefer components for state and postal code if they're still empty
  if (!formData.value.state) {
    formData.value.state = addressData.state || components.administrativeAreaLevel1 || '';
  }
  
  if (!formData.value.postalCode) {
    formData.value.postalCode = addressData.postalCode || components.postalCode || '';
  }
  
  // Handle country
  formData.value.country = addressData.country || components.country || '';
  
  // Save coordinates
  formData.value.latitude = addressData.lat !== undefined ? addressData.lat : null;
  formData.value.longitude = addressData.lng !== undefined ? addressData.lng : null;
  
  console.log("Updated form data with address:", formData.value);
};

// Handle form submission (triggered by BaseModal @save event)
const handleSubmit = async () => {
  if (!formData.value.name) {
    error.value = 'Warehouse name is required';
    return;
  }
  
  isLoading.value = true;
  error.value = '';
  
  try {
    // Convert form data to snake_case for API using the utility
    const apiData = convertObjectKeysToSnake(formData.value);
    
    // Add client ID to the data
    apiData.client = props.clientId;
    
    // Submit data to API
    const response = await axios.post(
      `${API_URL}/client/clients/${props.clientId}/warehouses/`,
      apiData
    );
    
    // Convert response to camelCase
    const createdWarehouse = convertObjectKeysToCamel(response.data);
    
    // Emit event with created warehouse data
    emit('warehouse-created', createdWarehouse);
    
    // Close modal
    emit('close');
  } catch (err: any) {
    console.error('Error creating warehouse:', err);
    error.value = err.response?.data?.detail || 'Failed to create warehouse. Please try again.';
  } finally {
    isLoading.value = false;
  }
};
</script> 