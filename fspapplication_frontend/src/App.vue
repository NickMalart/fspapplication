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
import { useAuthStore } from '@/stores/auth';

const companyStore = usecompanyStore();
const authStore = useAuthStore();

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

// Fetch company data and update favicon/title when mounted, but only if user is authenticated
onMounted(async () => {
  if (authStore.isAuthenticated && !companyStore.companyProfile) {
    await companyStore.fetchCompanyProfile();
    updateFaviconAndTitle();
  }
});

// Watch for changes to company profile
watch(() => companyStore.companyProfile, updateFaviconAndTitle);

// Also watch for authentication state changes
watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
  if (isAuthenticated && !companyStore.companyProfile) {
    await companyStore.fetchCompanyProfile();
    updateFaviconAndTitle();
  }
});
</script>
