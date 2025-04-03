import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { AxiosResponse } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Client model definition
export interface Client {
  id: string;
  name: string;
  logo: string | null;
  abn: string | null;
  website: string | null;
  email: string;
  phone: string | null;
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
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ClientsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Client[];
}

export interface ClientListParams {
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

export const clientService = {
  async getClients(params: ClientListParams = {}): Promise<ClientsResponse> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake({
        ...params,
        // Use status parameter directly like contract service
        status: params.status,
        // Remove is_active as we're using status instead
        is_active: undefined
      });

      // Remove undefined or null parameters
      Object.keys(apiParams).forEach(key => 
        (apiParams[key] === undefined || apiParams[key] === null) && delete apiParams[key]
      );
      
      const response = await axios.get(`${API_URL}/client/clients/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((client: any) => convertObjectKeysToCamel(client))
      };
    } catch (error: any) {
      console.error('Error fetching clients:', error);
      throw error;
    }
  },
  
  async getClientById(id: string): Promise<Client> {
    try {
      const cacheKey = generateCacheKey(`${API_URL}/client/clients/${id}/`);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      const response = await axios.get(`${API_URL}/client/clients/${id}/`);
      const clientData = convertObjectKeysToCamel(response.data);
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: clientData
      });
      
      return clientData;
    } catch (error: any) {
      console.error(`Error fetching client with ID ${id}:`, error);
      throw error;
    }
  },
  
  async createClient(clientData: Partial<Client>): Promise<Client> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(clientData);
      
      // Make API call to create the client
      const response = await axios.post(`${API_URL}/client/clients/`, apiData);
      const newClient = convertObjectKeysToCamel(response.data);
      
      // Clear any cached client lists since we added a new client
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/client/clients/:`)) {
          cache.delete(key);
        }
      }
      
      return newClient;
    } catch (error: any) {
      console.error('Error creating client:', error);
      throw error;
    }
  },
  
  async updateClientStatus(id: string, isActive: boolean): Promise<Client> {
    try {
      const data = convertObjectKeysToSnake({ isActive });
      const response = await axios.patch(`${API_URL}/client/clients/${id}/`, data);
      const updatedClient = convertObjectKeysToCamel(response.data);
      
      // Invalidate related caches
      const clientCacheKey = generateCacheKey(`${API_URL}/client/clients/${id}/`);
      cache.delete(clientCacheKey);
      
      // Clear any cached client lists since they might include this client
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/client/clients/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedClient;
    } catch (error: any) {
      console.error(`Error updating status for client ${id}:`, error);
      throw error;
    }
  },
  
  async updateClient(clientId: string, data: Partial<Client>): Promise<Client> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(data);
      
      const response: AxiosResponse<Client> = await axios.patch(
        `${API_URL}/client/clients/${clientId}/`,
        apiData
      );
      
      // Convert response data back to camelCase
      const updatedClient = convertObjectKeysToCamel(response.data);
      
      // Clear any cached data for this client
      const cacheKey = generateCacheKey(`${API_URL}/client/clients/${clientId}/`);
      cache.delete(cacheKey);
      
      // Clear any cached client lists since they might include this client
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/client/clients/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedClient;
    } catch (error: any) {
      console.error('Error updating client:', error);
      throw new Error(error.response?.data?.detail || 'Failed to update client');
    }
  },
  
  // Method to clear cache if needed
  clearCache(): void {
    cache.clear();
  }
}; 