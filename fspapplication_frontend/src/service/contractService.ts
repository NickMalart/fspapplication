import axios from 'axios';
import { convertObjectKeysToCamel, convertObjectKeysToSnake } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';

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

export const contractService = {
  async getContracts(params: ContractListParams = {}): Promise<ContractsResponse> {
    try {
      const apiParams = convertObjectKeysToSnake(params);
      const clientId = params.client;
      const response = await axios.get(`${API_URL}/client/clients/${clientId}/contracts/`, { params: apiParams });
      
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

  async getContractById(id: string): Promise<Contract> {
    try {
      const response = await axios.get(`${API_URL}/client/clients/${id}/contracts/${id}/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error(`Error fetching contract with ID ${id}:`, error);
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
      const response = await axios.post(`${API_URL}/client/clients/${clientId}/contracts/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error creating contract:', error);
      throw error;
    }
  },

  async updateContractStatus(contractId: string, isActive: boolean): Promise<Contract> {
    try {
      const response = await axios.patch(`${API_URL}/client/clients/${contractId}/contracts/${contractId}/`, {
        is_active: isActive
      });
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating contract status:', error);
      throw error;
    }
  },

  async updateContract(contractId: string, contractData: Partial<Contract>): Promise<Contract> {
    try {
      const apiData = convertObjectKeysToSnake(contractData);
      const response = await axios.patch(`${API_URL}/client/clients/${contractId}/contracts/${contractId}/`, apiData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      console.error('Error updating contract:', error);
      throw error;
    }
  }
}; 