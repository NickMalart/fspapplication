import { defineStore } from 'pinia'
import { agentService } from '@/service/agentService';
import { ref, computed } from 'vue';
import type { Agent, AgentWarehouse } from '@/service/agentService';

export interface AgentStoreState {
  agents: Agent[];
  loading: boolean;
  error: string | null;
  currentPage: number;
  perPage: number;
  totalAgents: number;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  searchTerm: string;
  statusFilter: 'active' | 'inactive' | 'all';
  selectedAgent: Agent | null;
}

export interface AgentWarehouseStoreState {
  warehouses: AgentWarehouse[];
  loading: boolean;
  error: string | null;
  currentPage: number;
  perPage: number;
  totalWarehouses: number;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  searchTerm: string;
  statusFilter: 'active' | 'inactive' | 'all';
  selectedWarehouse: AgentWarehouse | null;
}

export const useAgentStore = defineStore('agent', () => {
  // State
  const agents = ref<Agent[]>([]);
  const selectedAgent = ref<Agent | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const perPage = ref(10);
  const totalAgents = ref(0);
  const searchTerm = ref('');
  const statusFilter = ref<'active' | 'inactive' | 'all'>('active');
  const sortColumn = ref('name');
  const sortDirection = ref<'asc' | 'desc'>('asc');

  // Computed properties
  const totalPages = computed(() => Math.ceil(totalAgents.value / perPage.value) || 1);
  
  const startIndex = computed(() => {
    if (totalAgents.value === 0) return 0;
    return (currentPage.value - 1) * perPage.value + 1;
  });
  
  const endIndex = computed(() => {
    if (totalAgents.value === 0) return 0;
    return Math.min(currentPage.value * perPage.value, totalAgents.value);
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
  const getAgentById = computed(() => (id: string) => {
    return agents.value.find(agent => agent.id === id) || null;
  });

  // Actions
  const fetchAgents = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await agentService.getAgents({
        search: searchTerm.value,
        status: statusFilter.value,
        ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
        page: currentPage.value,
        pageSize: perPage.value
      });
      
      agents.value = response.results;
      totalAgents.value = response.count;
    } catch (err: any) {
      console.error('Error fetching agents:', err);
      error.value = err.message || 'Failed to fetch agents';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateAgent = async (agentId: string, data: Partial<Agent>) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedAgent = await agentService.updateAgent(agentId, data);
      
      // Update in agents array
      const index = agents.value.findIndex(a => a.id === agentId);
      if (index !== -1) {
        agents.value[index] = { ...agents.value[index], ...updatedAgent };
      }
      
      // Update selectedAgent if it matches
      if (selectedAgent.value?.id === agentId) {
        selectedAgent.value = { ...selectedAgent.value, ...updatedAgent };
      }
      
      return updatedAgent;
    } catch (err: any) {
      error.value = err.message || 'Failed to update agent';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateAgentLogo = async (agentId: string, logo: string | null) => {
    return await updateAgent(agentId, { logo });
  };

  const updateAgentStatus = async (agentId: string, isActive: boolean) => {
    return await updateAgent(agentId, { isActive });
  };

  const addAgent = async (data: Partial<Agent>) => {
    loading.value = true;
    error.value = null;
    try {
      const newAgent = await agentService.createAgent(data);
      await fetchAgents(); // Refresh the list to get updated pagination
      return newAgent;
    } catch (err: any) {
      error.value = err.message || 'Failed to create agent';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const setSelectedAgent = (agent: Agent | null) => {
    selectedAgent.value = agent;
  };

  // Pagination and filtering actions
  const setPerPage = (value: number) => {
    perPage.value = value;
    currentPage.value = 1; // Reset to first page when changing items per page
    fetchAgents(); // Fetch data with new page size
  };

  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
      fetchAgents(); // Fetch data for previous page
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      fetchAgents(); // Fetch data for next page
    }
  };

  const goToPage = (page: number) => {
    currentPage.value = page;
    fetchAgents(); // Fetch data for specific page
  };

  const setSearch = (term: string) => {
    searchTerm.value = term;
    currentPage.value = 1; // Reset to first page when searching
    fetchAgents(); // Fetch filtered data
  };

  const setStatusFilter = (status: 'active' | 'inactive' | 'all') => {
    statusFilter.value = status;
    currentPage.value = 1; // Reset to first page when changing filter
    fetchAgents(); // Fetch filtered data
  };

  const setSorting = (column: string) => {
    if (sortColumn.value === column) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn.value = column;
      sortDirection.value = 'asc';
    }
    fetchAgents(); // Fetch sorted data
  };

  return {
    // State
    agents,
    selectedAgent,
    loading,
    error,
    currentPage,
    perPage,
    totalAgents,
    sortColumn,
    sortDirection,
    // Computed
    totalPages,
    startIndex,
    endIndex,
    pageNumbers,
    // Getters
    getAgentById,
    // Actions
    fetchAgents,
    updateAgent,
    updateAgentLogo,
    updateAgentStatus,
    setSelectedAgent,
    addAgent,
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

export const useAgentWarehouseStore = defineStore('agentWarehouse', () => {
  // State
  const warehouses = ref<AgentWarehouse[]>([]);
  const selectedWarehouse = ref<AgentWarehouse | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const perPage = ref(10);
  const totalWarehouses = ref(0);
  const searchTerm = ref('');
  const statusFilter = ref<'active' | 'inactive' | 'all'>('active');
  const sortColumn = ref('name');
  const sortDirection = ref<'asc' | 'desc'>('asc');
  const currentAgentId = ref<string | null>(null);

  // Computed properties
  const totalPages = computed(() => Math.ceil(totalWarehouses.value / perPage.value) || 1);
  
  const startIndex = computed(() => {
    if (totalWarehouses.value === 0) return 0;
    return (currentPage.value - 1) * perPage.value + 1;
  });
  
  const endIndex = computed(() => {
    if (totalWarehouses.value === 0) return 0;
    return Math.min(currentPage.value * perPage.value, totalWarehouses.value);
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
  const getWarehouseById = computed(() => (id: string) => {
    return warehouses.value.find(warehouse => warehouse.id === id) || null;
  });

  // Actions
  const fetchWarehouses = async (agentId: string) => {
    if (!agentId) {
      error.value = 'Agent ID is required to fetch warehouses';
      return;
    }
    
    currentAgentId.value = agentId;
    loading.value = true;
    error.value = null;
    try {
      const response = await agentService.getAgentWarehouses(agentId, {
        search: searchTerm.value,
        status: statusFilter.value,
        ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
        page: currentPage.value,
        pageSize: perPage.value
      });
      
      warehouses.value = response.results;
      totalWarehouses.value = response.count;
    } catch (err: any) {
      console.error('Error fetching agent warehouses:', err);
      error.value = err.message || 'Failed to fetch agent warehouses';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const updateWarehouse = async (warehouseId: string, data: Partial<AgentWarehouse>) => {
    if (!currentAgentId.value) {
      error.value = 'No agent selected';
      return;
    }
    
    loading.value = true;
    error.value = null;
    try {
      const updatedWarehouse = await agentService.updateAgentWarehouse(
        currentAgentId.value,
        warehouseId,
        data
      );
      
      // Update in warehouses array
      const index = warehouses.value.findIndex(w => w.id === warehouseId);
      if (index !== -1) {
        warehouses.value[index] = { ...warehouses.value[index], ...updatedWarehouse };
      }
      
      // Update selectedWarehouse if it matches
      if (selectedWarehouse.value?.id === warehouseId) {
        selectedWarehouse.value = { ...selectedWarehouse.value, ...updatedWarehouse };
      }
      
      return updatedWarehouse;
    } catch (err: any) {
      error.value = err.message || 'Failed to update agent warehouse';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const addWarehouse = async (data: Partial<AgentWarehouse>) => {
    if (!currentAgentId.value) {
      error.value = 'No agent selected';
      return;
    }
    
    loading.value = true;
    error.value = null;
    try {
      const newWarehouse = await agentService.createAgentWarehouse(currentAgentId.value, data);
      await fetchWarehouses(currentAgentId.value); // Refresh the list to get updated pagination
      return newWarehouse;
    } catch (err: any) {
      error.value = err.message || 'Failed to create agent warehouse';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const setSelectedWarehouse = (warehouse: AgentWarehouse | null) => {
    selectedWarehouse.value = warehouse;
  };

  // Pagination and filtering actions
  const setPerPage = (value: number) => {
    perPage.value = value;
    currentPage.value = 1; // Reset to first page when changing items per page
    if (currentAgentId.value) {
      fetchWarehouses(currentAgentId.value); // Fetch data with new page size
    }
  };

  const prevPage = () => {
    if (currentPage.value > 1 && currentAgentId.value) {
      currentPage.value--;
      fetchWarehouses(currentAgentId.value); // Fetch data for previous page
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value && currentAgentId.value) {
      currentPage.value++;
      fetchWarehouses(currentAgentId.value); // Fetch data for next page
    }
  };

  const goToPage = (page: number) => {
    currentPage.value = page;
    if (currentAgentId.value) {
      fetchWarehouses(currentAgentId.value); // Fetch data for specific page
    }
  };

  const setSearch = (term: string) => {
    searchTerm.value = term;
    currentPage.value = 1; // Reset to first page when searching
    if (currentAgentId.value) {
      fetchWarehouses(currentAgentId.value); // Fetch filtered data
    }
  };

  const setStatusFilter = (status: 'active' | 'inactive' | 'all') => {
    statusFilter.value = status;
    currentPage.value = 1; // Reset to first page when changing filter
    if (currentAgentId.value) {
      fetchWarehouses(currentAgentId.value); // Fetch filtered data
    }
  };

  const setSorting = (column: string) => {
    if (sortColumn.value === column) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn.value = column;
      sortDirection.value = 'asc';
    }
    if (currentAgentId.value) {
      fetchWarehouses(currentAgentId.value); // Fetch sorted data
    }
  };

  return {
    // State
    warehouses,
    selectedWarehouse,
    loading,
    error,
    currentPage,
    perPage,
    totalWarehouses,
    sortColumn,
    sortDirection,
    // Computed
    totalPages,
    startIndex,
    endIndex,
    pageNumbers,
    // Getters
    getWarehouseById,
    // Actions
    fetchWarehouses,
    updateWarehouse,
    setSelectedWarehouse,
    addWarehouse,
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