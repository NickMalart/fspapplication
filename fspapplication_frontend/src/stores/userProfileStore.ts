import { defineStore } from 'pinia';
import { userService, UserLogin, CompleteUser, ProfileData } from '@/service/userProfileService';

interface UserState {
  currentUser: UserLogin | null;
  completeUser: CompleteUser | null;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    currentUser: null,
    completeUser: null,
    loading: false,
    error: null
  }),
  
  getters: {
    // Convenience getter for profile data
    userProfile: (state) => state.completeUser?.profile || null,
    // Full name getter
    fullName: (state) => {
      if (!state.completeUser) return '';
      return `${state.completeUser.first_name} ${state.completeUser.last_name}`.trim();
    }
  },
  
  actions: {
    async fetchCurrentUser() {
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
    
    async fetchUserProfile() {
      this.loading = true;
      this.error = null;
      try {
        this.completeUser = await userService.getUserProfile();
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
        this.completeUser = await userService.updateUserProfile(userData);
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
        this.completeUser = await userService.updateProfileData(profileData);
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