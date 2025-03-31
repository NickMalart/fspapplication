<template>
  <ComponentCard title="Address Information">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-900 text-red-700 dark:text-red-300 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Data Display with Edit Button in Relative Position -->
    <div v-else class="relative">
      <!-- Edit Button -->
      <button 
        v-if="companyProfile" 
        @click="isModalOpen = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="companyProfile" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <!-- Street Address -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Street Address</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatStreetAddress(companyProfile) }}
          </p>
        </div>
        
        <!-- Suburb/City -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Suburb/City</p>
          <p class="font-medium text-black dark:text-white">
            {{ companyProfile.suburb || companyProfile.city || 'Not provided' }}
          </p>
        </div>
        
        <!-- State/Province -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">State/Province</p>
          <p class="font-medium text-black dark:text-white">
            {{ companyProfile.state || 'Not provided' }}
          </p>
        </div>
        
        <!-- Postal Code -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Postal Code</p>
          <p class="font-medium text-black dark:text-white">
            {{ companyProfile.postalCode || 'Not provided' }}
          </p>
        </div>
        
        <!-- Country -->
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Country</p>
          <p class="font-medium text-black dark:text-white">
            {{ companyProfile.country || 'Not provided' }}
          </p>
        </div>
      </div>
      <div v-else class="py-4 text-center text-gray-500">
        No address information available
      </div>
    </div>

    <!-- Edit Modal -->
    <EditCompanyAddressModal
      v-if="isModalOpen && companyProfile"
      :key="modalKey"
      :companyData="companyProfile"
      :isSaving="isSaving"
      @close="isModalOpen = false"
      @save="handleSave"
    />
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { usecompanyStore } from '@/stores/companyStore';
import { storeToRefs } from 'pinia';
import ComponentCard from '@/components/common/ComponentCard.vue';
import EditCompanyAddressModal from '@/components/administration/company/EditCompanyAddressModal.vue';
import { CompanyProfile } from '@/service/companyService';

// Extend CompanyProfile to include any additional fields we need for Google Place
interface ExtendedCompanyProfile extends CompanyProfile {
  googlePlaceId?: string | null;
}

const companyStore = usecompanyStore();
const { companyProfile, loading, error } = storeToRefs(companyStore);

const isModalOpen = ref(false);
const isSaving = ref(false);
const modalKey = ref(0); // Used to force modal re-render

// Format street address
const formatStreetAddress = (profile: any) => {
  if (!profile.streetNumber && !profile.streetName) return 'Not provided';
  
  let address = '';
  if (profile.streetNumber) address += profile.streetNumber;
  if (profile.streetNumber && profile.streetName) address += ' ';
  if (profile.streetName) address += profile.streetName;
  
  return address;
};

// Handle save from modal
const handleSave = async (formData: Partial<ExtendedCompanyProfile>) => {
  isSaving.value = true;
  
  try {
    const addressData: Partial<CompanyProfile> = {
      streetNumber: formData.streetNumber,
      streetName: formData.streetName,
      suburb: formData.suburb,
      city: formData.city,
      state: formData.state,
      postalCode: formData.postalCode,
      country: formData.country,
      latitude: formData.latitude,
      longitude: formData.longitude
    };
    
    await companyStore.updateCompanyProfile(addressData);
    
    // Increment key to force modal re-render on next open
    modalKey.value++;
    
    // Refresh data after saving
    await companyStore.fetchCompanyProfile();
    isModalOpen.value = false;
  } catch (error) {
    console.error('Failed to save address changes:', error);
  } finally {
    isSaving.value = false;
  }
};

// Fetch company data on mount
onMounted(async () => {
  await companyStore.fetchCompanyProfile();
});

// Force refetch when modal closes
watch(isModalOpen, (open) => {
  if (!open) {
    companyStore.fetchCompanyProfile();
  }
});
</script> 