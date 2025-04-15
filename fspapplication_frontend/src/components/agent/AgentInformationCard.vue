<template>
  <ComponentCard title="Agent Information">
    <!-- Debug Info (Remove in production) -->
    <!-- <pre v-if="false" class="text-xs bg-gray-100 dark:bg-gray-800 p-2 mb-4 overflow-auto">
      agent: {{ JSON.stringify(agent, null, 2) }}
    </pre> -->

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
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="agent" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Agent Name</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.name || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Phone</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.phone || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Email</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.email || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Website</p>
          <p class="font-medium text-black dark:text-white">
            <a 
              v-if="agent.website" 
              :href="formatWebsiteUrl(agent.website)" 
              target="_blank" 
              class="text-brand-500 hover:underline"
            >
              {{ agent.website }}
            </a>
            <span v-else>Not provided</span>
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">ABN</p>
          <p class="font-medium text-black dark:text-white">
            {{ agent.abn || 'Not provided' }}
          </p>
        </div>
      </div>
      <div v-else class="py-4 text-center text-gray-500">
        No agent information available
      </div>
    </div>

    <!-- Edit Modal with key to force re-render -->
    <EditAgentInformationModal
      v-if="isModalOpen && agent"
      :key="modalKey"
      :agent-data="agent"
      :is-saving="isSaving"
      @close="isModalOpen = false"
      @save="handleSave"
    />
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useAgentStore } from '@/stores/agentStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';
import EditAgentInformationModal from './EditAgentInformationModal.vue';
import type { Agent } from '@/service/agentService';

const props = defineProps<{
  agentId: string;
}>();

const emit = defineEmits(['agent-updated']);

const agentStore = useAgentStore();
const { loading, error } = storeToRefs(agentStore);

const agent = computed(() => agentStore.getAgentById(props.agentId));
const isModalOpen = ref(false);
const isSaving = ref(false);
const modalKey = ref(0); // Used to force modal re-render

// Format website URL to ensure it has http/https
const formatWebsiteUrl = (url: string) => {
  if (!url) return '';
  return url.startsWith('http') ? url : `https://${url}`;
};

// Handle save from modal
const handleSave = async (formData: Partial<Agent>) => {
  isSaving.value = true;
  
  try {
    const updatedAgent = await agentStore.updateAgent(props.agentId, formData);
    
    // Emit update event to parent
    emit('agent-updated', updatedAgent);
    
    // Increment key to force modal re-render on next open
    modalKey.value++;
    
    // Close modal
    isModalOpen.value = false;
  } catch (error) {
    // console.error('Failed to save agent changes:', error);
    // TODO: Add user-facing error notification
  } finally {
    isSaving.value = false;
  }
};

// Fetch agent data on mount if not already in store
onMounted(async () => {
  if (!agent.value) {
    await agentStore.fetchAgents();
  }
});

// Force refetch when modal closes
watch(isModalOpen, (open) => {
  if (!open) {
    agentStore.fetchAgents();
  }
});
</script>
