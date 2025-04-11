import apiClient from './api'; // Import the shared client
// import axios from 'axios'; // Removed
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { CompleteUser } from '@/service/userProfileService';

// const API_URL = import.meta.env.VITE_API_URL || '/api'; // Removed

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
  // Endpoint should be relative path now (e.g., 'account/users/')
  if (!params) return `/api/${endpoint}`; // Add /api prefix for consistency in cache keys
  return `/api/${endpoint}:${JSON.stringify(params)}`; // Add /api prefix for consistency
}

// Helper to check if cache entry is valid
const isCacheValid = (entry: CacheEntry): boolean => {
  return Date.now() - entry.timestamp < CACHE_TTL;
}

export const userAccountsService = {
  async getUsers(params: UserListParams = {}): Promise<UsersResponse> {
    try {
      const apiParams = convertObjectKeysToSnake(params);
      
      // Use relative endpoint for cache key generation
      const cacheKey = generateCacheKey('account/users/', apiParams); 
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      // Use apiClient and relative path
      const response = await apiClient.get('account/users/', { 
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
      // Use relative endpoint for cache key generation
      const cacheKey = generateCacheKey(`account/users/${id}/`);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      // Use apiClient and relative path
      const response = await apiClient.get(`account/users/${id}/`); 
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
      // Use apiClient and relative path
      const response = await apiClient.patch(`account/users/${id}/`, data); 
      const updatedUser = convertObjectKeysToCamel(response.data);
      
      // Invalidate related caches using relative paths
      const userCacheKey = generateCacheKey(`account/users/${id}/`);
      cache.delete(userCacheKey);
      
      for (const key of cache.keys()) {
        // Check against cache keys which now start with /api/
        if (key.startsWith('/api/account/users/') && key.includes(':')) { 
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
      // Use apiClient and relative path
      const response = await apiClient.post('account/users/', data);
      const newUser = convertObjectKeysToCamel(response.data);
      
      for (const key of cache.keys()) {
         // Check against cache keys which now start with /api/
        if (key.startsWith('/api/account/users/') && key.includes(':')) { 
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