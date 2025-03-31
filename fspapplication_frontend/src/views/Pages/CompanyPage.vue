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
      <CompanyAvatarSection :company="companyProfile" />
      <CompanyInformationCard />
      <CompanyAddressCard />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import CompanyAvatarSection from "@/components/administration/company/CompanyAvatarSection.vue";
import CompanyInformationCard from "@/components/administration/company/CompanyInformationCard.vue";
import CompanyAddressCard from "@/components/administration/company/CompanyAddressCard.vue";
import { usecompanyStore } from "@/stores/companyStore";
import { CompanyProfile } from "@/service/companyService";

const currentPageTitle = ref("Company Settings");
const companyStore = usecompanyStore();
const loading = computed(() => companyStore.loading);
const error = computed(() => companyStore.error);
const companyProfile = computed<CompanyProfile | null>(() => companyStore.companyProfile);

onMounted(async () => {
  await companyStore.fetchCompanyProfile();
});
</script>

<style></style>
