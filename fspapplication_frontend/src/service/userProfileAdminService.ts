import apiClient from './api'; 
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { UserProfileAdmin } from '@/stores/userProfileAdminStore';


export const userProfileAdminService = {

  // ============================================================================
  // Fetch User Profile
  // ============================================================================

  async getUserProfile(userId: string): Promise<UserProfileAdmin> {
    try {
      // Use apiClient and relative path
      const response = await apiClient.get(`account/users/${userId}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error(`Error fetching user profile for userId ${userId}:`, error);
      throw error;
    }
  },

  // ============================================================================
  // Update User Profile
  // ============================================================================

  async updateUserProfilePartial(userId: string, data: Partial<UserProfileAdmin>): Promise<UserProfileAdmin> {
    try {
      const convertedData = convertObjectKeysToSnake(data);
      // Use apiClient and relative path
      const response = await apiClient.patch(`account/users/${userId}/`, convertedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error(`Error partially updating user profile for userId ${userId}:`, error);
      throw error;
    }
  },

  async updateUserStatus(userId: string, isActive: boolean): Promise<UserProfileAdmin> {
    try {
      return await this.updateUserProfilePartial(userId, { isActive });
    } catch (error) {
      console.error(`Error updating user status for userId ${userId}:`, error);
      throw error;
    }
  },

}; 