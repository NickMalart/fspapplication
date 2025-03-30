import axios from 'axios';
import { convertObjectKeysToSnake, convertObjectKeysToCamel } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export interface UserLogin {
  id: string; 
  email: string;
}

export interface ProfileData {
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
}

export interface CompleteUser {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  userType: string;
  avatar: string | null;
  isActive: boolean;
  isSuperuser: boolean;
  isStaff: boolean;
  dateJoined: string;
  lastLogin: string | null;
  functionalGroups: any[];
  profile: ProfileData;
}

// Create a flag to track if we're already refreshing tokens to prevent multiple attempts
let isRefreshingToken = false;
let tokenRefreshPromise: Promise<any> | null = null;

export const userService = {
  async handleAuthError(error: any): Promise<never> {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      // If we're not already refreshing the token
      if (!isRefreshingToken) {
        isRefreshingToken = true;
        tokenRefreshPromise = axios.post(`${API_URL}/account/token/refresh/`)
          .then(response => {
            // Token refreshed successfully, save new tokens
            console.log('Token refreshed successfully');
            return response.data;
          })
          .catch(refreshError => {
            console.error('Token refresh failed, redirecting to login');
            // Redirect to login page
            window.location.href = '/login';
            return Promise.reject(refreshError);
          })
          .finally(() => {
            isRefreshingToken = false;
            tokenRefreshPromise = null;
          });
      }
      
      // Wait for the token refresh to complete
      if (tokenRefreshPromise) {
        await tokenRefreshPromise;
        // Throw a custom error to indicate we should retry the original request
        const retryError = new Error('Token refreshed, retry request');
        retryError.name = 'RetryAfterRefresh';
        throw retryError;
      }
    }
    
    // For non-auth errors or if token refresh is not possible, just throw the original error
    throw error;
  },
  
  async getCurrentUser(): Promise<UserLogin> {
    try {
      const response = await axios.get(`${API_URL}/account/user/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      return this.handleAuthError(error);
    }
  },
  
  async getUserProfile(): Promise<CompleteUser> {
    try {
      const response = await axios.get(`${API_URL}/account/user/profile/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      // Special case for RetryAfterRefresh - retry the original request
      if (error.name === 'RetryAfterRefresh') {
        return this.getUserProfile();
      }
      return this.handleAuthError(error);
    }
  },
  
  async updateUserProfile(userData: Partial<CompleteUser>): Promise<CompleteUser> {
    try {
      // Create a simplified version of the data with only the fields we're updating
      const simplifiedData: any = {};
      
      // Extract only the fields that are present in userData
      if (userData.avatar !== undefined) simplifiedData.avatar = userData.avatar;
      if (userData.firstName !== undefined) simplifiedData.first_name = userData.firstName;
      if (userData.lastName !== undefined) simplifiedData.last_name = userData.lastName;
      if (userData.email !== undefined) simplifiedData.email = userData.email;
      
      // Handle profile data separately
      if (userData.profile) {
        simplifiedData.profile = convertObjectKeysToSnake(userData.profile);
      }
      
      console.log('Sending data to API:', simplifiedData);
      
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, simplifiedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      // Special case for RetryAfterRefresh - retry the original request
      if (error.name === 'RetryAfterRefresh') {
        return this.updateUserProfile(userData);
      }
      
      console.error('Error updating profile:', error);
      if (axios.isAxiosError(error) && error.response) {
        console.error('API Error Status:', error.response.status);
        console.error('API Error Response Data:', error.response.data);
      }
      return this.handleAuthError(error);
    }
  },
  
  async updateProfileData(profileData: Partial<ProfileData>): Promise<CompleteUser> {
    if (profileData.dateOfBirth) {
      try {
        const date = new Date(profileData.dateOfBirth);
        if (!isNaN(date.getTime())) {
          profileData.dateOfBirth = date.toISOString().split('T')[0];
        } else {
          profileData.dateOfBirth = null;
        }
      } catch (e) {
        profileData.dateOfBirth = null;
      }
    }
    
    const updateData: Partial<CompleteUser> = {
      profile: profileData as unknown as ProfileData
    };
    
    await this.updateUserProfile(updateData);
    return this.getUserProfile();
  }
};