<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90">Address</h4>
            <button 
              @click="openModal" 
              class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit
            </button>
          </div>
          
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

  <!-- Modal -->
  <Teleport to="body">
    <div v-if="isModalOpen" class="fixed inset-0 z-[100000] flex items-center justify-center overflow-hidden">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-gray-300 bg-opacity-70 dark:bg-black dark:bg-opacity-50" @click="closeModal"></div>
      
      <!-- Modal Content -->
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-md mx-4 p-6 relative">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Address</h3>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveAddress">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Country</label>
            <input 
              type="text" 
              v-model="formData.country" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">City</label>
            <input 
              type="text" 
              v-model="formData.city" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">State</label>
            <input 
              type="text" 
              v-model="formData.state" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Postal Code</label>
            <input 
              type="text" 
              v-model="formData.postal_code" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Unit</label>
            <input 
              type="text" 
              v-model="formData.unit" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Number</label>
            <input 
              type="text" 
              v-model="formData.number" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Street</label>
            <input 
              type="text" 
              v-model="formData.street" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="flex justify-end space-x-2">
            <button 
              type="button" 
              @click="closeModal" 
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="loading" 
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, reactive } from 'vue'
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

const loading = computed(() => companyStore.loading)
const isModalOpen = ref(false)

const formData = reactive({
  country: '',
  city: '',
  state: '',
  postal_code: '',
  unit: '',
  number: '',
  street: ''
})

function openModal() {
  // Initialize form with current values
  formData.country = company.value.country || ''
  formData.city = company.value.city || ''
  formData.state = company.value.state || ''
  formData.postal_code = company.value.postal_code || ''
  formData.unit = company.value.unit || ''
  formData.number = company.value.number || ''
  formData.street = company.value.street || ''
  isModalOpen.value = true
  // Prevent body scrolling when modal is open
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  isModalOpen.value = false
  // Restore body scrolling when modal is closed
  document.body.style.overflow = ''
}

async function saveAddress() {
  const updateData = {
    country: formData.country,
    city: formData.city,
    state: formData.state,
    postal_code: formData.postal_code,
    unit: formData.unit,
    number: formData.number,
    street: formData.street
  }

  const success = await companyStore.updateCompany(updateData)
  if (success) {
    closeModal()
  }
}

const getStreetAddress = (): string | null => {
  if (!company.value) return null
  
  const parts: string[] = []
  if (company.value.unit) parts.push(`Unit ${company.value.unit}`)
  if (company.value.number) parts.push(company.value.number)
  if (company.value.street) parts.push(company.value.street)
  
  return parts.length > 0 ? parts.join(' ') : null
}
</script> 