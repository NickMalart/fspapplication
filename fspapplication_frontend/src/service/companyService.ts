import apiClient from './api';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';
import { formatLatLong } from '@/utils/formatters';

// We don't need to add any prefix here since apiClient already has the baseURL set

export interface CompanyProfile {
  id: number;
  name: string;
  logo: string | null;
  streetNumber: string | null;
  streetName: string | null;
  suburb: string | null;
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

export const companyService = {
  /**
   * Fetch the company profile information
   * @returns Promise with company profile data
   */
  async getCompanyProfile(): Promise<CompanyProfile | null> {
    try {
      const response = await apiClient.get('company/');
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
      // Format latitude and longitude first
      const formattedData = {
        ...companyData,
        latitude: formatLatLong(companyData.latitude),
        longitude: formatLatLong(companyData.longitude),
      };

      // Convert camelCase to snake_case for API
      const snakeCaseData = Object.entries(formattedData).reduce((acc, [key, value]) => {
        // Convert camelCase to snake_case: streetName -> street_name
        const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
        acc[snakeKey] = value;
        return acc;
      }, {} as Record<string, any>);
      
      const response = await apiClient.patch('company/', snakeCaseData);
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