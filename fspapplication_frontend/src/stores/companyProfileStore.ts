import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { companyProfileService, CompanyProfile } from '@/service/companyProfileService';

export const useCompanyProfileStore = defineStore('companyProfile', () => {
  // State
  const companyProfile = ref<CompanyProfile | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const hasCompanyInfo = computed(() => !!companyProfile.value);

  const fullAddress = computed(() => {
    if (!companyProfile.value) return '';
    
    const parts = [
      companyProfile.value.number,
      companyProfile.value.street,
      companyProfile.value.city,
      companyProfile.value.state,
      companyProfile.value.postalCode,
      companyProfile.value.country
    ].filter(Boolean);
    
    return parts.join(', ');
  });

  // Actions
  const fetchCompanyProfile = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const data = await companyProfileService.getCompanyProfile();
      companyProfile.value = data;
    } catch (err) {
      error.value = 'Failed to load company profile';
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  const updateCompanyProfile = async (data: Partial<CompanyProfile>) => {
    loading.value = true;
    error.value = null;
    
    try {
      const result = await companyProfileService.updateCompanyProfile(data);
      
      if (result.success && result.company) {
        companyProfile.value = result.company;
        return true;
      } else {
        error.value = result.error || 'Failed to update company profile';
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
    companyProfile.value = null;
    loading.value = false;
    error.value = null;
  };

  return {
    // State
    companyProfile,
    loading,
    error,
    
    // Getters
    hasCompanyInfo,
    fullAddress,
    
    // Actions
    fetchCompanyProfile,
    updateCompanyProfile,
    resetState
  };
}); 