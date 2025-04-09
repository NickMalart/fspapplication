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

// Simple in-memory cache to avoid duplicate requests
interface CacheEntry {
  timestamp: number;
  data: any;
}

const cache: Map<string, CacheEntry> = new Map();
const CACHE_TTL = 60 * 1000; // 60 seconds

// Generate a cache key from request parameters
const generateCacheKey = (endpoint: string, params?: any): string => {
  if (!params) return endpoint;
  return `${endpoint}:${JSON.stringify(params)}`;
}

// Helper to check if cache entry is valid
const isCacheValid = (entry: CacheEntry): boolean => {
  return Date.now() - entry.timestamp < CACHE_TTL;
}

export const userAccountsService = {
  async getUsers(params: UserListParams = {}): Promise<UsersResponse> {
    try {
      // Convert all params from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake(params);
      
      // Check cache first
      const cacheKey = generateCacheKey(`${API_URL}/account/users/`, apiParams);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      // Make a single batch request with all parameters
      const response = await axios.get(`${API_URL}/account/users/`, { 
        params: apiParams
      });
      
      // Process and transform the response
      const transformedResponse = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((user: any) => convertObjectKeysToCamel(user))
      };
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: transformedResponse
      });
      
      return transformedResponse;
    } catch (error: any) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },
  
  async getUserById(id: string): Promise<UserAccount> {
    try {
      const cacheKey = generateCacheKey(`${API_URL}/account/users/${id}/`);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      const response = await axios.get(`${API_URL}/account/users/${id}/`);
      const userData = convertObjectKeysToCamel(response.data);
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: userData
      });
      
      return userData;
    } catch (error: any) {
      console.error(`Error fetching user with ID ${id}:`, error);
      throw error;
    }
  },
  
  async updateUserStatus(id: string, isActive: boolean): Promise<UserAccount> {
    try {
      const data = convertObjectKeysToSnake({ isActive });
      const response = await axios.patch(`${API_URL}/account/users/${id}/`, data);
      const updatedUser = convertObjectKeysToCamel(response.data);
      
      // Invalidate related caches
      const userCacheKey = generateCacheKey(`${API_URL}/account/users/${id}/`);
      cache.delete(userCacheKey);
      
      // Clear any cached user lists since they might include this user
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/account/users/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedUser;
    } catch (error: any) {
      console.error(`Error updating status for user ${id}:`, error);
      throw error;
    }
  },
  
  async createUser(userData: Partial<UserAccount>): Promise<UserAccount> {
    try {
      const data = convertObjectKeysToSnake(userData);
      const response = await axios.post(`${API_URL}/account/users/`, data);
      const newUser = convertObjectKeysToCamel(response.data);
      
      // Clear any cached user lists since they might include this user
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/account/users/:`)) {
          cache.delete(key);
        }
      }
      
      return newUser;
    } catch (error: any) {
      console.error('Error creating user:', error);
      throw error;
    }
  },
  
  // Method to clear cache if needed
  clearCache(): void {
    cache.clear();
  }
}; 