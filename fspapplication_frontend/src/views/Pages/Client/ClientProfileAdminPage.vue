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

const route = useRoute();
const clientId = computed(() => Number(route.params.id));
const currentPageTitle = ref('Client Profile');

const client = ref<Client | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

// Computed property to check if we have any address information
const hasAddressInfo = computed(() => {
  return client.value && (
    client.value.streetNumber || 
    client.value.streetName || 
    client.value.suburb || 
    client.value.city || 
    client.value.state || 
    client.value.postalCode || 
    client.value.country
  );
});

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
const handleLogoUpdate = async (updateData: { id: number, logo: string | null }) => {
  try {
    // Here you would call your client update service
    // For now, just update the local client data
    if (client.value) {
      client.value.logo = updateData.logo;
    }
  } catch (err) {
    console.error('Error updating client logo:', err);
  }
};

// Fetch data when component mounts
onMounted(() => {
  fetchClientDetails();
});
</script>
