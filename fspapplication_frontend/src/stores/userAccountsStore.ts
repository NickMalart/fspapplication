import { defineStore } from 'pinia';
import { userAccountsService, UserAccount, UserListParams } from '@/service/userAccountsService';

interface UserAccountsState {
  users: UserAccount[];
  totalUsers: number;
  currentPage: number;
  perPage: number;
  loading: boolean;
  error: string | null;
  searchQuery: string;
  statusFilter: 'active' | 'inactive' | 'all';
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  selectedUser: UserAccount | null;
}

export const useUserAccountsStore = defineStore('userAccounts', {
  state: (): UserAccountsState => ({
    users: [],
    totalUsers: 0,
    currentPage: 1,
    perPage: 10,
    loading: false,
    error: null,
    searchQuery: '',
    statusFilter: 'active',
    sortColumn: 'firstName',
    sortDirection: 'asc',
    selectedUser: null
  }),
  
  getters: {
    totalPages: (state) => Math.ceil(state.totalUsers / state.perPage) || 1,
    
    startIndex: (state) => {
      if (state.totalUsers === 0) return 0;
      return (state.currentPage - 1) * state.perPage + 1;
    },
    
    endIndex: (state) => {
      if (state.totalUsers === 0) return 0;
      return Math.min(state.currentPage * state.perPage, state.totalUsers);
    },
    
    currentOrdering: (state) => {
      return `${state.sortDirection === 'desc' ? '-' : ''}${state.sortColumn}`;
    },
    
    // Generate array of nearby page numbers for pagination UI
    pageNumbers: (state) => {
      const range = 2;
      const totalPages = Math.ceil(state.totalUsers / state.perPage) || 1;
      
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
    async fetchUsers() {
      this.loading = true;
      this.error = null;
      
      try {
        const params: UserListParams = {
          search: this.searchQuery,
          status: this.statusFilter,
          ordering: this.currentOrdering,
          page: this.currentPage,
          pageSize: this.perPage
        };
        
        const response = await userAccountsService.getUsers(params);
        
        this.users = response.results;
        this.totalUsers = response.count;
        
        return this.users;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch users';
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    async getUserById(userId: string) {
      this.loading = true;
      this.error = null;
      
      try {
        this.selectedUser = await userAccountsService.getUserById(userId);
        return this.selectedUser;
      } catch (error: any) {
        this.error = error.message || `Failed to fetch user with ID ${userId}`;
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateUserStatus(userId: string, isActive: boolean) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedUser = await userAccountsService.updateUserStatus(userId, isActive);
        
        // Update the user in the local state
        const index = this.users.findIndex((user: UserAccount) => user.id === userId);
        if (index !== -1) {
          this.users[index] = updatedUser;
        }
        
        return true;
      } catch (error: any) {
        this.error = error.message || `Failed to update status for user ${userId}`;
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // Pagination and filtering actions
    goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        return this.fetchUsers();
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
      return this.fetchUsers();
    },
    
    setSearch(query: string) {
      this.searchQuery = query;
      this.currentPage = 1; // Reset to first page
      return this.fetchUsers();
    },
    
    setStatusFilter(status: 'active' | 'inactive' | 'all') {
      this.statusFilter = status;
      this.currentPage = 1; // Reset to first page
      return this.fetchUsers();
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
      return this.fetchUsers();
    }
  }
}); 