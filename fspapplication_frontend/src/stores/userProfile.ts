import { defineStore } from 'pinia';
import { UserProfileService } from '@/services/userProfileService';
import type {
    User,
    UserListItem,
    UserProfile,
    UpdateUserRequest,
    UpdateUserProfileRequest,
    PaginatedResponse
} from '@/types/userProfile';

interface UserProfileState {
    currentUser: User | null;
    users: UserListItem[];
    loading: boolean;
    error: string | null;
    pagination: {
        count: number;
        totalPages: number;
        currentPage: number;
    };
    filters: {
        search: string;
        userType: string;
        status: 'active' | 'inactive' | '';
        ordering: string;
    };
}

export const useUserProfileStore = defineStore('userProfile', {
    state: (): UserProfileState => ({
        currentUser: null,
        users: [],
        loading: false,
        error: null,
        pagination: {
            count: 0,
            totalPages: 0,
            currentPage: 1
        },
        filters: {
            search: '',
            userType: '',
            status: '',
            ordering: ''
        }
    }),

    getters: {
        isAuthenticated: (state) => !!state.currentUser,
        userFullName: (state) => state.currentUser 
            ? `${state.currentUser.first_name} ${state.currentUser.last_name}`.trim() 
            : '',
        userInitials: (state) => state.currentUser 
            ? `${state.currentUser.first_name.charAt(0)}${state.currentUser.last_name.charAt(0)}`.toUpperCase() 
            : '',
        currentUserProfile: (state) => state.currentUser?.profile ?? null,
        isAdmin: (state) => state.currentUser?.functional_groups.some(group => group.code === 'admin') ?? false,
        userTypeOptions: () => [
            { value: 'employee', label: 'Employee' },
            { value: 'agent', label: 'Agent' },
            { value: 'client', label: 'Client' }
        ],
        statusOptions: () => [
            { value: '', label: 'All' },
            { value: 'active', label: 'Active' },
            { value: 'inactive', label: 'Inactive' }
        ],
        orderingOptions: () => [
            { value: 'first_name', label: 'First Name (A-Z)' },
            { value: '-first_name', label: 'First Name (Z-A)' },
            { value: 'last_name', label: 'Last Name (A-Z)' },
            { value: '-last_name', label: 'Last Name (Z-A)' },
            { value: 'email', label: 'Email (A-Z)' },
            { value: '-email', label: 'Email (Z-A)' },
            { value: 'date_joined', label: 'Newest First' },
            { value: '-date_joined', label: 'Oldest First' }
        ]
    },

    actions: {
        // Current User Actions
        async fetchCurrentUser() {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                this.currentUser = await service.getCurrentUser();
            } catch (err) {
                this.error = 'Failed to fetch current user';
                console.error('Error fetching current user:', err);
            } finally {
                this.loading = false;
            }
        },

        async updateCurrentUser(data: UpdateUserRequest) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                this.currentUser = await service.updateCurrentUser(data);
                return true;
            } catch (err) {
                this.error = 'Failed to update user information';
                console.error('Error updating user:', err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        // User List Actions
        async fetchUsers(page = 1, pageSize = 10) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                const response = await service.getUsers({
                    page,
                    page_size: pageSize,
                    search: this.filters.search,
                    ordering: this.filters.ordering,
                    user_type: this.filters.userType,
                    status: this.filters.status as 'active' | 'inactive' | undefined
                });

                this.users = response.results;
                this.pagination = {
                    count: response.count,
                    totalPages: response.total_pages,
                    currentPage: response.current_page
                };
            } catch (err) {
                this.error = 'Failed to fetch users';
                console.error('Error fetching users:', err);
            } finally {
                this.loading = false;
            }
        },

        async createUser(data: UpdateUserRequest) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                await service.createUser(data);
                await this.fetchUsers(this.pagination.currentPage);
                return true;
            } catch (err) {
                this.error = 'Failed to create user';
                console.error('Error creating user:', err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        async updateUser(userId: string, data: UpdateUserRequest) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                await service.updateUser(userId, data);
                await this.fetchUsers(this.pagination.currentPage);
                return true;
            } catch (err) {
                this.error = 'Failed to update user';
                console.error('Error updating user:', err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        async deleteUser(userId: string) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                await service.deleteUser(userId);
                await this.fetchUsers(this.pagination.currentPage);
                return true;
            } catch (err) {
                this.error = 'Failed to delete user';
                console.error('Error deleting user:', err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        // User Status Actions
        async toggleUserStatus(userId: string, activate: boolean) {
            this.loading = true;
            this.error = null;
            try {
                const service = new UserProfileService();
                if (activate) {
                    await service.activateUser(userId);
                } else {
                    await service.deactivateUser(userId);
                }
                await this.fetchUsers(this.pagination.currentPage);
                return true;
            } catch (err) {
                this.error = `Failed to ${activate ? 'activate' : 'deactivate'} user`;
                console.error('Error toggling user status:', err);
                return false;
            } finally {
                this.loading = false;
            }
        },

        // Filter Actions
        setFilter(
            filter: keyof UserProfileState['filters'],
            value: string | 'active' | 'inactive' | ''
        ) {
            if (filter === 'status') {
                this.filters[filter] = value as 'active' | 'inactive' | '';
            } else {
                this.filters[filter as 'search' | 'userType' | 'ordering'] = value as string;
            }
            this.fetchUsers(1); // Reset to first page when filters change
        },

        resetFilters() {
            this.filters = {
                search: '',
                userType: '',
                status: '',
                ordering: ''
            };
            this.fetchUsers(1);
        },

        // Error Handling
        clearError() {
            this.error = null;
        }
    }
}); 