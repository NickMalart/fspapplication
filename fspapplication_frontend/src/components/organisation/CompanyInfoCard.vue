<template>
  <div>
    <div class="p-5 mb-6 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
        <div class="flex flex-col items-center w-full gap-6 xl:flex-row">
          <div
            class="w-20 h-20 overflow-hidden border border-gray-200 rounded-full dark:border-gray-800"
          >
            <img v-if="company.logo" :src="company.logo" alt="company logo" />
            <img v-else :src="`https://ui-avatars.com/api/?name=${company.name}&background=0D8ABC&color=fff&size=100`" alt="company" />
          </div>
          <div class="order-3 xl:order-2">
            <h4
              class="mb-2 text-lg font-semibold text-center text-gray-800 dark:text-white/90 xl:text-left"
            >
              {{ company.name }}
            </h4>
            <div
              class="flex flex-col items-center gap-1 text-center xl:flex-row xl:gap-3 xl:text-left"
            >
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ company.email }}</p>
              <div class="hidden h-3.5 w-px bg-gray-300 dark:bg-gray-700 xl:block"></div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ company.phone || 'No phone' }}</p>
              <div class="hidden h-3.5 w-px bg-gray-300 dark:bg-gray-700 xl:block"></div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ getFullAddress() }}</p>
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
  name: '',
  email: '',
  phone: '',
  unit: '',
  number: '',
  street: ''
})

const getFullAddress = (): string => {
  if (!company.value) return 'No address'
  
  const parts: string[] = []
  if (company.value.unit) parts.push(company.value.unit)
  if (company.value.number) parts.push(company.value.number)
  if (company.value.street) parts.push(company.value.street)
  
  return parts.length > 0 ? parts.join(' ') : 'No address'
}
</script> 