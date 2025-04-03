<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="isLoading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 dark:bg-red-900/20 dark:border-red-700 dark:text-red-400">
      {{ error }}
    </div>
    <div v-else-if="!client" class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-600 dark:bg-yellow-900/20 dark:border-yellow-700 dark:text-yellow-400">
      No client data found for ID: {{ clientId }}
    </div>
    <div v-else class="space-y-6">
      <ClientAvatarSection 
        :client="client" 
        @logo-updated="handleLogoUpdate"
        @status-updated="handleStatusUpdate"
      />
      
      <ClientInformationCard 
        :client-id="clientId"
        @client-updated="handleClientUpdate"
      />

      <ClientAddressCard 
        :client-id="clientId"
        @client-updated="handleClientUpdate"
      />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { clientService, type Client } from '@/service/clientService';
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue';
import ClientAvatarSection from '@/components/client/ClientAvatarSection.vue';
import ClientInformationCard from '@/components/client/ClientInformationCard.vue';
import ClientAddressCard from '@/components/client/ClientAddressCard.vue';

const route = useRoute();
const clientId = computed(() => route.params.id as string);
const currentPageTitle = ref('Client Profile');

const client = ref<Client | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

// Fetch client details
const fetchClientDetails = async () => {
  if (!clientId.value) return;
  
  isLoading.value = true;
  error.value = null;
  
  try {
    const data = await clientService.getClientById(clientId.value);
    client.value = data;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load client details';
    console.error('Error fetching client details:', err);
  } finally {
    isLoading.value = false;
  }
};

// Handle logo update events from the avatar component
const handleLogoUpdate = async (updateData: { id: string, logo: string | null }) => {
  try {
    if (client.value) {
      client.value.logo = updateData.logo;
    }
  } catch (err) {
    console.error('Error updating client logo:', err);
  }
};

// Handle status update events from the avatar component
const handleStatusUpdate = async (updateData: { id: string, isActive: boolean }) => {
  try {
    if (client.value) {
      client.value.isActive = updateData.isActive;
    }
  } catch (err) {
    console.error('Error updating client status:', err);
  }
};

// Handle client information updates
const handleClientUpdate = async (updatedClient: Client) => {
  try {
    client.value = updatedClient;
    await fetchClientDetails(); // Refresh the data to ensure consistency
  } catch (err) {
    console.error('Error handling client update:', err);
  }
};

// Fetch data when component mounts
onMounted(() => {
  fetchClientDetails();
});
</script>
