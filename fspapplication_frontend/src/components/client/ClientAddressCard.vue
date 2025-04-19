<template>
  <ComponentCard title="Address Information">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-900 text-red-700 dark:text-red-300 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Data Display with Edit Button in Relative Position -->
    <div v-else class="relative">
      <!-- Edit Button -->
      <button 
        v-if="client" 
        @click="isModalOpen = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="client" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <!-- Street Address -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Street Address</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatStreetAddress(client) }}
          </p>
        </div>
        
        <!-- Suburb/City -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Suburb/City</p>
          <p class="font-medium text-black dark:text-white">
            {{ client.suburb || client.city || 'Not provided' }}
          </p>
        </div>
        
        <!-- State/Province -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">State/Province</p>
          <p class="font-medium text-black dark:text-white">
            {{ client.state || 'Not provided' }}
          </p>
        </div>
        
        <!-- Postal Code -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Postal Code</p>
          <p class="font-medium text-black dark:text-white">
            {{ client.postalCode || 'Not provided' }}
          </p>
        </div>
        
        <!-- Country -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Country</p>
          <p class="font-medium text-black dark:text-white">
            {{ client.country || 'Not provided' }}
          </p>
        </div>
      </div>
      <!-- Map Container - Show if client has coordinates -->
      <div v-show="client && client.latitude && client.longitude" class="mt-6 relative"> 
        <div 
          ref="mapContainer" 
          class="h-32 w-32 rounded-md border border-gray-300 dark:border-gray-600 cursor-pointer overflow-hidden" 
          @click="isMapViewerOpen = true" 
        ></div>
      </div>
      <!-- No Address Message - Show if loading is done and client is null or has no coordinates -->
      <div v-if="!loading && (!client || !client.latitude || !client.longitude)" class="py-4 text-center text-gray-500">
        No map available (missing coordinates)
      </div>
    </div>

    <!-- Edit Modal with key to force re-render -->
    <EditClientAddressModal
      v-if="isModalOpen && client"
      :key="modalKey"
      :client-data="client"
      :is-saving="isSaving"
      @close="isModalOpen = false"
      @save="handleSave"
    />
    
    <!-- Map Viewer Modal -->
    <MapViewerModal
      v-if="isMapViewerOpen && client && client.latitude && client.longitude"
      :show="isMapViewerOpen"
      :latitude="client.latitude"
      :longitude="client.longitude"
      :title="`${client.name || 'Client'} Location`"
      @close="isMapViewerOpen = false"
    />
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue';
import { useClientStore } from '@/stores/clientStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';
import EditClientAddressModal from './EditClientAddressModal.vue';
import MapViewerModal from '@/components/common/MapViewerModal.vue';
import type { Client } from '@/service/clientService';
import 'leaflet/dist/leaflet.css'; // Import Leaflet CSS
import L from 'leaflet'; // Import Leaflet

const props = defineProps<{
  clientId: string;
}>();

const clientStore = useClientStore();
const { loading, error } = storeToRefs(clientStore);

const client = computed(() => clientStore.getClientById(props.clientId));
const isModalOpen = ref(false);
const isSaving = ref(false);
const modalKey = ref(0); // Used to force modal re-render
const mapContainer = ref<HTMLElement | null>(null); // Ref for map container element
const mapInstance = ref<L.Map | null>(null); // Ref for map instance
const isMapViewerOpen = ref(false); // State for the map viewer modal

// Format street address
const formatStreetAddress = (client: Client) => {
  if (!client.streetNumber && !client.streetName) return 'Not provided';
  
  let address = '';
  if (client.streetNumber) address += client.streetNumber;
  if (client.streetNumber && client.streetName) address += ' ';
  if (client.streetName) address += client.streetName;
  
  return address;
};

// Handle save from modal
const handleSave = async (formData: Partial<Client>) => {
  isSaving.value = true;
  
  try {
    
    // Create a properly formatted address data object
    const addressData: Partial<Client> = {
      streetNumber: formData.streetNumber,
      streetName: formData.streetName,
      suburb: formData.suburb,
      city: formData.city,
      state: formData.state,
      postalCode: formData.postalCode,
      country: formData.country,
      latitude: formData.latitude,
      longitude: formData.longitude,
      googlePlaceId: formData.googlePlaceId
    };
    
    // Update client through store
    await clientStore.updateClient(props.clientId, addressData);
    
    // Increment key to force modal re-render on next open
    modalKey.value++;
    
    // Close modal
    isModalOpen.value = false;
    
    // Force refresh client data
    await clientStore.fetchClients();
  } catch (error) {
    console.error('Failed to save address changes:', error);
  } finally {
    isSaving.value = false;
  }
};

// Fetch client data on mount if not already in store
onMounted(async () => {
  if (!client.value) {
    await clientStore.fetchClients();
  }
});

// Force refetch when modal closes
watch(isModalOpen, (open) => {
  if (!open) {
    clientStore.fetchClients();
  }
});

// Function to initialize Leaflet map
const initMap = () => {
  const currentClient = client.value;
  if (mapContainer.value && currentClient && currentClient.latitude && currentClient.longitude && !mapInstance.value) {
    mapInstance.value = L.map(mapContainer.value, {
      attributionControl: false, // Disable Leaflet attribution
      scrollWheelZoom: false, // Disable scroll wheel zoom
      zoomControl: false // Disable zoom control (+/- buttons)
    }).setView(
      [currentClient.latitude, currentClient.longitude],
      13 // Zoom level
    );

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapInstance.value as L.Map);

    // Add marker
    L.marker([currentClient.latitude, currentClient.longitude]).addTo(mapInstance.value as L.Map);
  }
};

// Function to destroy Leaflet map
const destroyMap = () => {
  if (mapInstance.value) {
    mapInstance.value.remove();
    mapInstance.value = null;
  }
};

// Watch for changes in client data to update the map
watch(client, (newClient, oldClient) => {
  if (newClient && newClient.latitude && newClient.longitude) {
    // If client data is available and has coordinates
    if (!mapInstance.value || 
        (oldClient && (newClient.latitude !== oldClient.latitude || newClient.longitude !== oldClient.longitude))) {
      // Initialize map if it doesn't exist or coordinates changed
      nextTick(() => {
        destroyMap(); // Ensure old instance is removed before creating new
        initMap();
      });
    }
  } else {
    // If no client or no coordinates, destroy the map
    destroyMap();
  }
}, { immediate: true, deep: true }); // immediate: true to run on load, deep to watch nested props like lat/lng

// Ensure map is destroyed when component unmounts
onUnmounted(() => {
  destroyMap();
});
</script> 