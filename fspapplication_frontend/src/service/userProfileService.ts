import axios from 'axios';

// Instead of using process.env, use a direct base URL or import from a config file
const API_URL = import.meta.env.VITE_API_URL || '/api';

// Add auth token to all requests
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export interface UserLogin {
  id: string; // UUID is represented as string in TypeScript
  email: string;
}

export interface ProfileData {
  id: string;
  phone_number: string | null;
  emergency_contact: string | null;
  emergency_contact_first_name: string | null;
  emergency_contact_last_name: string | null;
  street_number: string | null;
  street_name: string | null;
  suburb: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
  country: string | null;
  latitude: number | null;
  longitude: number | null;
  google_place_id: string | null;
  date_of_birth: string | null;
  created_at: string;
  updated_at: string;
}

export interface CompleteUser {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
  avatar: string | null;
  is_active: boolean;
  is_superuser: boolean;
  is_staff: boolean;
  date_joined: string;
  last_login: string | null;
  functional_groups: any[];
  profile: ProfileData;
}

export const userService = {
  async getCurrentUser(): Promise<UserLogin> {
    try {
      const response = await axios.get(`${API_URL}/account/user/`);
      return response.data;
    } catch (error) {
      console.error('Error getting current user:', error);
      throw error;
    }
  },
  
  async getUserProfile(): Promise<CompleteUser> {
    try {
      const response = await axios.get(`${API_URL}/account/user/profile/`);
      return response.data;
    } catch (error) {
      console.error('Error getting user profile:', error);
      throw error;
    }
  },
  
  async updateUserProfile(userData: Partial<CompleteUser>): Promise<CompleteUser> {
    try {
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, userData);
      return response.data;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  },
  
  async updateProfileData(profileData: Partial<ProfileData>): Promise<CompleteUser> {
    const updateData: Partial<CompleteUser> = {
      profile: profileData as ProfileData
    };
    
    return this.updateUserProfile(updateData);
  }
};