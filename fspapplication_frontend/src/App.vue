<template>
  <ThemeProvider>
    <SidebarProvider>
      <RouterView />
    </SidebarProvider>
  </ThemeProvider>
</template>

<script setup lang="ts">
import ThemeProvider from './components/layout/ThemeProvider.vue'
import SidebarProvider from './components/layout/SidebarProvider.vue'
import { onMounted, watch } from 'vue';
import { usecompanyStore } from '@/stores/companyStore';
import { fileService } from '@/service/fileService';

const companyStore = usecompanyStore();

// Function to update favicon and title
const updateFaviconAndTitle = () => {
  const company = companyStore.companyProfile;
  if (company) {
    // Update page title
    document.title = company.name || 'FSP Application';
    
    // Update favicon if company has a logo
    if (company.logo) {
      const logoUrl = fileService.getCloudFrontUrl(company.logo);
      const favicon = document.getElementById('favicon') as HTMLLinkElement;
      if (favicon) {
        favicon.href = logoUrl;
      }
    }
  }
};

// Fetch company data and update favicon/title when mounted
onMounted(async () => {
  if (!companyStore.companyProfile) {
    await companyStore.fetchCompanyProfile();
  }
  updateFaviconAndTitle();
});

// Watch for changes to company profile
watch(() => companyStore.companyProfile, updateFaviconAndTitle);
</script>
