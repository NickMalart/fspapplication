<template>
  <div>
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90 lg:mb-6">Business Details</h4>
          
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-7 2xl:gap-x-32">
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Phone</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.phone || 'Not set' }}</p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Email</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.email || 'Not set' }}</p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Website</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                <a v-if="company.website" :href="company.website" target="_blank" class="text-blue-500 hover:underline">
                  {{ company.website }}
                </a>
                <span v-else>Not set</span>
              </p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Tax Number</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.tax_number || 'Not set' }}</p>
            </div>
            
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Business Registration Number</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.abn_number || 'Not set' }}</p>
            </div>
            
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Established Date</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ company.established_date ? formatDate(company.established_date) : 'Not set' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCompanyStore } from '@/stores/company'

const companyStore = useCompanyStore()
const company = computed(() => companyStore.company || {
  phone: '',
  email: '',
  website: '',
  tax_number: '',
  abn_number: '',
  established_date: ''
})

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString()
}
</script> 