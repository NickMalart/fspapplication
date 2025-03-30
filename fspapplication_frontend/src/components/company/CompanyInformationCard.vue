<template>
  <ComponentCard title="Company Information">
    <!-- Debug Info (Remove in production) -->
    <pre v-if="false" class="text-xs bg-gray-100 dark:bg-gray-800 p-2 mb-4 overflow-auto">
      companyProfile: {{ JSON.stringify(companyProfile, null, 2) }}
      company: {{ JSON.stringify(company, null, 2) }}
    </pre>

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
        v-if="company" 
        @click="isModalOpen = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <div v-if="company" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-black dark:text-white">
            {{ company.name || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Phone</p>
          <p class="font-medium text-black dark:text-white">
            {{ company.phone || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Email</p>
          <p class="font-medium text-black dark:text-white">
            {{ company.email || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Website</p>
          <p class="font-medium text-black dark:text-white">
            <a 
              v-if="company.website" 
              :href="formatWebsiteUrl(company.website)" 
              target="_blank" 
              class="text-brand-500 hover:underline"
            >
              {{ company.website }}
            </a>
            <span v-else>Not provided</span>
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Tax Number</p>
          <p class="font-medium text-black dark:text-white">
            {{ company.taxNumber || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Business Registration Number</p>
          <p class="font-medium text-black dark:text-white">
            {{ company.abnNumber || 'Not provided' }}
          </p>
        </div>
      </div>
      <div v-else class="py-4 text-center text-gray-500">
        No company information available
      </div>
    </div>

    <!-- Edit Modal with key to force re-render -->
    <EditCompanyInformationModal
      v-if="isModalOpen && company"
      :key="modalKey"
      :companyData="company"
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
import EditCompanyInformationModal from '@/components/company/EditCompanyInformationModal.vue';

const companyStore = usecompanyStore();
const { companyProfile, loading, error } = storeToRefs(companyStore);

const company = computed(() => {
  console.log('Computing company:', companyProfile.value);
  return companyProfile.value;
});
const isModalOpen = ref(false);
const isSaving = ref(false);
const modalKey = ref(0); // Used to force modal re-render

// Format website URL to ensure it has http/https
const formatWebsiteUrl = (url: string) => {
  if (!url) return '';
  return url.startsWith('http') ? url : `https://${url}`;
};

// Handle save from modal
const handleSave = async (formData: { 
  name: string | undefined, 
  phone: string | undefined, 
  email: string | undefined, 
  website: string | undefined 
}) => {
  isSaving.value = true;
  
  try {
    console.log('Sending company data to store:', formData);
    const success = await companyStore.updateCompanyProfile(formData);
    console.log('Update result:', success);
    
    // Increment key to force modal re-render on next open
    modalKey.value++;
    
    // Refresh data after saving
    await companyStore.fetchCompanyProfile();
    isModalOpen.value = false;
  } catch (error) {
    console.error('Failed to save company changes:', error);
  } finally {
    isSaving.value = false;
  }
};

// Fetch company data on mount
onMounted(async () => {
  console.log('Company card mounted, fetching company data');
  await companyStore.fetchCompanyProfile();
});

// Debug log when company data changes
watch(() => companyProfile.value, (newValue) => {
  console.log('companyProfile changed:', newValue);
}, { deep: true });

watch(company, (newCompany) => {
  console.log('company computed changed:', newCompany);
}, { deep: true });

// Force refetch when modal closes
watch(isModalOpen, (open) => {
  if (!open) {
    console.log('Company modal closed, refreshing data');
    companyStore.fetchCompanyProfile();
  }
});
</script> 