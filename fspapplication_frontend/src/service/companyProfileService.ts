import apiClient from './api';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

// Remove or adjust the API_URL to avoid duplication
// const API_URL = import.meta.env.VITE_API_URL || '/api';

export interface CompanyProfile {
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
  createdAt: string;
  updatedAt: string;
}

export interface CompanyUpdateResponse {
  success: boolean;
  company?: CompanyProfile;
  error?: string;
}

export const companyProfileService = {
  /**
   * Fetch the company profile information
   * @returns Promise with company profile data
   */
  async getCompanyProfile(): Promise<CompanyProfile | null> {
    try {
      const response = await apiClient.get('/company/');
      return convertObjectKeysToCamel(response.data);
    } catch (error) {
      console.error('Failed to fetch company profile:', error);
      return null;
    }
  },

  /**
   * Update the company profile
   * @param companyData The company data to update
   * @returns Promise with update result
   */
  async updateCompanyProfile(companyData: Partial<CompanyProfile>): Promise<CompanyUpdateResponse> {
    try {
      const response = await apiClient.patch('/company/', companyData);
      return {
        success: true,
        company: convertObjectKeysToCamel(response.data),
      };
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { error?: string } }, message?: string };
      return {
        success: false,
        error: axiosError.response?.data?.error || axiosError.message || 'Failed to update company profile',
      };
    }
  }
}; 