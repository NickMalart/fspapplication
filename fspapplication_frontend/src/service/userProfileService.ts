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

let isRefreshingToken = false;
let tokenRefreshPromise: Promise<any> | null = null;

export const userService = {
  async handleAuthError(error: any): Promise<never> {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      if (!isRefreshingToken) {
        isRefreshingToken = true;
        tokenRefreshPromise = axios.post(`${API_URL}/account/token/refresh/`)
          .then(response => {
            return response.data;
          })
          .catch(refreshError => {
            window.location.href = '/login';
            return Promise.reject(refreshError);
          })
          .finally(() => {
            isRefreshingToken = false;
            tokenRefreshPromise = null;
          });
      }
      
      if (tokenRefreshPromise) {
        await tokenRefreshPromise;
        const retryError = new Error('Token refreshed, retry request');
        retryError.name = 'RetryAfterRefresh';
        throw retryError;
      }
    }
    
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
      if (error.name === 'RetryAfterRefresh') {
        return this.getUserProfile();
      }
      return this.handleAuthError(error);
    }
  },
  
  async updateUserProfile(userData: Partial<CompleteUser>): Promise<CompleteUser> {
    try {
      const simplifiedData: any = {};
      
      if (userData.avatar !== undefined) simplifiedData.avatar = userData.avatar;
      if (userData.firstName !== undefined) simplifiedData.first_name = userData.firstName;
      if (userData.lastName !== undefined) simplifiedData.last_name = userData.lastName;
      if (userData.email !== undefined) simplifiedData.email = userData.email;
      
      if (userData.profile) {
        simplifiedData.profile = convertObjectKeysToSnake(userData.profile);
      }
      
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, simplifiedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      if (error.name === 'RetryAfterRefresh') {
        return this.updateUserProfile(userData);
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