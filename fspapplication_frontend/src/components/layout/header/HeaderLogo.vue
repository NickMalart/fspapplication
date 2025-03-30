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

// Get the company logo URL or null if not available
const companyLogoUrl = computed(() => {
  if (!companyStore.companyProfile?.logo) return null;
  return fileService.getCloudFrontUrl(companyStore.companyProfile.logo);
});

// Get company name
const companyName = computed(() => {
  return companyStore.companyProfile?.name || 'Company Name';
});
</script>
