import { defineStore } from 'pinia';
import { clientService, Client, ClientListParams } from '@/service/clientService';

interface ClientStoreState {
  clients: Client[];
  totalClients: number;
  currentPage: number;
  perPage: number;
  loading: boolean;
  error: string | null;
  searchQuery: string;
  statusFilter: 'active' | 'inactive' | 'all';
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  selectedClient: Client | null;
}

export const useClientStore = defineStore('clients', {
  state: (): ClientStoreState => ({
    clients: [],
    totalClients: 0,
    currentPage: 1,
    perPage: 10,
    loading: false,
    error: null,
    searchQuery: '',
    statusFilter: 'active',
    sortColumn: 'name',
    sortDirection: 'asc',
    selectedClient: null
  }),
  
  getters: {
    totalPages: (state) => Math.ceil(state.totalClients / state.perPage) || 1,
    
    startIndex: (state) => {
      if (state.totalClients === 0) return 0;
      return (state.currentPage - 1) * state.perPage + 1;
    },
    
    endIndex: (state) => {
      if (state.totalClients === 0) return 0;
      return Math.min(state.currentPage * state.perPage, state.totalClients);
    },
    
    currentOrdering: (state) => {
      return `${state.sortDirection === 'desc' ? '-' : ''}${state.sortColumn}`;
    },
    
    // Generate array of nearby page numbers for pagination UI
    pageNumbers: (state) => {
      const range = 2;
      const totalPages = Math.ceil(state.totalClients / state.perPage) || 1;
      
      let pages = [];
      for (
        let i = Math.max(1, state.currentPage - range);
        i <= Math.min(totalPages, state.currentPage + range);
        i++
      ) {
        pages.push(i);
      }
      return pages;
    }
  },
  
  actions: {
    async fetchClients() {
      this.loading = true;
      this.error = null;
      
      try {
        const params: ClientListParams = {
          search: this.searchQuery,
          status: this.statusFilter,
          ordering: this.currentOrdering,
          page: this.currentPage,
          pageSize: this.perPage
        };
        
        const response = await clientService.getClients(params);
        
        this.clients = response.results;
        this.totalClients = response.count;
        
        return this.clients;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch clients';
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    async getClientById(clientId: number) {
      this.loading = true;
      this.error = null;
      
      try {
        this.selectedClient = await clientService.getClientById(clientId);
        return this.selectedClient;
      } catch (error: any) {
        this.error = error.message || `Failed to fetch client with ID ${clientId}`;
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateClientStatus(clientId: number, isActive: boolean) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedClient = await clientService.updateClientStatus(clientId, isActive);
        
        // Update the client in the local state
        const index = this.clients.findIndex((client: Client) => client.id === clientId);
        if (index !== -1) {
          this.clients[index] = updatedClient;
        }
        
        return true;
      } catch (error: any) {
        this.error = error.message || `Failed to update status for client ${clientId}`;
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // Pagination and filtering actions
    goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        return this.fetchClients();
      }
      return Promise.resolve([]);
    },
    
    nextPage() {
      return this.goToPage(this.currentPage + 1);
    },
    
    prevPage() {
      return this.goToPage(this.currentPage - 1);
    },
    
    setPerPage(perPage: number) {
      this.perPage = perPage;
      this.currentPage = 1; // Reset to first page
      return this.fetchClients();
    },
    
    setSearch(query: string) {
      this.searchQuery = query;
      this.currentPage = 1; // Reset to first page
      return this.fetchClients();
    },
    
    setStatusFilter(status: 'active' | 'inactive' | 'all') {
      this.statusFilter = status;
      this.currentPage = 1; // Reset to first page
      return this.fetchClients();
    },
    
    setSorting(column: string) {
      if (this.sortColumn === column) {
        // Toggle direction if same column
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // New column, default to ascending
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
      return this.fetchClients();
    }
  }
}); 