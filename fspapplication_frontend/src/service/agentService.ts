import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import type { AxiosResponse } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Agent model definition
export interface Agent {
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
  agentType: string | null;
  serviceAreas: string | null;
  specialties: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AgentsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Agent[];
}

export interface AgentListParams {
  search?: string;
  status?: 'active' | 'inactive' | 'all';
  ordering?: string;
  page?: number;
  pageSize?: number;
}

// AgentWarehouse model definition
export interface AgentWarehouse {
  id: string;
  agent: string;
  name: string;
  description: string | null;
  streetNumber: string | null;
  streetName: string | null;
  suburb: string | null;
  city: string | null;
  state: string | null;
  postalCode: string | null;
  country: string | null;
  latitude: number | null;
  longitude: number | null;
  firstName: string | null;
  lastName: string | null;
  contactPhone: string | null;
  contactEmail: string | null;
  isPrimary: boolean;
  operatingHours: string | null;
  facilityType: string | null;
  specialInstructions: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AgentWarehousesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: AgentWarehouse[];
}

export interface AgentWarehouseListParams {
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

export const agentService = {
  async getAgents(params: AgentListParams = {}): Promise<AgentsResponse> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake({
        ...params,
        // Use status parameter directly
        status: params.status,
        // Remove is_active as we're using status instead
        is_active: undefined
      });

      // Remove undefined or null parameters
      Object.keys(apiParams).forEach(key => 
        (apiParams[key] === undefined || apiParams[key] === null) && delete apiParams[key]
      );
      
      const response = await axios.get(`${API_URL}/agent/agents/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((agent: any) => convertObjectKeysToCamel(agent))
      };
    } catch (error: any) {
      console.error('Error fetching agents:', error);
      throw error;
    }
  },
  
  async getAgentById(id: string): Promise<Agent> {
    try {
      const cacheKey = generateCacheKey(`${API_URL}/agent/agents/${id}/`);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      const response = await axios.get(`${API_URL}/agent/agents/${id}/`);
      const agentData = convertObjectKeysToCamel(response.data);
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: agentData
      });
      
      return agentData;
    } catch (error: any) {
      console.error(`Error fetching agent with ID ${id}:`, error);
      throw error;
    }
  },
  
  async createAgent(agentData: Partial<Agent>): Promise<Agent> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(agentData);
      
      // Make API call to create the agent
      const response = await axios.post(`${API_URL}/agent/agents/`, apiData);
      const newAgent = convertObjectKeysToCamel(response.data);
      
      // Clear any cached agent lists since we added a new agent
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/agent/agents/:`)) {
          cache.delete(key);
        }
      }
      
      return newAgent;
    } catch (error: any) {
      console.error('Error creating agent:', error);
      throw error;
    }
  },
  
  async updateAgentStatus(id: string, isActive: boolean): Promise<Agent> {
    try {
      const data = convertObjectKeysToSnake({ isActive });
      const response = await axios.patch(`${API_URL}/agent/agents/${id}/`, data);
      const updatedAgent = convertObjectKeysToCamel(response.data);
      
      // Invalidate related caches
      const agentCacheKey = generateCacheKey(`${API_URL}/agent/agents/${id}/`);
      cache.delete(agentCacheKey);
      
      // Clear any cached agent lists since they might include this agent
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/agent/agents/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedAgent;
    } catch (error: any) {
      console.error(`Error updating status for agent ${id}:`, error);
      throw error;
    }
  },
  
  async updateAgent(agentId: string, data: Partial<Agent>): Promise<Agent> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(data);
      
      const response: AxiosResponse<Agent> = await axios.patch(
        `${API_URL}/agent/agents/${agentId}/`,
        apiData
      );
      
      // Convert response data back to camelCase
      const updatedAgent = convertObjectKeysToCamel(response.data);
      
      // Clear any cached data for this agent
      const cacheKey = generateCacheKey(`${API_URL}/agent/agents/${agentId}/`);
      cache.delete(cacheKey);
      
      // Clear any cached agent lists since they might include this agent
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/agent/agents/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedAgent;
    } catch (error: any) {
      console.error('Error updating agent:', error);
      throw new Error(error.response?.data?.detail || 'Failed to update agent');
    }
  },
  
  // Agent Warehouse methods
  async getAgentWarehouses(agentId: string, params: AgentWarehouseListParams = {}): Promise<AgentWarehousesResponse> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiParams = convertObjectKeysToSnake({
        ...params,
        status: params.status,
        is_active: undefined
      });

      // Remove undefined or null parameters
      Object.keys(apiParams).forEach(key => 
        (apiParams[key] === undefined || apiParams[key] === null) && delete apiParams[key]
      );
      
      const response = await axios.get(`${API_URL}/agent/agents/${agentId}/warehouses/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((warehouse: any) => convertObjectKeysToCamel(warehouse))
      };
    } catch (error: any) {
      console.error(`Error fetching warehouses for agent ${agentId}:`, error);
      throw error;
    }
  },
  
  async getAgentWarehouseById(agentId: string, warehouseId: string): Promise<AgentWarehouse> {
    try {
      const cacheKey = generateCacheKey(`${API_URL}/agent/agents/${agentId}/warehouses/${warehouseId}/`);
      const cachedData = cache.get(cacheKey);
      
      if (cachedData && isCacheValid(cachedData)) {
        return cachedData.data;
      }
      
      const response = await axios.get(`${API_URL}/agent/agents/${agentId}/warehouses/${warehouseId}/`);
      const warehouseData = convertObjectKeysToCamel(response.data);
      
      // Cache the response
      cache.set(cacheKey, {
        timestamp: Date.now(),
        data: warehouseData
      });
      
      return warehouseData;
    } catch (error: any) {
      console.error(`Error fetching warehouse with ID ${warehouseId}:`, error);
      throw error;
    }
  },
  
  async createAgentWarehouse(agentId: string, warehouseData: Partial<AgentWarehouse>): Promise<AgentWarehouse> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(warehouseData);
      
      // Make API call to create the warehouse
      const response = await axios.post(`${API_URL}/agent/agents/${agentId}/warehouses/`, apiData);
      const newWarehouse = convertObjectKeysToCamel(response.data);
      
      // Clear any cached warehouse lists since we added a new warehouse
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/agent/agents/${agentId}/warehouses/:`)) {
          cache.delete(key);
        }
      }
      
      return newWarehouse;
    } catch (error: any) {
      console.error('Error creating agent warehouse:', error);
      throw error;
    }
  },
  
  async updateAgentWarehouse(agentId: string, warehouseId: string, data: Partial<AgentWarehouse>): Promise<AgentWarehouse> {
    try {
      // Convert data from camelCase to snake_case for the API
      const apiData = convertObjectKeysToSnake(data);
      
      const response: AxiosResponse<AgentWarehouse> = await axios.patch(
        `${API_URL}/agent/agents/${agentId}/warehouses/${warehouseId}/`,
        apiData
      );
      
      // Convert response data back to camelCase
      const updatedWarehouse = convertObjectKeysToCamel(response.data);
      
      // Clear any cached data for this warehouse
      const cacheKey = generateCacheKey(`${API_URL}/agent/agents/${agentId}/warehouses/${warehouseId}/`);
      cache.delete(cacheKey);
      
      // Clear any cached warehouse lists since they might include this warehouse
      for (const key of cache.keys()) {
        if (key.startsWith(`${API_URL}/agent/agents/${agentId}/warehouses/:`)) {
          cache.delete(key);
        }
      }
      
      return updatedWarehouse;
    } catch (error: any) {
      console.error('Error updating agent warehouse:', error);
      throw new Error(error.response?.data?.detail || 'Failed to update agent warehouse');
    }
  },
  
  // Method to clear cache if needed
  clearCache(): void {
    cache.clear();
  }
}; 