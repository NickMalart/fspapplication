import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { companyService, CompanyProfile } from '@/service/companyService';

export const usecompanyStore = defineStore('companyProfile', () => {
  // State
  const companyProfile = ref<CompanyProfile | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const lastFetchTime = ref<number | null>(null);
  const consecutiveErrors = ref(0);
  
  // Cache settings
  const CACHE_TTL = 5 * 60 * 1000; // 5 minutes
  const MAX_CONSECUTIVE_ERRORS = 3;
  const ERROR_COOLDOWN = 30 * 1000; // 30 seconds
  
  // Getters
  const hasCompanyInfo = computed(() => !!companyProfile.value);
  
  const isCacheValid = computed(() => {
    if (!lastFetchTime.value) return false;
    return Date.now() - lastFetchTime.value < CACHE_TTL;
  });

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
    // Return cached data if still valid
    if (isCacheValid.value && companyProfile.value) {
      console.log('Using cached company profile data');
      return companyProfile.value;
    }
    
    // If we've had too many consecutive errors, don't try again until cooldown period
    if (consecutiveErrors.value >= MAX_CONSECUTIVE_ERRORS) {
      const timeSinceLastAttempt = lastFetchTime.value ? Date.now() - lastFetchTime.value : Infinity;
      if (timeSinceLastAttempt < ERROR_COOLDOWN) {
        console.warn(`Too many API errors. Waiting for cooldown period (${Math.round((ERROR_COOLDOWN - timeSinceLastAttempt)/1000)}s remaining)`);
        return companyProfile.value;
      }
    }
    
    // If already loading, return current data
    if (loading.value) {
      console.log('Already fetching company profile data');
      return companyProfile.value;
    }
    
    loading.value = true;
    error.value = null;
    
    try {
      const data = await companyService.getCompanyProfile();
      lastFetchTime.value = Date.now();
      
      if (data) {
        companyProfile.value = data;
        consecutiveErrors.value = 0; // Reset error counter on success
      } else {
        error.value = 'No company profile data received';
        consecutiveErrors.value++;
      }
      
      return companyProfile.value;
    } catch (err) {
      console.error('Failed to load company profile:', err);
      error.value = 'Could not connect to server. Please try again later.';
      consecutiveErrors.value++;
      return companyProfile.value;
    } finally {
      loading.value = false;
    }
  };

  const updateCompanyProfile = async (data: Partial<CompanyProfile>) => {
    // If we've had too many consecutive errors, don't try again until cooldown period
    if (consecutiveErrors.value >= MAX_CONSECUTIVE_ERRORS) {
      const timeSinceLastAttempt = lastFetchTime.value ? Date.now() - lastFetchTime.value : Infinity;
      if (timeSinceLastAttempt < ERROR_COOLDOWN) {
        error.value = 'Server connection issues. Please try again later.';
        return false;
      }
    }
    
    loading.value = true;
    error.value = null;
    
    try {
      const result = await companyService.updateCompanyProfile(data);
      lastFetchTime.value = Date.now();
      
      if (result.success && result.company) {
        companyProfile.value = result.company;
        consecutiveErrors.value = 0; // Reset error counter on success
        return true;
      } else {
        error.value = result.error || 'Failed to update company profile';
        consecutiveErrors.value++;
        return false;
      }
    } catch (err) {
      error.value = 'Could not connect to server. Please try again later.';
      console.error('Failed to update company profile:', err);
      consecutiveErrors.value++;
      return false;
    } finally {
      loading.value = false;
    }
  };

  const resetState = () => {
    companyProfile.value = null;
    loading.value = false;
    error.value = null;
    lastFetchTime.value = null;
    consecutiveErrors.value = 0;
  };

  return {
    // State
    companyProfile,
    loading,
    error,
    lastFetchTime,
    
    // Getters
    hasCompanyInfo,
    fullAddress,
    isCacheValid,
    
    // Actions
    fetchCompanyProfile,
    updateCompanyProfile,
    resetState
  };
}); 