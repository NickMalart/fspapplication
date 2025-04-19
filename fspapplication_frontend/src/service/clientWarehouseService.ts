import apiClient from './api'; 
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';
import { formatLatLong } from '@/utils/formatters';
import type { AxiosResponse } from 'axios';

// Warehouse model definition (matching backend)
export interface Warehouse {
  id: string;
  name: string;
  client: string; // Client ID
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
  contactName?: string | null; // Optional as it's a property on the backend
  contactPhone: string | null;
  contactEmail: string | null;
  isPrimary: boolean;
  operatingHours: string | null;
  storageCapacity: string | null;
  specialInstructions: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

// Response for listing warehouses
export interface WarehousesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Warehouse[];
}

// Parameters for listing warehouses
export interface WarehouseListParams {
  search?: string;
  ordering?: string;
  page?: number;
  pageSize?: number;
  status?: 'active' | 'inactive' | 'all';
}

export const clientWarehouseService = {
  async getWarehouses(clientId: string, params: WarehouseListParams = {}): Promise<WarehousesResponse> {
    if (!clientId) {
      throw new Error('Client ID is required to fetch warehouses');
    }
    try {
      const apiParams = convertObjectKeysToSnake(params);
      
      // Remove undefined or null parameters
      Object.keys(apiParams).forEach(key => 
        (apiParams[key] === undefined || apiParams[key] === null) && delete apiParams[key]
      );

      const response = await apiClient.get(`client/clients/${clientId}/warehouses/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((warehouse: any) => convertObjectKeysToCamel(warehouse))
      };
    } catch (error: any) {
      console.error('Error fetching warehouses:', error);
      throw error;
    }
  },

  async getWarehouseById(clientId: string, warehouseId: string): Promise<Warehouse> {
    if (!clientId || !warehouseId) {
      throw new Error('Client ID and Warehouse ID are required to fetch a warehouse');
    }
    try {
      const response = await apiClient.get(`client/clients/${clientId}/warehouses/${warehouseId}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error fetching warehouse with ID ${warehouseId}:`, error);
      throw error;
    }
  },

  async createWarehouse(clientId: string, warehouseData: Partial<Warehouse>): Promise<Warehouse> {
    if (!clientId) {
      throw new Error('Client ID is required to create a warehouse');
    }
    try {
      const apiData = convertObjectKeysToSnake({ ...warehouseData, client: clientId });
      
      // Format latitude and longitude using the utility function
      apiData.latitude = formatLatLong(apiData.latitude);
      apiData.longitude = formatLatLong(apiData.longitude);

      const response: AxiosResponse<Warehouse> = await apiClient.post(
        `client/clients/${clientId}/warehouses/`, 
        apiData
      );
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error creating warehouse:', error);
      throw error;
    }
  },

  async updateWarehouse(clientId: string, warehouseId: string, warehouseData: Partial<Warehouse>): Promise<Warehouse> {
    if (!clientId || !warehouseId) {
      throw new Error('Client ID and Warehouse ID are required to update a warehouse');
    }
    try {
       const apiData = convertObjectKeysToSnake(warehouseData);

       // Format latitude and longitude using the utility function
       apiData.latitude = formatLatLong(apiData.latitude);
       apiData.longitude = formatLatLong(apiData.longitude);

      const response: AxiosResponse<Warehouse> = await apiClient.patch(
        `client/clients/${clientId}/warehouses/${warehouseId}/`,
        apiData
      );
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating warehouse:', error);
      throw error;
    }
  },

  async updateWarehouseStatus(clientId: string, warehouseId: string, isActive: boolean): Promise<Warehouse> {
    if (!clientId || !warehouseId) {
      throw new Error('Client ID and Warehouse ID are required to update warehouse status');
    }
    try {
      const response: AxiosResponse<Warehouse> = await apiClient.patch(
        `client/clients/${clientId}/warehouses/${warehouseId}/`, 
        { is_active: isActive } // Only send the status field
      );
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating warehouse status:', error);
      throw error;
    }
  }
}; 