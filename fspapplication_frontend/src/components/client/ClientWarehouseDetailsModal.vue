<!-- Warehouse Details Modal -->
<template>
  <BaseModal 
    v-if="show"
    :title="warehouse.name" 
    :isLoading="isLoading"
    :showSubmitButton="isEditing"
    :submitButtonText="'Save Changes'"
    :loadingText="'Saving...'"
    :modalSize="'max-w-2xl'"
    @close="closeModal"
    @save="handleSave"
  >
    <!-- Two-part layout: scrollable content + fixed footer -->
    <div class="flex flex-col h-[calc(100vh-15rem)]">
      <!-- Scrollable Content Area with fixed height to maintain size -->
      <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar pb-4">
        <!-- Warehouse Information -->
        <div class="space-y-4">
          <!-- Basic Information -->
          <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Basic Information</h4>
            
            <div>
              <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Name</h5>
              <div v-if="isEditing" class="mt-1">
                <input
                  v-model="editedWarehouse.name"
                  type="text"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  placeholder="Enter warehouse name"
                />
              </div>
              <p v-else class="mt-1 text-base font-medium text-gray-900 dark:text-white">{{ warehouse.name }}</p>
            </div>
            
            <div class="mt-3">
              <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Description</h5>
              <div v-if="isEditing" class="mt-1">
                <textarea
                  v-model="editedWarehouse.description"
                  rows="3"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  placeholder="Enter warehouse description"
                ></textarea>
              </div>
              <p v-else class="mt-1 text-base text-gray-900 dark:text-white min-h-[4.5rem]">
                {{ warehouse.description || 'No description provided' }}
              </p>
            </div>
            
            <div class="mt-3">
              <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Type</h5>
              <div v-if="isEditing" class="mt-1">
                <select
                  v-model="editedWarehouse.isPrimary"
                  class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                >
                  <option :value="true">Primary Warehouse</option>
                  <option :value="false">Secondary Warehouse</option>
                </select>
              </div>
              <p v-else class="mt-1 text-base text-gray-900 dark:text-white min-h-[2.5rem]">
                {{ warehouse.isPrimary ? 'Primary Warehouse' : 'Secondary Warehouse' }}
              </p>
            </div>
            
            <div class="mt-3">
              <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</h5>
              <span 
                :class="[
                  'mt-1 inline-flex px-2.5 py-0.5 rounded-full text-sm font-medium min-h-[2rem]',
                  warehouse.isActive 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400' 
                    : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-400'
                ]"
              >
                {{ warehouse.isActive ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
          
          <!-- Location Information -->
          <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Location</h4>
            
            <div v-if="isEditing" class="min-h-[10rem]">
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
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Street Number</h5>
                  <input
                    v-model="editedWarehouse.streetNumber"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Street Name</h5>
                  <input
                    v-model="editedWarehouse.streetName"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Suburb</h5>
                  <input
                    v-model="editedWarehouse.suburb"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">City</h5>
                  <input
                    v-model="editedWarehouse.city"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">State/Province</h5>
                  <input
                    v-model="editedWarehouse.state"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Postal Code</h5>
                  <input
                    v-model="editedWarehouse.postalCode"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
                <div>
                  <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Country</h5>
                  <input
                    v-model="editedWarehouse.country"
                    type="text"
                    class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  />
                </div>
              </div>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-[10rem]">
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Address</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ formatAddress(warehouse) }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- Contact Information -->
          <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Contact Information</h4>
            
            <div v-if="isEditing" class="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-[10rem]">
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">First Name</h5>
                <input
                  v-model="editedWarehouse.firstName"
                  type="text"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                />
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Last Name</h5>
                <input
                  v-model="editedWarehouse.lastName"
                  type="text"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                />
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contact Phone</h5>
                <input
                  v-model="editedWarehouse.contactPhone"
                  type="tel"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                />
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contact Email</h5>
                <input
                  v-model="editedWarehouse.contactEmail"
                  type="email"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                />
              </div>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-[10rem]">
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contact Name</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ warehouse.contactName || formatNameFromParts(warehouse.firstName, warehouse.lastName) || 'Not specified' }}
                </p>
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contact Phone</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ warehouse.contactPhone || 'Not specified' }}
                </p>
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contact Email</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ warehouse.contactEmail || 'Not specified' }}
                </p>
              </div>
            </div>
          </div>
          
          <!-- Warehouse Details -->
          <div>
            <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">Warehouse Details</h4>
            
            <div v-if="isEditing" class="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-[10rem]">
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Operating Hours</h5>
                <input
                  v-model="editedWarehouse.operatingHours"
                  type="text"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  placeholder="e.g. Mon-Fri 9am-5pm"
                />
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Storage Capacity</h5>
                <input
                  v-model="editedWarehouse.storageCapacity"
                  type="text"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  placeholder="e.g. 1000 pallets / 500 sqm"
                />
              </div>
              <div class="md:col-span-2">
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Special Instructions</h5>
                <textarea
                  v-model="editedWarehouse.specialInstructions"
                  rows="3"
                  class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
                  placeholder="Enter special instructions"
                ></textarea>
              </div>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-[10rem]">
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Operating Hours</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ warehouse.operatingHours || 'Not specified' }}
                </p>
              </div>
              <div>
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Storage Capacity</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white">
                  {{ warehouse.storageCapacity || 'Not specified' }}
                </p>
              </div>
              <div class="md:col-span-2">
                <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Special Instructions</h5>
                <p class="mt-1 text-base text-gray-900 dark:text-white min-h-[4.5rem]">
                  {{ warehouse.specialInstructions || 'Not specified' }}
                </p>
              </div>
            </div>
          </div>
          
          <div>
            <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</h5>
            <p class="mt-1 text-base text-gray-900 dark:text-white">
              {{ warehouse.updatedAt ? new Date(warehouse.updatedAt).toLocaleDateString() : 'Unknown' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Fixed Action Buttons Footer -->
      <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700 mt-2 bg-white dark:bg-gray-800 py-3">
        <button
          v-if="!isEditing"
          @click="toggleStatus"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200',
            warehouse.isActive 
              ? 'text-white bg-red-600 hover:bg-red-700 focus:ring-red-500 dark:bg-red-500 dark:hover:bg-red-600'
              : 'text-white bg-green-600 hover:bg-green-700 focus:ring-green-500 dark:bg-green-500 dark:hover:bg-green-600'
          ]"
        >
          {{ warehouse.isActive ? 'Deactivate' : 'Activate' }}
        </button>
        <button
          v-if="!isEditing"
          @click="startEditing"
          class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400 dark:focus:ring-offset-gray-900 transition-colors duration-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit Warehouse
        </button>
        <button
          v-if="isEditing"
          @click="cancelEditing"
          class="px-4 py-2 text-sm font-medium rounded-lg text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
        >
          Cancel
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import BaseModal from '@/components/ui/BaseModal.vue';
import AddressAutocomplete from '@/components/common/AddressAutocomplete.vue';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Define the Warehouse interface
interface Warehouse {
  id: string;
  name: string;
  client: string;
  description: string | null;
  streetNumber: string | null;
  streetName: string | null;
  suburb: string | null;
  city: string | null;
  state: string | null;
  postalCode: string | null;
  country: string | null;
  latitude: number | null;
  longitude: number | null;
  firstName: string | null;
  lastName: string | null;
  contactName: string | null;
  contactPhone: string | null;
  contactEmail: string | null;
  isPrimary: boolean;
  operatingHours: string | null;
  storageCapacity: string | null;
  specialInstructions: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

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

const props = defineProps<{
  show: boolean;
  warehouse: Warehouse;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'status-updated', warehouse: Warehouse): void;
  (e: 'warehouse-updated', warehouse: Warehouse): void;
}>();

const isLoading = ref(false);
const isEditing = ref(false);
const editedWarehouse = reactive<Partial<Warehouse>>({});

// Helper function to handle address update from AddressAutocomplete
const handleAddressUpdate = (addressData: AddressData) => {
  console.log("Received address data:", addressData);
  
  // Extract components, handling potential undefined
  const components = addressData.components || {};

  // Reset address fields to ensure clean data
  editedWarehouse.streetNumber = '';
  editedWarehouse.streetName = '';
  editedWarehouse.suburb = '';
  editedWarehouse.city = '';
  editedWarehouse.state = '';
  editedWarehouse.postalCode = '';
  editedWarehouse.country = '';

  // Populate fields from components if available (using camelCase internally)
  if (components.streetNumber) {
    editedWarehouse.streetNumber = components.streetNumber;
  }
  
  if (components.route) {
    editedWarehouse.streetName = components.route;
  }
  
  // Extract from street if components aren't available
  if (addressData.street && !components.streetNumber && !components.route) {
    // Try to split the street into number and name
    const streetParts = addressData.street.trim().split(' ');
    if (streetParts.length > 1 && /^\d+$/.test(streetParts[0])) {
      editedWarehouse.streetNumber = streetParts[0];
      editedWarehouse.streetName = streetParts.slice(1).join(' ');
    } else {
      // If can't split, put everything in street name
      editedWarehouse.streetName = addressData.street;
    }
  }
  
  // Handle suburb (sublocality)
  if (components.sublocality) {
    editedWarehouse.suburb = components.sublocality;
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
        editedWarehouse.postalCode = lastPart;
        cityParts.pop(); // Remove postal code from parts
      }
      
      // Check if the second-to-last part looks like a state (e.g., NSW, VIC, QLD)
      if (cityParts.length >= 2) {
        const stateCandidate = cityParts[cityParts.length - 1];
        if (stateCandidate.length <= 3 && stateCandidate === stateCandidate.toUpperCase()) {
          editedWarehouse.state = stateCandidate;
          cityParts.pop(); // Remove state from parts
        }
      }
      
      // The rest is the suburb/city
      if (cityParts.length > 0) {
        editedWarehouse.suburb = cityParts.join(' ');
      }
    } else {
      // If simple format, use as city
      editedWarehouse.city = cityString;
    }
  }
  
  // Use locality as city if suburb has been populated from above and city isn't set yet
  if (components.locality && !editedWarehouse.city && editedWarehouse.suburb) {
    editedWarehouse.city = components.locality;
  } else if (components.locality && !editedWarehouse.suburb) {
    // If suburb isn't set yet, use locality as suburb
    editedWarehouse.suburb = components.locality;
  }
  
  // Prefer components for state and postal code if they're still empty
  if (!editedWarehouse.state) {
    editedWarehouse.state = addressData.state || components.administrativeAreaLevel1 || '';
  }
  
  if (!editedWarehouse.postalCode) {
    editedWarehouse.postalCode = addressData.postalCode || components.postalCode || '';
  }
  
  // Handle country
  editedWarehouse.country = addressData.country || components.country || '';
  
  // Save coordinates
  editedWarehouse.latitude = addressData.lat !== undefined ? addressData.lat : null;
  editedWarehouse.longitude = addressData.lng !== undefined ? addressData.lng : null;
  
  console.log("Updated warehouse data with address:", editedWarehouse);
};

// Helper function to format address
const formatAddress = (warehouse: Warehouse): string => {
  const parts = [];
  if (warehouse.streetNumber) parts.push(warehouse.streetNumber);
  if (warehouse.streetName) parts.push(warehouse.streetName);
  if (warehouse.suburb) parts.push(warehouse.suburb);
  if (warehouse.city) parts.push(warehouse.city);
  if (warehouse.state) parts.push(warehouse.state);
  if (warehouse.postalCode) parts.push(warehouse.postalCode);
  if (warehouse.country) parts.push(warehouse.country);
  
  return parts.length > 0 ? parts.join(', ') : 'No address specified';
};

// Helper function to format name from parts
const formatNameFromParts = (firstName: string | null, lastName: string | null): string => {
  if (!firstName && !lastName) return '';
  const parts = [];
  if (firstName) parts.push(firstName);
  if (lastName) parts.push(lastName);
  return parts.join(' ');
};

// Close modal and reset editing state
const closeModal = () => {
  isEditing.value = false;
  emit('close');
};

// Toggle warehouse status
const toggleStatus = async () => {
  try {
    isLoading.value = true;
    const response = await axios.patch(
      `${API_URL}/client/clients/${props.warehouse.client}/warehouses/${props.warehouse.id}/`,
      { is_active: !props.warehouse.isActive }
    );
    
    const updatedWarehouse = convertObjectKeysToCamel(response.data);
    emit('status-updated', updatedWarehouse);
  } catch (error) {
    console.error('Error updating warehouse status:', error);
  } finally {
    isLoading.value = false;
  }
};

// Start editing mode
const startEditing = () => {
  // Copy all warehouse properties to the editedWarehouse object
  Object.assign(editedWarehouse, props.warehouse);
  isEditing.value = true;
};

// Cancel editing
const cancelEditing = () => {
  isEditing.value = false;
};

// Handle form submission
const handleSave = async () => {
  try {
    isLoading.value = true;
    
    // Create a copy of the edited warehouse data to modify coordinates if needed
    const warehouseData = { ...editedWarehouse };
    
    // Format coordinates to ensure they don't exceed database limits
    if (warehouseData.latitude !== null && warehouseData.latitude !== undefined) {
      // Convert to number with 6 decimal places
      warehouseData.latitude = Number(parseFloat(String(warehouseData.latitude)).toFixed(6));
    }
    
    if (warehouseData.longitude !== null && warehouseData.longitude !== undefined) {
      // Convert to number with 9 decimal places
      warehouseData.longitude = Number(parseFloat(String(warehouseData.longitude)).toFixed(9));
    }
    
    // Convert to snake_case for API
    const apiData = convertObjectKeysToSnake(warehouseData);
    
    // Submit data to API
    const response = await axios.patch(
      `${API_URL}/client/clients/${props.warehouse.client}/warehouses/${props.warehouse.id}/`,
      apiData
    );
    
    // Convert response back to camelCase
    const updatedWarehouse = convertObjectKeysToCamel(response.data);
    
    // Emit update event
    emit('warehouse-updated', updatedWarehouse);
    
    // Exit editing mode
    isEditing.value = false;
  } catch (error) {
    console.error('Error updating warehouse:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Custom scrollbar styling for both light and dark mode */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 8px;
  border: 2px solid transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.7);
}

/* Dark mode scrollbar styles */
:root.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

:root.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(75, 85, 99, 0.5);
}

:root.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(75, 85, 99, 0.7);
}
</style> 