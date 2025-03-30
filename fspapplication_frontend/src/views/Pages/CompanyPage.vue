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
      <!-- Future company information cards can be added here -->
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import { useCompanyStore } from "@/stores/companyStore";
import { Company } from "@/service/companyService";

const currentPageTitle = ref("Company Settings");
const companyStore = useCompanyStore();
const loading = computed(() => companyStore.loading);
const error = computed(() => companyStore.error);
const company = computed<Company | null>(() => companyStore.company);

onMounted(async () => {
  await companyStore.fetchCompany();
});
</script>

<style></style>
