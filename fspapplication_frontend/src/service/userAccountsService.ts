import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import { CompleteUser } from '@/service/userProfileService';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Export the UserAccount type which can reuse CompleteUser
export type UserAccount = CompleteUser;

export interface UsersResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: UserAccount[];
}

export interface UserListParams {
  search?: string;
  status?: 'active' | 'inactive' | 'all';
  ordering?: string;
  page?: number;
  pageSize?: number;
}

export const userAccountsService = {
  async getUsers(params: UserListParams = {}): Promise<UsersResponse> {
    try {
      // Convert all params from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake(params);
      
      const response = await axios.get(`${API_URL}/account/users/`, { params: apiParams });
      
      // Convert the response data from snake_case to camelCase
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((user: any) => convertObjectKeysToCamel(user))
      };
    } catch (error: any) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },
  
  async getUserById(id: string): Promise<UserAccount> {
    try {
      const response = await axios.get(`${API_URL}/account/users/${id}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error fetching user with ID ${id}:`, error);
      throw error;
    }
  },
  
  async updateUserStatus(id: string, isActive: boolean): Promise<UserAccount> {
    try {
      const data = convertObjectKeysToSnake({ isActive });
      const response = await axios.patch(`${API_URL}/account/users/${id}/`, data);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error updating status for user ${id}:`, error);
      throw error;
    }
  }
}; 