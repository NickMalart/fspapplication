import apiClient from './api'; // Import the shared client
// import axios from 'axios'; // Remove direct axios import
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { UserProfileAdmin, FunctionalGroup } from '@/stores/userProfileAdminStore';

// const API_URL = import.meta.env.VITE_API_URL || '/api'; // Remove manual API_URL construction

export const userProfileAdminService = {
  /**
   * Fetch a specific user's detailed profile
   */
  async getUserProfile(userId: string): Promise<UserProfileAdmin> {
    try {
      // Use apiClient and relative path
      const response = await apiClient.get(`account/users/${userId}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      // TODO: Implement proper error handling, potentially using a shared handler
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
      
      // Use apiClient and relative path - Changed to PATCH
      const response = await apiClient.patch(`account/users/${userId}/`, convertedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      // TODO: Implement proper error handling
      throw error;
    }
  },

  /**
   * Patch only specific fields of a user's profile
   */
  async patchUserProfile(userId: string, data: any): Promise<UserProfileAdmin> {
    try {
      const convertedData = convertObjectKeysToSnake(data);
      // Use apiClient and relative path
      const response = await apiClient.patch(`account/users/${userId}/`, convertedData);
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      // TODO: Implement proper error handling
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