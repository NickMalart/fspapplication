import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';

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
      // Convert all params from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake(params);
      
      // Check cache first
      const cacheKey = generateCacheKey(`${API_URL}/client/clients/`, apiParams);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      // Make a single batch request with all parameters
      const response = await axios.get(`${API_URL}/client/clients/`, { 
        params: apiParams
      });
      
      // Process and transform the response
      const transformedResponse = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((client: any) => convertObjectKeysToCamel(client))
      };
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: transformedResponse
      });
      
      return transformedResponse;
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
  
  // Method to clear cache if needed
  clearCache(): void {
    cache.clear();
  }
}; 