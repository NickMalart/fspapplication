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
  // State
  const clients = ref<Client[]>([]);
  const selectedClient = ref<Client | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const perPage = ref(10);
  const totalClients = ref(0);
  const searchTerm = ref('');
  const statusFilter = ref<'active' | 'inactive' | 'all'>('active');
  const sortColumn = ref('name');
  const sortDirection = ref<'asc' | 'desc'>('asc');

  // Computed properties
  const totalPages = computed(() => Math.ceil(totalClients.value / perPage.value) || 1);
  
  const startIndex = computed(() => {
    if (totalClients.value === 0) return 0;
    return (currentPage.value - 1) * perPage.value + 1;
  });
  
  const endIndex = computed(() => {
    if (totalClients.value === 0) return 0;
    return Math.min(currentPage.value * perPage.value, totalClients.value);
  });
  
  const pageNumbers = computed(() => {
    const range = 2;
    const pages = [];
    for (
      let i = Math.max(1, currentPage.value - range);
      i <= Math.min(totalPages.value, currentPage.value + range);
      i++
    ) {
      pages.push(i);
    }
    return pages;
  });

  // Getters
  const getClientById = computed(() => (id: string) => {
    return clients.value.find(client => client.id === id) || null;
  });

  // Actions
  const fetchClients = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await clientService.getClients({
        search: searchTerm.value,
        status: statusFilter.value,
        ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
        page: currentPage.value,
        pageSize: perPage.value
      });
      
      clients.value = response.results;
      totalClients.value = response.count;
    } catch (err: any) {
      console.error('Error fetching clients:', err);
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

  const addClient = async (data: Partial<Client>) => {
    loading.value = true;
    error.value = null;
    try {
      const newClient = await clientService.createClient(data);
      await fetchClients(); // Refresh the list to get updated pagination
      return newClient;
    } catch (err: any) {
      error.value = err.message || 'Failed to create client';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const setSelectedClient = (client: Client | null) => {
    selectedClient.value = client;
  };

  // Pagination and filtering actions
  const setPerPage = (value: number) => {
    perPage.value = value;
    currentPage.value = 1; // Reset to first page when changing items per page
    fetchClients(); // Fetch data with new page size
  };

  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
      fetchClients(); // Fetch data for previous page
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      fetchClients(); // Fetch data for next page
    }
  };

  const goToPage = (page: number) => {
    currentPage.value = page;
    fetchClients(); // Fetch data for specific page
  };

  const setSearch = (term: string) => {
    searchTerm.value = term;
    currentPage.value = 1; // Reset to first page when searching
    fetchClients(); // Fetch filtered data
  };

  const setStatusFilter = (status: 'active' | 'inactive' | 'all') => {
    statusFilter.value = status;
    currentPage.value = 1; // Reset to first page when changing filter
    fetchClients(); // Fetch filtered data
  };

  const setSorting = (column: string) => {
    if (sortColumn.value === column) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn.value = column;
      sortDirection.value = 'asc';
    }
    fetchClients(); // Fetch sorted data
  };

  return {
    // State
    clients,
    selectedClient,
    loading,
    error,
    currentPage,
    perPage,
    totalClients,
    sortColumn,
    sortDirection,
    // Computed
    totalPages,
    startIndex,
    endIndex,
    pageNumbers,
    // Getters
    getClientById,
    // Actions
    fetchClients,
    updateClient,
    updateClientLogo,
    updateClientStatus,
    setSelectedClient,
    addClient,
    // Pagination and filtering actions
    setPerPage,
    prevPage,
    nextPage,
    goToPage,
    setSearch,
    setStatusFilter,
    setSorting
  };
}); 