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
        v-if="agent" 
        @click="isModalOpen = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
        aria-label="Edit Address"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="agent" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <!-- Street Address -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Street Address</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatStreetAddress(agent) }}
          </p>
        </div>
        
        <!-- Suburb/City -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Suburb/City</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.suburb || agent.city || 'Not provided' }}
          </p>
        </div>
        
        <!-- State/Province -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">State/Province</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.state || 'Not provided' }}
          </p>
        </div>
        
        <!-- Postal Code -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Postal Code</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.postalCode || 'Not provided' }}
          </p>
        </div>
        
        <!-- Country -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Country</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.country || 'Not provided' }}
          </p>
        </div>
      </div>
      <!-- Map Container - Show if agent has coordinates -->
      <div v-show="agent && agent.latitude && agent.longitude" class="mt-6 relative"> 
        <div 
          ref="mapContainer" 
          class="h-32 w-32 rounded-md border border-gray-300 dark:border-gray-600 cursor-pointer overflow-hidden" 
          @click="isMapViewerOpen = true" 
        ></div>
      </div>
      <!-- No Address Message - Show if loading is done and agent is null or has no coordinates -->
      <div v-if="!loading && (!agent || !agent.latitude || !agent.longitude)" class="py-4 text-center text-gray-500">
        No map available (missing coordinates)
      </div>
       <!-- Display No Agent Data if agent is null after loading -->
      <div v-else-if="!agent && !loading" class="py-4 text-center text-gray-500">
        No address information available.
      </div>
    </div>

    <!-- Edit Modal with key to force re-render -->
    <EditAgentAddressModal
      v-if="isModalOpen && agent"
      :key="modalKey"
      :agent-data="agent"
      :is-saving="isSaving"
      @close="isModalOpen = false"
      @save="handleSave"
    />
    
    <!-- Map Viewer Modal -->
    <MapViewerModal
      v-if="isMapViewerOpen && agent && agent.latitude && agent.longitude"
      :show="isMapViewerOpen"
      :latitude="agent.latitude"
      :longitude="agent.longitude"
      :title="`${agent.name || 'Agent'} Location`"
      @close="isMapViewerOpen = false"
    />
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue';
import { useAgentStore } from '@/stores/agentStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';
import EditAgentAddressModal from './EditAgentAddressModal.vue'; // Import the agent edit modal
import MapViewerModal from '@/components/common/MapViewerModal.vue';
import type { Agent } from '@/service/agentService';
import 'leaflet/dist/leaflet.css'; // Import Leaflet CSS
import L from 'leaflet'; // Import Leaflet

const props = defineProps<{
  agentId: string;
}>();

const agentStore = useAgentStore();
const { loading, error } = storeToRefs(agentStore);

// Use the agentStore's getAgentById getter
const agent = computed(() => agentStore.getAgentById(props.agentId)); 
const isModalOpen = ref(false);
const isSaving = ref(false);
const modalKey = ref(0); // Used to force modal re-render
const mapContainer = ref<HTMLElement | null>(null); // Ref for map container element
const mapInstance = ref<L.Map | null>(null); // Ref for map instance
const isMapViewerOpen = ref(false); // State for the map viewer modal

// Format street address
const formatStreetAddress = (agent: Agent) => {
  if (!agent.streetNumber && !agent.streetName) return 'Not provided';
  
  let address = '';
  if (agent.streetNumber) address += agent.streetNumber;
  if (agent.streetNumber && agent.streetName) address += ' ';
  if (agent.streetName) address += agent.streetName;
  
  return address;
};

// Handle save from modal
const handleSave = async (formData: Partial<Agent>) => {
  isSaving.value = true;
  
  try {
    
    // Create a properly formatted address data object
    // Only include address-related fields expected by the backend update method
    const addressData: Partial<Agent> = {
      streetNumber: formData.streetNumber,
      streetName: formData.streetName,
      suburb: formData.suburb,
      city: formData.city,
      state: formData.state,
      postalCode: formData.postalCode,
      country: formData.country,
      latitude: formData.latitude,
      longitude: formData.longitude
      // Removed googlePlaceId as it's not in the Agent model
    };
    
    // Update agent through store
    await agentStore.updateAgent(props.agentId, addressData);
    
    // Increment key to force modal re-render on next open
    modalKey.value++;
    
    // Close modal
    isModalOpen.value = false;
    
    // Emit an event to notify the parent page to refresh data if needed
    // emit('agent-updated'); // Maybe not needed if parent already handles refetching
    
    // Optionally force refetch agent data if needed, but parent page should handle this
    // await agentStore.fetchAgents(); // Avoid double fetching if parent already does it

  } catch (saveError) {
    console.error('Failed to save address changes:', saveError);
    // Optionally display an error message to the user
  } finally {
    isSaving.value = false;
  }
};

// Fetch agent data on mount if not already in store
// The parent page (AgentProfileAdminPage) already fetches the agent data. 
// We rely on the store being populated by the parent.
// If the agent data isn't found initially, the computed 'agent' will be null.
// watch(
//   () => props.agentId,
//   async (newId) => {
//     if (newId && !agent.value) {
//        // console.log(`AgentAddressCard: Agent ${newId} not found in store, parent should fetch.`);
//        // Consider if we need a fallback fetch here, but ideally parent handles it.
//        // await agentStore.fetchAgentById(newId); // Need to add fetchAgentById to store if we do this
//     }
//   },
//   { immediate: true }
// );


// Function to initialize Leaflet map
const initMap = () => {
  const currentAgent = agent.value;
  if (mapContainer.value && currentAgent && currentAgent.latitude && currentAgent.longitude && !mapInstance.value) {
    try {
        mapInstance.value = L.map(mapContainer.value, {
        attributionControl: false, // Disable Leaflet attribution
        scrollWheelZoom: false, // Disable scroll wheel zoom
        zoomControl: false // Disable zoom control (+/- buttons)
      }).setView(
        [currentAgent.latitude, currentAgent.longitude],
        13 // Zoom level
      );

      // Add OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(mapInstance.value as L.Map);

      // Add marker
      L.marker([currentAgent.latitude, currentAgent.longitude]).addTo(mapInstance.value as L.Map);
    } catch (mapError) {
      console.error("Failed to initialize Leaflet map:", mapError);
      // Clean up if initialization failed partially
      destroyMap(); 
    }
  }
};

// Function to destroy Leaflet map
const destroyMap = () => {
  if (mapInstance.value) {
    mapInstance.value.remove();
    mapInstance.value = null;
  }
};

// Watch for changes in agent data to update the map
watch(agent, (newAgent, oldAgent) => {
  if (newAgent && newAgent.latitude && newAgent.longitude) {
    // If agent data is available and has coordinates
    if (!mapInstance.value || 
        (oldAgent && (newAgent.latitude !== oldAgent.latitude || newAgent.longitude !== oldAgent.longitude))) {
      // Initialize map if it doesn't exist or coordinates changed
      nextTick(() => {
        destroyMap(); // Ensure old instance is removed before creating new
        initMap();
      });
    }
  } else {
    // If no agent or no coordinates, destroy the map
    destroyMap();
  }
}, { immediate: true, deep: true }); // immediate: true to run on load, deep to watch nested props like lat/lng

// Ensure map is destroyed when component unmounts
onUnmounted(() => {
  destroyMap();
});
</script> 