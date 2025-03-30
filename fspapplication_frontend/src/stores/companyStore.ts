import { defineStore } from 'pinia';
import { companyService, Company } from '@/service/companyService';

interface CompanyState {
  company: Company | null;
  loading: boolean;
  error: string | null;
  lastFetchTime: number | null;
}

// Cache expiration time in ms (5 minutes)
const CACHE_EXPIRATION = 5 * 60 * 1000;

export const useCompanyStore = defineStore('company', {
  state: (): CompanyState => ({
    company: null,
    loading: false,
    error: null,
    lastFetchTime: null
  }),
  
  getters: {
    // Check if cache is still valid
    isCacheValid: (state): boolean => {
      if (!state.lastFetchTime || !state.company) return false;
      return Date.now() - state.lastFetchTime < CACHE_EXPIRATION;
    },
    
    // Get company name
    companyName: (state): string => {
      return state.company?.name || '';
    },
    
    // Get company logo
    companyLogo: (state): string | null => {
      return state.company?.logo || null;
    },
    
    // Get company colors
    companyColors: (state) => {
      if (!state.company) return { primary: '#3B82F6', secondary: '#1E40AF' };
      return {
        primary: state.company.primaryColor,
        secondary: state.company.secondaryColor
      };
    },
    
    // Get company address
    companyAddress: (state): string => {
      if (!state.company) return '';
      
      const parts = [];
      if (state.company.number) parts.push(state.company.number);
      if (state.company.street) parts.push(state.company.street);
      if (state.company.city) parts.push(state.company.city);
      if (state.company.state) parts.push(state.company.state);
      if (state.company.postalCode) parts.push(state.company.postalCode);
      if (state.company.country) parts.push(state.company.country);
      
      return parts.join(', ');
    }
  },
  
  actions: {
    async fetchCompany(forceRefresh = false) {
      // Use cached data if valid and not forcing refresh
      if (!forceRefresh && this.isCacheValid) {
        console.log('Using cached company data');
        return this.company;
      }
      
      // If we're already loading, don't start another request
      if (this.loading) {
        console.log('Already loading company data, skipping duplicate request');
        return this.company;
      }
      
      this.loading = true;
      this.error = null;
      try {
        console.log('Fetching company data...');
        const companyData = await companyService.getCompany();
        
        // Update state
        this.company = { ...companyData };
        this.lastFetchTime = Date.now();
        
        return this.company;
      } catch (error: any) {
        this.error = error.message || 'Failed to fetch company data';
        console.error('Store error:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    async updateCompany(companyData: Partial<Company>) {
      this.loading = true;
      this.error = null;
      try {
        console.log('Updating company with:', companyData);
        const updatedCompany = await companyService.updateCompany(companyData);
        
        // Update the state with the returned data
        this.company = { ...updatedCompany };
        this.lastFetchTime = Date.now();
        
        return true;
      } catch (error: any) {
        this.error = error.message || 'Failed to update company';
        console.error('Store error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    }
  }
}); 