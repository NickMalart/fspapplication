<!-- Warehouse Details Modal -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full dark:bg-gray-800">
        <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <div class="flex justify-between items-center">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white" id="modal-title">
                  {{ warehouse.name }}
                </h3>
                <span 
                  :class="[
                    'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                    warehouse.isActive 
                      ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400' 
                      : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-400'
                  ]"
                >
                  {{ warehouse.isActive ? 'Active' : 'Inactive' }}
                </span>
              </div>
              
              <div class="mt-4 space-y-4">
                <!-- Basic Information -->
                <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Basic Information</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Description</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.description || 'No description' }}</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Type</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.isPrimary ? 'Primary Warehouse' : 'Secondary Warehouse' }}</p>
                    </div>
                  </div>
                </div>
                
                <!-- Location Information -->
                <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Location</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Address</p>
                      <p class="text-sm text-gray-900 dark:text-white">
                        {{ formatAddress(warehouse) }}
                      </p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Coordinates</p>
                      <p class="text-sm text-gray-900 dark:text-white">
                        {{ warehouse.latitude && warehouse.longitude 
                          ? `${warehouse.latitude}, ${warehouse.longitude}` 
                          : 'Not specified' }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Contact Information -->
                <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Contact Information</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Contact Name</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.contactName || 'Not specified' }}</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Contact Phone</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.contactPhone || 'Not specified' }}</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Contact Email</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.contactEmail || 'Not specified' }}</p>
                    </div>
                  </div>
                </div>
                
                <!-- Warehouse Details -->
                <div>
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Warehouse Details</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Operating Hours</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.operatingHours || 'Not specified' }}</p>
                    </div>
                    <div>
                      <p class="text-sm text-gray-500 dark:text-gray-400">Storage Capacity</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.storageCapacity || 'Not specified' }}</p>
                    </div>
                    <div class="md:col-span-2">
                      <p class="text-sm text-gray-500 dark:text-gray-400">Special Instructions</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ warehouse.specialInstructions || 'Not specified' }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button 
            type="button" 
            @click="$emit('close')"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400 dark:focus:ring-offset-gray-700"
          >
            Close
          </button>
          <button 
            type="button" 
            @click="toggleStatus"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm dark:bg-gray-800 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-blue-400 dark:focus:ring-offset-gray-700"
          >
            {{ warehouse.isActive ? 'Deactivate' : 'Activate' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

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

const props = defineProps<{
  show: boolean;
  warehouse: Warehouse;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'status-updated', warehouse: Warehouse): void;
  (e: 'warehouse-updated', warehouse: Warehouse): void;
}>();

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

// Toggle warehouse status
const toggleStatus = async () => {
  try {
    const response = await axios.patch(
      `${API_URL}/client/clients/${props.warehouse.client}/warehouses/${props.warehouse.id}/`,
      { is_active: !props.warehouse.isActive }
    );
    
    const updatedWarehouse = convertObjectKeysToCamel(response.data);
    emit('status-updated', updatedWarehouse);
  } catch (error) {
    console.error('Error updating warehouse status:', error);
  }
};
</script> 