<template>
  <div>
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90 lg:mb-6">Address</h4>
          
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-7 2xl:gap-x-32">
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Country</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.country || 'Not set' }}</p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">City/State</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ (company.city && company.state) ? `${company.city}, ${company.state}` : 'Not set' }}
              </p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">
                Postal Code
              </p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.postal_code || 'Not set' }}</p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Address</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ getStreetAddress() || 'Not set' }}
              </p>
            </div>
            
            <div v-if="company.latitude && company.longitude">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Coordinates</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ company.latitude }}, {{ company.longitude }}
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
  country: '',
  city: '',
  state: '',
  postal_code: '',
  unit: '',
  number: '',
  street: '',
  latitude: null,
  longitude: null
})

const getStreetAddress = (): string | null => {
  if (!company.value) return null
  
  const parts: string[] = []
  if (company.value.unit) parts.push(`Unit ${company.value.unit}`)
  if (company.value.number) parts.push(company.value.number)
  if (company.value.street) parts.push(company.value.street)
  
  return parts.length > 0 ? parts.join(' ') : null
}
</script> 