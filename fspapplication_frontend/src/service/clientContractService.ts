import apiClient from './api'; // Import the shared client
// import axios from 'axios'; // Remove direct axios import
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';

// const API_URL = import.meta.env.VITE_API_URL || '/api'; // Remove manual API_URL construction

// Contract model definition
export interface Contract {
  id: string;
  name: string;
  client: string;
  description: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ContractsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Contract[];
}

export interface ContractListParams {
  search?: string;
  ordering?: string;
  client?: string;
  page?: number;
  pageSize?: number;
  status?: 'active' | 'inactive' | 'all';
}

export const clientContractService = {
  async getContracts(params: ContractListParams = {}): Promise<ContractsResponse> {
    try {
      const apiParams = convertObjectKeysToSnake(params);
      const clientId = params.client;
      if (!clientId) {
        throw new Error('Client ID is required to fetch contracts');
      }
      // Use apiClient and relative path
      const response = await apiClient.get(`client/clients/${clientId}/contracts/`, { params: apiParams });
      
      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results.map((contract: any) => convertObjectKeysToCamel(contract))
      };
    } catch (error: any) {
      console.error('Error fetching contracts:', error);
      throw error;
    }
  },

  async getContractById(clientId: string, contractId: string): Promise<Contract> {
    try {
      if (!clientId) {
        throw new Error('Client ID is required to fetch a contract');
      }
      // Use apiClient and relative path
      const response = await apiClient.get(`client/clients/${clientId}/contracts/${contractId}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error fetching contract with ID ${contractId}:`, error);
      throw error;
    }
  },

  async createContract(contractData: Partial<Contract>): Promise<Contract> {
    try {
      if (!contractData.client) {
        throw new Error('Client ID is required to create a contract');
      }
      const apiData = convertObjectKeysToSnake(contractData);
      const clientId = contractData.client;
      // Use apiClient and relative path
      const response = await apiClient.post(`client/clients/${clientId}/contracts/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error creating contract:', error);
      throw error;
    }
  },

  async updateContractStatus(clientId: string, contractId: string, isActive: boolean): Promise<Contract> {
    try {
      if (!clientId) {
        throw new Error('Client ID is required to update contract status');
      }
      // Use apiClient and relative path
      const response = await apiClient.patch(`client/clients/${clientId}/contracts/${contractId}/`, {
        is_active: isActive
      });
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating contract status:', error);
      throw error;
    }
  },

  async updateContract(clientId: string, contractId: string, contractData: Partial<Contract>): Promise<Contract> {
    try {
      if (!clientId) {
        throw new Error('Client ID is required to update a contract');
      }
      const apiData = convertObjectKeysToSnake(contractData);
      // Use apiClient and relative path
      const response = await apiClient.patch(`client/clients/${clientId}/contracts/${contractId}/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating contract:', error);
      throw error;
    }
  }
}; 