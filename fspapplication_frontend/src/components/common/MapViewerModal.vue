<template>
  <BaseModal
    v-if="show"
    :title="modalTitle"
    :showSubmitButton="false"
    :modalSize="'max-w-3xl'" 
    @close="closeModal"
  >
    <div class="h-[60vh] w-full" ref="mapContainer">
      <!-- Map will be rendered here -->
    </div>
    <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
      Use scroll wheel to zoom, drag to pan.
    </p>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const props = defineProps<{
  show: boolean;
  latitude: number | null | undefined;
  longitude: number | null | undefined;
  title?: string;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const mapContainer = ref<HTMLElement | null>(null);
const mapInstance = ref<L.Map | null>(null);

const modalTitle = computed(() => props.title || 'Map View');

const initMap = () => {
  if (mapContainer.value && props.latitude && props.longitude && !mapInstance.value) {
    mapInstance.value = L.map(mapContainer.value, {
      scrollWheelZoom: true, 
      attributionControl: false
    }).setView([props.latitude, props.longitude], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapInstance.value as L.Map);

    L.marker([props.latitude, props.longitude]).addTo(mapInstance.value as L.Map);
  }
};

const destroyMap = () => {
  if (mapInstance.value) {
    mapInstance.value.remove();
    mapInstance.value = null;
  }
};

const closeModal = () => {
  emit('close');
};

// Watch for the modal becoming visible and coordinates being valid
watch(() => [props.show, props.latitude, props.longitude], ([show, lat, lng]) => {
  if (show && lat && lng) {
    // Use nextTick to ensure the container is ready in the DOM
    nextTick(() => {
      initMap();
    });
  } else {
    // Destroy map if modal is hidden or coordinates are invalid
    destroyMap();
  }
}, { immediate: true });

// Ensure map is destroyed when the component itself is unmounted
onUnmounted(() => {
  destroyMap();
});

// Recalculate map size if the modal (and thus container) resizes
// This might be needed depending on BaseModal implementation
// You might need a more robust resize observer if needed.
// Example:
// onMounted(() => {
//   if (mapContainer.value) {
//     const resizeObserver = new ResizeObserver(() => {
//       mapInstance.value?.invalidateSize();
//     });
//     resizeObserver.observe(mapContainer.value);
//     onUnmounted(() => resizeObserver.disconnect());
//   }
// });

</script>

<style>
/* Ensure leaflet controls are visible */
.leaflet-control-zoom a {
  color: #000 !important; /* Adjust color if needed */
}
.leaflet-control-attribution a {
   color: #0078A8 !important; /* Adjust color if needed */
}
/* You might need !important depending on BaseModal styles */
.leaflet-pane,
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-marker-shadow,
.leaflet-tile-container,
.leaflet-pane > canvas,
.leaflet-zoom-box,
.leaflet-image-layer,
.leaflet-layer {
  position: absolute;
  left: 0;
  top: 0;
}
.leaflet-container {
  overflow: hidden; /* Hide scrollbars if they appear */
}
</style> 