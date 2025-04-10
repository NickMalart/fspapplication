<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="isLoading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 dark:bg-red-900/20 dark:border-red-700 dark:text-red-400">
      {{ error }}
    </div>
    <div v-else-if="!agent" class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-600 dark:bg-yellow-900/20 dark:border-yellow-700 dark:text-yellow-400">
      No agent data found for ID: {{ agentId }}
    </div>
    <div v-else class="space-y-6">
      <AgentAvatarSection 
        :agent="agent" 
        @logo-updated="handleLogoUpdate"
        @status-updated="handleStatusUpdate"
      />
      
      <!-- Additional agent sections to be added later -->
      
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { agentService, type Agent } from '@/service/agentService';
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue';
import AgentAvatarSection from '@/components/agent/AgentAvatarSection.vue';

const route = useRoute();
const agentId = computed(() => route.params.id as string);
const currentPageTitle = ref('Agent Profile');

const agent = ref<Agent | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

// Fetch agent details
const fetchAgentDetails = async () => {
  if (!agentId.value) return;
  
  isLoading.value = true;
  error.value = null;
  
  try {
    const data = await agentService.getAgentById(agentId.value);
    agent.value = data;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load agent details';
    console.error('Error fetching agent details:', err);
  } finally {
    isLoading.value = false;
  }
};

// Handle logo update events from the avatar component
const handleLogoUpdate = async (updateData: { id: string, logo: string | null }) => {
  try {
    if (agent.value) {
      agent.value.logo = updateData.logo;
    }
  } catch (err) {
    console.error('Error updating agent logo:', err);
  }
};

// Handle status update events from the avatar component
const handleStatusUpdate = async (updateData: { id: string, isActive: boolean }) => {
  try {
    if (agent.value) {
      agent.value.isActive = updateData.isActive;
    }
  } catch (err) {
    console.error('Error updating agent status:', err);
  }
};

// Handle agent information updates
const handleAgentUpdate = async (updatedAgent: Agent) => {
  try {
    agent.value = updatedAgent;
    await fetchAgentDetails(); // Refresh the data to ensure consistency
  } catch (err) {
    console.error('Error handling agent update:', err);
  }
};

// Fetch data when component mounts
onMounted(() => {
  fetchAgentDetails();
});
</script>
