import apiClient from './api'; // Import the shared client
// import axios from 'axios'; // Remove direct axios import if not needed elsewhere in the file
import { convertObjectKeysToSnake, convertObjectKeysToCamel } from '@/utils/caseConverter';

// const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api'; // Reverted

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
  isTenantOwner: boolean;
  dateJoined: string;
  lastLogin: string | null;
  functionalGroups: any[];
  profile: ProfileData;
}

let isRefreshingToken = false;
let tokenRefreshPromise: Promise<any> | null = null;

export const userService = {
  async handleAuthError(error: any): Promise<never> {
    console.error("[handleAuthError] Error encountered:", error);
    
    if (apiClient.isAxiosError(error) && error.response?.status === 401) {
      console.log("[handleAuthError] 401 Unauthorized error detected.");
      
      if (!isRefreshingToken) {
        console.log("[handleAuthError] Starting token refresh process...");
        isRefreshingToken = true;
        tokenRefreshPromise = apiClient.post(`account/token/refresh/`)
          .then(response => {
            console.log("[handleAuthError] Token refresh successful:", response.data);
            return response.data;
          })
          .catch(refreshError => {
            console.error("[handleAuthError] Token refresh failed:", refreshError);
            // Redirect to login upon refresh token failure
            window.location.href = '/login';
            return Promise.reject(refreshError);
          })
          .finally(() => {
            console.log("[handleAuthError] Token refresh process finished.");
            isRefreshingToken = false;
            tokenRefreshPromise = null;
          });
      }
      
      if (tokenRefreshPromise) {
        await tokenRefreshPromise;
        const retryError = new Error('Token refreshed, retry request');
        retryError.name = 'RetryAfterRefresh';
        console.log("[handleAuthError] Token refreshed. Throwing retry error.");
        throw retryError;
      }
    }
    
    throw error;
  },
  
  async getCurrentUser(): Promise<UserLogin> {
    console.log("[getCurrentUser] Sending GET request to:", `account/user/`);
    try {
      const response = await apiClient.get(`account/user/`);
      console.log("[getCurrentUser] Response received:", response.data);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error("[getCurrentUser] Error occurred:", error);
      return this.handleAuthError(error);
    }
  },
  
  async getUserProfile(): Promise<CompleteUser> {
    try {
      const response = await apiClient.get(`account/user/profile/`);
      console.log(`[getUserProfile] Profile received for user ID: ${response.data.id}`); // Log only ID for confirmation
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error("[getUserProfile] Error occurred:", error);
      if (error.name === 'RetryAfterRefresh') {
        return this.getUserProfile();
      }
      return this.handleAuthError(error);
    }
  },
  
  async updateUserProfile(userData: Partial<CompleteUser>): Promise<CompleteUser> {
    console.log("[updateUserProfile] Updating user profile with data:", userData);
    try {
      const simplifiedData: any = {};
      
      if (userData.avatar !== undefined) simplifiedData.avatar = userData.avatar;
      if (userData.firstName !== undefined) simplifiedData.first_name = userData.firstName;
      if (userData.lastName !== undefined) simplifiedData.last_name = userData.lastName;
      if (userData.email !== undefined) simplifiedData.email = userData.email;
      
      if (userData.profile) {
        simplifiedData.profile = convertObjectKeysToSnake(userData.profile);
      }
      
      console.log("[updateUserProfile] Simplified data to be sent:", simplifiedData);
      const response = await apiClient.put(`account/user/profile/update/`, simplifiedData);
      console.log("[updateUserProfile] Response received:", response.data);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error("[updateUserProfile] Error occurred:", error);
      if (error.name === 'RetryAfterRefresh') {
        console.log("[updateUserProfile] Retrying update after token refresh...");
        return this.updateUserProfile(userData);
      }
      
      return this.handleAuthError(error);
    }
  },
  
  async updateProfileData(profileData: Partial<ProfileData>): Promise<CompleteUser> {
    console.log("[updateProfileData] Updating profile data with:", profileData);
    if (profileData.dateOfBirth) {
      try {
        const date = new Date(profileData.dateOfBirth);
        if (!isNaN(date.getTime())) {
          profileData.dateOfBirth = date.toISOString().split('T')[0];
          console.log("[updateProfileData] Converted dateOfBirth:", profileData.dateOfBirth);
        } else {
          console.warn("[updateProfileData] Provided dateOfBirth is invalid. Setting value to null.");
          profileData.dateOfBirth = null;
        }
      } catch (e) {
        console.error("[updateProfileData] Error converting dateOfBirth:", e);
        profileData.dateOfBirth = null;
      }
    }
    
    const updateData: Partial<CompleteUser> = {
      profile: profileData as unknown as ProfileData
    };
    
    console.log("[updateProfileData] Sending updateUserProfile request with data:", updateData);
    await this.updateUserProfile(updateData);
    return this.getUserProfile();
  }
};
