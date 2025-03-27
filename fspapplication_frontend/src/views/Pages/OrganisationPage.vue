<template>
  <admin-layout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />

    <div
      class="rounded-2xl border border-gray-200 bg-white p-5 dark:border-gray-800 dark:bg-white/[0.03] lg:p-6"
    >
      <h3 class="mb-5 text-lg font-semibold text-gray-800 dark:text-white/90 lg:mb-7">Organisation</h3>
      <company-info-card v-if="!loading" />
      <company-address-card v-if="!loading" />
      <company-details-card v-if="!loading" />
      <company-branding-card v-if="!loading" />
      
      <div v-if="loading" class="flex justify-center py-10">
        <div class="animate-spin h-10 w-10 border-4 border-blue-500 rounded-full border-t-transparent"></div>
      </div>
      
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4">
        <strong class="font-bold">Error!</strong>
        <span class="block sm:inline"> {{ error }}</span>
      </div>
    </div>
  </admin-layout>
</template>

<script setup lang="ts">
import AdminLayout from '../../components/layout/AdminLayout.vue'
import PageBreadcrumb from '@/components/common/PageBreadcrumb.vue'
import CompanyInfoCard from '@/components/organisation/CompanyInfoCard.vue'
import CompanyAddressCard from '@/components/organisation/CompanyAddressCard.vue'
import CompanyDetailsCard from '@/components/organisation/CompanyDetailsCard.vue'
import CompanyBrandingCard from '@/components/organisation/CompanyBrandingCard.vue'
import { ref, onMounted, computed } from 'vue'
import { useCompanyStore } from '@/stores/company'

const currentPageTitle = ref('Organisation')
const companyStore = useCompanyStore()

const loading = computed(() => companyStore.loading)
const error = computed(() => companyStore.error)

onMounted(async () => {
  await companyStore.fetchCompany()
})
</script>
