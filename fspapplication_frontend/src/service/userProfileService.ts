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
      
      // Convert userData to appropriate format for backend
      const transformedData: any = { ...userData };
      
      // If profile data exists, convert from camelCase to snake_case
      if (transformedData.profile) {
        const profileData: any = { ...transformedData.profile };
        
        // Convert dateOfBirth to date_of_birth
        if ('dateOfBirth' in profileData) {
          profileData.date_of_birth = profileData.dateOfBirth;
          delete profileData.dateOfBirth;
        }
        
        // Convert other camelCase keys to snake_case
        Object.keys(profileData).forEach(key => {
          if (key.includes('_')) return; // Already snake_case
          
          const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
          if (key !== snakeKey) {
            profileData[snakeKey] = profileData[key];
            delete profileData[key];
          }
        });
        
        transformedData.profile = profileData;
      }
      
      console.log('Transformed data for backend:', transformedData);
      const response = await axios.put(`${API_URL}/account/user/profile/update/`, transformedData);
      const updatedData = response.data;
      console.log('Update response:', updatedData);
      return updatedData;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  },
  
  async updateProfileData(profileData: Partial<ProfileData>): Promise<CompleteUser> {
    // Format date_of_birth to YYYY-MM-DD if it exists - adding debug statements
    console.log('Original date received in service:', profileData.dateOfBirth);
    
    if (profileData.dateOfBirth) {
      try {
        // Date is already in YYYY-MM-DD format when coming from the date picker
        // Just ensure it's valid
        const date = new Date(profileData.dateOfBirth);
        if (!isNaN(date.getTime())) {
          // Ensure it's in YYYY-MM-DD format without timezone or time part
          const formattedDate = date.toISOString().split('T')[0];
          console.log('Date is valid, formatted as:', formattedDate);
          profileData.dateOfBirth = formattedDate;
        } else {
          console.error('Invalid date received:', profileData.dateOfBirth);
          profileData.dateOfBirth = null;
        }
      } catch (e) {
        console.error('Error handling date:', e);
        profileData.dateOfBirth = null;
      }
    }
    
    console.log('Final profile data to be sent:', profileData);
    
    // Create a properly formatted update object with snake_case keys for backend
    const updateData: Partial<CompleteUser> = {
      profile: profileData as unknown as ProfileData
    };
    
    console.log('Full update data object:', updateData);
    
    // Call updateUserProfile and return its result directly
    const result = await this.updateUserProfile(updateData);
    
    // Force a refresh of the user profile to ensure we have the latest data
    const refreshedProfile = await this.getUserProfile();
    
    // Return the refreshed profile instead of the update result
    return refreshedProfile;
  }
};