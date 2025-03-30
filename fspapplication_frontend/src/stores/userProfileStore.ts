import { defineStore } from 'pinia';
import { userService, UserLogin, CompleteUser, ProfileData } from '@/service/userProfileService';

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
      // If we're already loading, don't start another request
      if (this.loading) {
        console.log('Already loading user data, skipping duplicate request');
        return this.currentUser;
      }
      
      this.loading = true;
      this.error = null;
      try {
        this.currentUser = await userService.getCurrentUser();
        return this.currentUser;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch user data';
        console.error('Store error:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchUserProfile(forceRefresh = false) {
      // Use cached data if valid and not forcing refresh
      if (!forceRefresh && this.isCacheValid) {
        console.log('Using cached profile data');
        return this.completeUser;
      }
      
      // If we're already loading, don't start another request
      if (this.loading) {
        console.log('Already loading profile data, skipping duplicate request');
        return this.completeUser;
      }
      
      this.loading = true;
      this.error = null;
      try {
        console.log('Fetching user profile...');
        const userData = await userService.getUserProfile();
        
        // Update state
        this.completeUser = { ...userData };
        this.lastFetchTime = Date.now();
        
        return this.completeUser;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch user profile';
        console.error('Store error:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateUserProfile(userData: Partial<CompleteUser>) {
      this.loading = true;
      this.error = null;
      try {
        console.log('Updating user profile with:', userData);
        const updatedUser = await userService.updateUserProfile(userData);
        
        // Update the state with the returned data
        this.completeUser = { ...updatedUser };
        this.lastFetchTime = Date.now();
        
        return true;
      } catch (error: any) {
        this.error = error.message || 'Failed to update profile';
        console.error('Store error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    async updateProfileData(profileData: Partial<ProfileData>) {
      this.loading = true;
      this.error = null;
      try {
        console.log('Updating profile data with:', profileData);
        const updatedUser = await userService.updateProfileData(profileData);
        
        // Update state
        if (updatedUser) {
          this.completeUser = { ...updatedUser };
          this.lastFetchTime = Date.now();
        }
        
        return true;
      } catch (error: any) {
        this.error = error.message || 'Failed to update profile data';
        console.error('Store error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    }
  }
});