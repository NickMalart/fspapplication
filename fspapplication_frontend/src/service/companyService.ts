import axios from 'axios';
import { convertObjectKeysToSnake, convertObjectKeysToCamel } from '@/utils/caseConverter';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export interface Company {
  id: number;
  name: string;
  logo: string | null;
  number: string | null;
  street: string | null;
  city: string | null;
  state: string | null;
  postalCode: string | null;
  country: string | null;
  latitude: number | null;
  longitude: number | null;
  phone: string | null;
  email: string | null;
  website: string | null;
  taxNumber: string | null;
  abnNumber: string | null;
  primaryColor: string;
  secondaryColor: string;
  establishedDate: string | null;
}

// Create a flag to track if we're already refreshing tokens to prevent multiple attempts
let isRefreshingToken = false;
let tokenRefreshPromise: Promise<any> | null = null;

export const companyService = {
  async handleAuthError(error: any): Promise<never> {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      // If we're not already refreshing the token
      if (!isRefreshingToken) {
        isRefreshingToken = true;
        tokenRefreshPromise = axios.post(`${API_URL}/account/token/refresh/`)
          .then(response => {
            // Token refreshed successfully, save new tokens
            console.log('Token refreshed successfully');
            return response.data;
          })
          .catch(refreshError => {
            console.error('Token refresh failed, redirecting to login');
            // Redirect to login page
            window.location.href = '/login';
            return Promise.reject(refreshError);
          })
          .finally(() => {
            isRefreshingToken = false;
            tokenRefreshPromise = null;
          });
      }
      
      // Wait for the token refresh to complete
      if (tokenRefreshPromise) {
        await tokenRefreshPromise;
        // Throw a custom error to indicate we should retry the original request
        const retryError = new Error('Token refreshed, retry request');
        retryError.name = 'RetryAfterRefresh';
        throw retryError;
      }
    }
    
    // For non-auth errors or if token refresh is not possible, just throw the original error
    throw error;
  },
  
  async getCompany(): Promise<Company> {
    try {
      const response = await axios.get(`${API_URL}/organisation/company/`);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      // Special case for RetryAfterRefresh - retry the original request
      if (error.name === 'RetryAfterRefresh') {
        return this.getCompany();
      }
      return this.handleAuthError(error);
    }
  },
  
  async updateCompany(companyData: Partial<Company>): Promise<Company> {
    try {
      // Convert camelCase keys to snake_case for API
      const snakeCaseData = convertObjectKeysToSnake(companyData);
      
      console.log('Sending company data to API:', snakeCaseData);
      
      const response = await axios.put(`${API_URL}/organisation/company/`, snakeCaseData);
      return convertObjectKeysToCamel(response.data);
    } catch (error: any) {
      // Special case for RetryAfterRefresh - retry the original request
      if (error.name === 'RetryAfterRefresh') {
        return this.updateCompany(companyData);
      }
      
      console.error('Error updating company:', error);
      if (axios.isAxiosError(error) && error.response) {
        console.error('API Error Status:', error.response.status);
        console.error('API Error Response Data:', error.response.data);
      }
      return this.handleAuthError(error);
    }
  }
}; 