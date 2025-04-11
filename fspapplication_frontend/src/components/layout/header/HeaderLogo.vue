<template>
  <router-link to="/" class="lg:hidden flex items-center">
    <img 
      v-if="companyLogoUrl" 
      :src="companyLogoUrl" 
      alt="Company Logo" 
      class="h-8 mr-2"
    />
    <img 
      v-else
      src="/images/logo/default-company-logo.png" 
      alt="Default Company Logo" 
      class="h-8 mr-2"
    />
    <span class="font-semibold text-gray-800 dark:text-white">{{ companyName }}</span>
  </router-link>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue';
import { usecompanyStore } from '@/stores/companyStore';
import { fileService } from '@/service/fileService';

const companyStore = usecompanyStore();

// Computed property for the logo URL
const logoUrl = computed(() => {
  // Use the tenant-specific logo if available, otherwise fallback to default
  if (companyStore.companyProfile?.logo) {
    // Use the file service to get the correct URL
    return fileService.getPublicFileUrl(companyStore.companyProfile.logo);
  } else {
    // Provide a fallback path to a default logo in the public directory
    return '/images/logo/default-company-logo.png';
  }
});

// Get company name
const companyName = computed(() => {
  return companyStore.companyProfile?.name || 'Company Name';
});
</script>
