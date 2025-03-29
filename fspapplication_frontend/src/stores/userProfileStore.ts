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
        console.log('Fetching user profile...');
        const userData = await userService.getUserProfile();
        console.log('Fetched user profile:', userData);
        
        // Ensure we're updating the state properly
        this.completeUser = { ...userData };
        
        console.log('Updated state:', this.completeUser);
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
        console.log('User profile updated:', updatedUser);
        
        // Update the state with the returned data
        this.completeUser = { ...updatedUser };
        
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
        console.log('Profile data updated, response:', updatedUser);
        
        // Ensure we're updating the state with the correct data
        if (updatedUser) {
          this.completeUser = { ...updatedUser };
          console.log('State updated to:', this.completeUser);
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