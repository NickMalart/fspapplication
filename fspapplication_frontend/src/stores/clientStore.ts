import { defineStore } from 'pinia'
import { clientService, type Client as ServiceClient } from '@/service/clientService';

// Use Client interface from service
export type Client = ServiceClient;

interface ClientStoreState {
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
}

export const useClientStore = defineStore('client', {
  state: (): ClientStoreState => ({
    clients: [],
    loading: false,
    error: null,
    currentPage: 1,
    perPage: 10,
    totalClients: 0,
    sortColumn: 'name',
    sortDirection: 'asc',
    searchTerm: '',
    statusFilter: 'active', // 'active', 'inactive', or 'all'
  }),

  getters: {
    // Server-side pagination and filtering means we don't need these client-side getters
    // Instead use the clients array directly which contains paginated results from API
    totalPages(): number {
      return Math.ceil(this.totalClients / this.perPage);
    },
    
    startIndex(): number {
      return this.clients.length === 0 
        ? 0 
        : (this.currentPage - 1) * this.perPage + 1;
    },
    
    endIndex(): number {
      const end = this.currentPage * this.perPage;
      return Math.min(end, this.totalClients);
    },
    
    pageNumbers(): number[] {
      const totalPages = this.totalPages;
      const currentPage = this.currentPage;
      
      if (totalPages <= 5) {
        return Array.from({ length: totalPages }, (_, i) => i + 1);
      }
      
      if (currentPage <= 3) {
        return [1, 2, 3, 4, 5];
      }
      
      if (currentPage >= totalPages - 2) {
        return [
          totalPages - 4,
          totalPages - 3,
          totalPages - 2,
          totalPages - 1,
          totalPages
        ];
      }
      
      return [
        currentPage - 2,
        currentPage - 1,
        currentPage,
        currentPage + 1,
        currentPage + 2
      ];
    }
  },
  
  actions: {
    async fetchClients() {
      this.loading = true;
      try {
        // Make real API call using clientService
        const response = await clientService.getClients({
          search: this.searchTerm,
          status: this.statusFilter,
          ordering: this.sortDirection === 'asc' ? this.sortColumn : `-${this.sortColumn}`,
          page: this.currentPage,
          pageSize: this.perPage
        });
        
        // Update store with response data - these are already paginated from server
        this.clients = response.results;
        this.totalClients = response.count;
      } catch (error) {
        this.error = error instanceof Error ? error.message : String(error);
        console.error('Error fetching clients:', error);
      } finally {
        this.loading = false;
      }
    },
    
    async createClient(clientData: Partial<Client>): Promise<Client> {
      this.loading = true;
      try {
        // Make real API call to create client
        const newClient = await clientService.createClient(clientData);
        
        // Refresh the client list to include the new client
        this.fetchClients();
        
        return newClient;
      } catch (error) {
        this.error = error instanceof Error ? error.message : String(error);
        console.error('Error creating client:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateClientStatus(clientId: number, isActive: boolean) {
      this.loading = true;
      try {
        // Make real API call to update client status
        await clientService.updateClientStatus(clientId.toString(), isActive);
        
        // Refresh the client list to reflect the updated status
        this.fetchClients();
      } catch (error) {
        this.error = error instanceof Error ? error.message : String(error);
        console.error('Error updating client status:', error);
      } finally {
        this.loading = false;
      }
    },
    
    setSearch(searchTerm: string) {
      this.searchTerm = searchTerm;
      this.currentPage = 1; // Reset to first page when searching
    },
    
    setSorting(column: string) {
      if (this.sortColumn === column) {
        // Toggle direction if clicking the same column
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        // Default to ascending for new columns
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    
    setPerPage(perPage: number) {
      this.perPage = perPage;
      this.currentPage = 1; // Reset to first page
    },
    
    setStatusFilter(status: 'active' | 'inactive' | 'all') {
      this.statusFilter = status;
      this.currentPage = 1; // Reset to first page
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  }
}); 