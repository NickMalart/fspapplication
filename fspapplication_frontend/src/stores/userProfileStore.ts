import { defineStore } from 'pinia';
import { userService } from '@/service/userProfileService';
import type { UserLogin, CompleteUser, ProfileData } from '@/service/userProfileService';

interface UserState {
  currentUser: UserLogin | null;
  completeUser: CompleteUser | null;
  loading: boolean;
  error: string | null;
  lastFetchTime: number | null;
}

// Cache expiration time in ms (5 minutes)
const CACHE_EXPIRATION = 5 * 60 * 1000;

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    currentUser: null,
    completeUser: null,
    loading: false,
    error: null,
    lastFetchTime: null
  }),
  
  getters: {
    // Convenience getter for profile data
    userProfile: (state) => state.completeUser?.profile || null,
    // Full name getter
    fullName: (state) => {
      if (!state.completeUser) return '';
      return `${state.completeUser.firstName} ${state.completeUser.lastName}`.trim();
    },
    // Check if cache is still valid
    isCacheValid: (state): boolean => {
      if (!state.lastFetchTime || !state.completeUser) return false;
      return Date.now() - state.lastFetchTime < CACHE_EXPIRATION;
    }
  },
  
  actions: {
    async fetchCurrentUser() {
      if (this.loading) return this.currentUser;
      
      this.loading = true;
      this.error = null;
      try {
        this.currentUser = await userService.getCurrentUser();
        return this.currentUser;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch user data';
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchUserProfile(forceRefresh = false) {
      if (!forceRefresh && this.isCacheValid) return this.completeUser;
      if (this.loading) return this.completeUser;
      
      this.loading = true;
      this.error = null;
      try {
        const userData = await userService.getUserProfile();
        this.completeUser = { ...userData };
        this.lastFetchTime = Date.now();
        return this.completeUser;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch user profile';
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateUserProfile(userData: Partial<CompleteUser>) {
      this.loading = true;
      this.error = null;
      try {
        const updatedUser = await userService.updateUserProfile(userData);
        this.completeUser = { ...updatedUser };
        this.lastFetchTime = Date.now();
        return true;
      } catch (error: any) {
        this.error = error.message || 'Failed to update profile';
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    async updateProfileData(profileData: Partial<ProfileData>) {
      this.loading = true;
      this.error = null;
      try {
        const updatedUser = await userService.updateProfileData(profileData);
        if (updatedUser) {
          this.completeUser = { ...updatedUser };
          this.lastFetchTime = Date.now();
        }
        return true;
      } catch (error: any) {
        this.error = error.message || 'Failed to update profile data';
        return false;
      } finally {
        this.loading = false;
      }
    }
  }
});