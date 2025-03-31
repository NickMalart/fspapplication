import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { UserProfileAdmin, FunctionalGroup } from '@/stores/userProfileAdminStore';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export const userProfileAdminService = {
  /**
   * Fetch a specific user's detailed profile
   */
  async getUserProfile(userId: string): Promise<UserProfileAdmin> {
    try {
      const response = await axios.get(`${API_URL}/account/users/${userId}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      throw error;
    }
  },

  /**
   * Update a user's profile
   */
  async updateUserProfile(userId: string, userData: Partial<UserProfileAdmin>): Promise<UserProfileAdmin> {
    try {
      // Convert data to snake_case for API
      const convertedData = convertObjectKeysToSnake(userData);
      
      // Special handling for functional groups
      if (userData.functionalGroups) {
        convertedData.functional_group_ids = userData.functionalGroups.map(
          (group: FunctionalGroup) => group.id
        );
        delete convertedData.functional_groups;
      }
      
      const response = await axios.put(`${API_URL}/account/users/${userId}/`, convertedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      throw error;
    }
  },

  /**
   * Patch only specific fields of a user's profile
   */
  async patchUserProfile(userId: string, data: any): Promise<UserProfileAdmin> {
    try {
      const convertedData = convertObjectKeysToSnake(data);
      const response = await axios.patch(`${API_URL}/account/users/${userId}/`, convertedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      throw error;
    }
  },

  /**
   * Update a user's active status
   */
  async updateUserStatus(userId: string, isActive: boolean): Promise<UserProfileAdmin> {
    try {
      return await this.patchUserProfile(userId, { isActive });
    } catch (error) {
      throw error;
    }
  },

  /**
   * Update a user's functional groups
   */
  async updateFunctionalGroups(userId: string, groupIds: string[]): Promise<UserProfileAdmin> {
    try {
      return await this.patchUserProfile(userId, { functionalGroupIds: groupIds });
    } catch (error) {
      throw error;
    }
  }
}; 