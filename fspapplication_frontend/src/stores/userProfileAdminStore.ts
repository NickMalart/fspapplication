import { defineStore } from 'pinia';
import { useAuthStore } from './auth';
import { userProfileAdminService } from '@/service/userProfileAdminService';

// Types for the admin user profile management
export interface FunctionalGroup {
  id: string;
  code: string;
  name: string;
  color: string;
}

export interface AgentProfileAdmin {
  companyName: string;
  abn: string;
  yearsOfExperience: number;
}

export interface ClientProfile {
  companyName: string;
  industry: string | null;
  clientSince: string;
}

export interface EmployeeProfile {
  companyName: string;
  department: string;
  employeeId: string | null;
  jobTitle: string | null;
  startDate: string;
  reportsTo: string | null;
}

export interface UserProfileAdmin {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  userType: string;
  avatar: string | null;
  isActive: boolean;
  isStaff: boolean;
  isTenantOwner: boolean;
  dateJoined: string;
  lastLogin: string | null;
  profile: {
    id: string;
    phoneNumber: string | null;
    emergencyContact: string | null;
    emergencyContactFirstName: string | null;
    emergencyContactLastName: string | null;
    streetNumber: string | null;
    streetName: string | null;
    suburb: string | null;
    city: string | null;
    state: string | null;
    postalCode: string | null;
    country: string | null;
    latitude: number | null;
    longitude: number | null;
    googlePlaceId: string | null;
    dateOfBirth: string | null;
    createdAt: string;
    updatedAt: string;
  };
  functionalGroups: FunctionalGroup[];
  agentProfile?: AgentProfileAdmin;
  clientProfile?: ClientProfile;
  employeeProfile?: EmployeeProfile;
}

interface UserProfileAdminState {
  currentUser: UserProfileAdmin | null;
  loading: boolean;
  error: string | null;
  saving: boolean;
}

export const useUserProfileAdminStore = defineStore('userProfileAdmin', {
  state: (): UserProfileAdminState => ({
    currentUser: null,
    loading: false,
    error: null,
    saving: false
  }),
  
  getters: {
    fullName: (state) => {
      if (!state.currentUser) return '';
      return `${state.currentUser.firstName} ${state.currentUser.lastName}`.trim();
    },
    
    userTypeProfile: (state) => {
      if (!state.currentUser) return null;
      
      if (state.currentUser.userType === 'agent') {
        return state.currentUser.agentProfile;
      } else if (state.currentUser.userType === 'client') {
        return state.currentUser.clientProfile;
      } else if (state.currentUser.userType === 'employee') {
        return state.currentUser.employeeProfile;
      }
      
      return null;
    },
    
    functionalGroupCodes: (state) => {
      if (!state.currentUser?.functionalGroups) return [];
      return state.currentUser.functionalGroups.map(group => group.code);
    }
  },
  
  actions: {
    async fetchUserProfile(userId: string) {
      this.loading = true;
      this.error = null;
      
      try {
        this.currentUser = await userProfileAdminService.getUserProfile(userId);
        return this.currentUser;
      } catch (error: any) {
        this.error = error.response?.data?.detail || error.message || 'Failed to fetch user profile';
        
        // If unauthorized, redirect to login
        if (error.response?.status === 401 || error.response?.status === 403) {
          const authStore = useAuthStore();
          authStore.removeToken();
        }
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateUserProfile(userId: string, userData: Partial<UserProfileAdmin>) {
      this.saving = true;
      this.error = null;
      
      try {
        this.currentUser = await userProfileAdminService.updateUserProfile(userId, userData);
        return this.currentUser;
      } catch (error: any) {
        this.error = error.response?.data?.detail || error.message || 'Failed to update user profile';
        
        // If unauthorized, redirect to login
        if (error.response?.status === 401 || error.response?.status === 403) {
          const authStore = useAuthStore();
          authStore.removeToken();
        }
        return null;
      } finally {
        this.saving = false;
      }
    },
    
    async updateUserStatus(userId: string, isActive: boolean) {
      this.saving = true;
      this.error = null;
      
      try {
        this.currentUser = await userProfileAdminService.updateUserStatus(userId, isActive);
        return true;
      } catch (error: any) {
        this.error = error.response?.data?.detail || error.message || 'Failed to update user status';
        return false;
      } finally {
        this.saving = false;
      }
    },
    
    async updateFunctionalGroups(userId: string, groupIds: string[]) {
      this.saving = true;
      this.error = null;
      
      try {
        this.currentUser = await userProfileAdminService.updateFunctionalGroups(userId, groupIds);
        return true;
      } catch (error: any) {
        this.error = error.response?.data?.detail || error.message || 'Failed to update functional groups';
        return false;
      } finally {
        this.saving = false;
      }
    },
    
    reset() {
      this.currentUser = null;
      this.loading = false;
      this.error = null;
      this.saving = false;
    }
  }
}); 