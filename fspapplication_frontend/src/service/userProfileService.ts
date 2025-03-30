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

export const userService = {
  async getCurrentUser(): Promise<UserLogin> {
    try {
      const response = await axios.get(`${API_URL}/account/user/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error('Error getting current user:', error);
      throw error;
    }
  },
  
  async getUserProfile(): Promise<CompleteUser> {
    try {
      const response = await axios.get(`${API_URL}/account/user/profile/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error('Error getting user profile:', error);
      throw error;
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
      
      // Log request before sending
      console.log('API Request URL:', `${API_URL}/account/user/profile/update/`);
      console.log('API Request Method: PUT');
      console.log('API Request Headers:', 'Content-Type: application/json');
      console.log('API Request Data:', JSON.stringify(simplifiedData, null, 2));
      
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, simplifiedData);
      console.log('API Response:', response.data);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error('Error updating profile:', error);
      if (axios.isAxiosError(error) && error.response) {
        console.error('API Error Status:', error.response.status);
        console.error('API Error Headers:', error.response.headers);
        console.error('API Error Response Data:', error.response.data);
        
        if (error.request) {
          console.error('API Error Request:', error.request);
        }
      }
      throw error;
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