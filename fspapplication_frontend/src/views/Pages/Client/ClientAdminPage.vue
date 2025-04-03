<template>
    <AdminLayout>
      <PageBreadcrumb :pageTitle="currentPageTitle" />
      <div
        class="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12"
      >
        <div class="mx-auto w-full max-w-[630px] text-center">
          <h3
            class="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl"
          >
            Client Management
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 sm:text-base">
            Below is the list of client accounts currently available.
          </p>
        </div>
        
        <!-- Action buttons -->
        <div class="mb-6 flex justify-end">
          <button
            @click="openCreateModal"
            class="flex items-center rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-brand-600"
          >
            <span class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </span>
            Create Client
          </button>
        </div>
        
        <ClientDataTable 
          @refresh="fetchClients" 
          @client-selected="handleClientSelected"
        />
        
        <!-- Client Information Card -->
        <div v-if="selectedClientId" class="mt-8">
          <ClientInformationCard :client-id="selectedClientId" />
        </div>
        
        <!-- Create Client Modal -->
        <ClientCreateModal 
          :show="showCreateModal" 
          @close="closeCreateModal" 
          @client-created="handleClientCreated" 
        />
      </div>
    </AdminLayout>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from "vue";
  import AdminLayout from "@/components/layout/AdminLayout.vue";
  import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
  import ClientDataTable from "@/components/client/ClientDataTable.vue";
  import ClientCreateModal from "@/components/client/ClientCreateModal.vue";
  import ClientInformationCard from "@/components/client/ClientInformationCard.vue";
  import { useClientStore } from "@/stores/clientStore";
  import type { Client } from "@/service/clientService";
  
  const currentPageTitle = ref("Client Management");
  const showCreateModal = ref(false);
  const selectedClientId = ref<string | null>(null);
  const clientStore = useClientStore();
  
  const openCreateModal = () => {
    showCreateModal.value = true;
  };
  
  const closeCreateModal = () => {
    showCreateModal.value = false;
  };
  
  const handleClientCreated = (newClient: Client) => {
    // Refresh the client list to ensure the new client is displayed
    fetchClients();
    closeCreateModal();
  };

  const handleClientSelected = (clientId: string) => {
    selectedClientId.value = clientId;
  };
  
  const fetchClients = async () => {
    await clientStore.fetchClients();
  };
  
  onMounted(() => {
    fetchClients();
  });
  </script>
  
  <style></style>
  