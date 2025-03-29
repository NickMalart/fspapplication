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
      const userData = response.data;
      console.log('Profile data from API:', userData);
      return userData;
    } catch (error) {
      console.error('Error getting user profile:', error);
      throw error;
    }
  },
  
  async updateUserProfile(userData: Partial<CompleteUser>): Promise<CompleteUser> {
    try {
      console.log('Sending update data:', userData);
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, userData);
      const updatedData = response.data;
      console.log('Update response:', updatedData);
      return updatedData;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  },
  
  async updateProfileData(profileData: Partial<ProfileData>): Promise<CompleteUser> {
    // Format date_of_birth to YYYY-MM-DD if it exists
    if (profileData.dateOfBirth) {
      try {
        // Ensure the date is in YYYY-MM-DD format
        const date = new Date(profileData.dateOfBirth);
        if (!isNaN(date.getTime())) {
          profileData.dateOfBirth = date.toISOString().split('T')[0];
        }
      } catch (e) {
        console.error('Error formatting date:', e);
      }
    }
    
    console.log('Updating profile data:', profileData);
    
    // Create a properly formatted update object with correct type
    const updateData: Partial<CompleteUser> = {
      profile: profileData as unknown as ProfileData
    };
    
    // Call updateUserProfile and return its result directly
    const result = await this.updateUserProfile(updateData);
    
    // Force a refresh of the user profile to ensure we have the latest data
    const refreshedProfile = await this.getUserProfile();
    
    // Return the refreshed profile instead of the update result
    return refreshedProfile;
  }
};