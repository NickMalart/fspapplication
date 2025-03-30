<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="loading && !isRetrying" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400">
      <p>{{ error }}</p>
      <button 
        @click="retryFetch" 
        class="mt-3 px-4 py-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-300 font-medium rounded-md hover:bg-red-200 dark:hover:bg-red-900/50 transition duration-150"
        :disabled="isRetrying"
      >
        <span v-if="isRetrying" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent mr-2 align-[-2px]"></span>
        {{ isRetrying ? 'Reconnecting...' : 'Retry Connection' }}
      </button>
      
      <!-- Show offline mode components with cached data if available -->
      <div v-if="hasOfflineData" class="mt-6">
        <div class="flex items-center mb-4">
          <div class="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
          <p class="text-sm font-medium text-yellow-600 dark:text-yellow-400">
            Showing cached data in offline mode
          </p>
        </div>
        
        <div class="space-y-6 opacity-80">
          <div class="bg-white dark:bg-boxdark rounded-lg shadow-sm p-6" v-if="companyProfile">
            <CompanyAvatarSection :company="companyProfile" />
          </div>
          
          <div class="bg-white dark:bg-boxdark rounded-lg shadow-sm p-6">
            <CompanyInformationCard />
          </div>
        </div>
      </div>
    </div>
    <div v-else class="space-y-6">
      <div class="bg-white dark:bg-boxdark rounded-lg shadow-sm p-6">
        <CompanyAvatarSection :company="companyProfile" />
      </div>
      
      <!-- Company Information Card -->
      <div class="bg-white dark:bg-boxdark rounded-lg shadow-sm p-6">
        <CompanyInformationCard />
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import CompanyAvatarSection from "@/components/company/CompanyAvatarSection.vue";
import CompanyInformationCard from "@/components/company/CompanyInformationCard.vue";
import { useCompanyProfileStore } from "@/stores/companyProfileStore";
import { CompanyProfile } from "@/service/companyProfileService";

const currentPageTitle = ref("Company Settings");
const companyProfileStore = useCompanyProfileStore();
const loading = computed(() => companyProfileStore.loading);
const error = computed(() => companyProfileStore.error);
const companyProfile = computed<CompanyProfile | null>(() => companyProfileStore.companyProfile);
const isRetrying = ref(false);

// Check if we have offline data to display
const hasOfflineData = computed(() => !!companyProfile.value);

// Retry fetching company profile data
const retryFetch = async () => {
  isRetrying.value = true;
  try {
    await companyProfileStore.fetchCompanyProfile();
  } catch (err) {
    console.error("Failed to reconnect:", err);
  } finally {
    isRetrying.value = false;
  }
};

onMounted(async () => {
  await companyProfileStore.fetchCompanyProfile();
});
</script>

<style></style>
