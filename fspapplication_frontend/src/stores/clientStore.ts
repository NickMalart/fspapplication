import { defineStore } from 'pinia'
import { clientService } from '@/service/clientService';
import { ref, computed } from 'vue';
import type { Client } from '@/service/clientService';

export interface ClientStoreState {
  clients: Client[];
  loading: boolean;
  error: string | null;
  currentPage: number;
  perPage: number;
  totalClients: number;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  searchTerm: string;
  statusFilter: 'active' | 'inactive' | 'all';
  selectedClient: Client | null;
}

export const useClientStore = defineStore('client', () => {
  const clients = ref<Client[]>([]);
  const selectedClient = ref<Client | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const getClientById = computed(() => (id: string) => {
    return clients.value.find(client => client.id === id) || null;
  });

  // Actions
  const fetchClients = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await clientService.getClients();
      clients.value = response.results;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch clients';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateClient = async (clientId: string, data: Partial<Client>) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedClient = await clientService.updateClient(clientId, data);
      
      // Update in clients array
      const index = clients.value.findIndex(c => c.id === clientId);
      if (index !== -1) {
        clients.value[index] = { ...clients.value[index], ...updatedClient };
      }
      
      // Update selectedClient if it matches
      if (selectedClient.value?.id === clientId) {
        selectedClient.value = { ...selectedClient.value, ...updatedClient };
      }
      
      return updatedClient;
    } catch (err: any) {
      error.value = err.message || 'Failed to update client';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateClientLogo = async (clientId: string, logo: string | null) => {
    return await updateClient(clientId, { logo });
  };

  const updateClientStatus = async (clientId: string, isActive: boolean) => {
    return await updateClient(clientId, { isActive });
  };

  const setSelectedClient = (client: Client | null) => {
    selectedClient.value = client;
  };

  return {
    // State
    clients,
    selectedClient,
    loading,
    error,
    // Getters
    getClientById,
    // Actions
    fetchClients,
    updateClient,
    updateClientLogo,
    updateClientStatus,
    setSelectedClient,
  };
}); 