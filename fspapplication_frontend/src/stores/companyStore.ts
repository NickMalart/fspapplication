import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { companyProfileService, CompanyProfile } from '@/service/companyProfileService';

// Company type is an alias for CompanyProfile
export type Company = CompanyProfile;

export const useCompanyStore = defineStore('company', () => {
  // State
  const company = ref<Company | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const lastFetchTime = ref<number | null>(null);

  // Cache validity check (5 minutes)
  const isCacheValid = computed(() => {
    if (!lastFetchTime.value) return false;
    const fiveMinutesInMs = 5 * 60 * 1000;
    return Date.now() - lastFetchTime.value < fiveMinutesInMs;
  });

  // Actions
  const fetchCompany = async (force = false) => {
    // Skip fetch if cache is valid and not forced
    if (isCacheValid.value && !force) {
      return company.value;
    }

    loading.value = true;
    error.value = null;
    
    try {
      const data = await companyProfileService.getCompanyProfile();
      company.value = data;
      lastFetchTime.value = Date.now();
      return data;
    } catch (err) {
      error.value = 'Failed to load company information';
      console.error(err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  const updateCompany = async (data: Partial<Company>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const result = await companyProfileService.updateCompanyProfile(data);
      
      if (result.success && result.company) {
        company.value = result.company;
        lastFetchTime.value = Date.now();
        return true;
      } else {
        error.value = result.error || 'Failed to update company information';
        return false;
      }
    } catch (err) {
      error.value = 'An unexpected error occurred';
      console.error(err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  const resetState = () => {
    company.value = null;
    loading.value = false;
    error.value = null;
    lastFetchTime.value = null;
  };

  return {
    // State
    company,
    loading,
    error,
    lastFetchTime,
    
    // Getters
    isCacheValid,
    
    // Actions
    fetchCompany,
    updateCompany,
    resetState
  };
}); 