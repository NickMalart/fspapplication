<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
      {{ error }}
    </div>
    <div v-else class="space-y-6">
      <div class="bg-white dark:bg-boxdark rounded-lg shadow-sm p-6">
        <CompanyAvatarSection :company="companyProfile" />
        
        <!-- Additional company information sections can be added here -->
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import CompanyAvatarSection from "@/components/company/CompanyAvatarSection.vue";
import { useCompanyProfileStore } from "@/stores/companyProfileStore";
import { CompanyProfile } from "@/service/companyProfileService";

const currentPageTitle = ref("Company Settings");
const companyProfileStore = useCompanyProfileStore();
const loading = computed(() => companyProfileStore.loading);
const error = computed(() => companyProfileStore.error);
const companyProfile = computed<CompanyProfile | null>(() => companyProfileStore.companyProfile);

onMounted(async () => {
  await companyProfileStore.fetchCompanyProfile();
});
</script>

<style></style>
