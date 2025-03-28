<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90">Business Details</h4>
            <button 
              @click="openModal" 
              class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit
            </button>
          </div>
          
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

  <!-- Modal -->
  <Teleport to="body">
    <div v-if="isModalOpen" class="fixed inset-0 z-[100000] flex items-center justify-center overflow-hidden">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-gray-300 bg-opacity-70 dark:bg-black dark:bg-opacity-50" @click="closeModal"></div>
      
      <!-- Modal Content -->
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-md mx-4 p-6 relative">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Business Details</h3>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveDetails">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone</label>
            <input 
              type="text" 
              v-model="formData.phone" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input 
              type="email" 
              v-model="formData.email" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Website</label>
            <div class="relative">
              <span class="absolute left-3 top-2 text-gray-400">http://</span>
              <input 
                type="text" 
                v-model="formData.website" 
                @blur="handleWebsiteBlur"
                placeholder="example.com"
                class="w-full py-2 pl-[70px] pr-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tax Number</label>
            <input 
              type="text" 
              v-model="formData.tax_number" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Business Registration Number</label>
            <input 
              type="text" 
              v-model="formData.abn_number" 
              class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Established Date</label>
            <input 
              type="date" 
              v-model="formData.established_date" 
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
  phone: '',
  email: '',
  website: '',
  tax_number: '',
  abn_number: '',
  established_date: ''
})

const loading = computed(() => companyStore.loading)
const isModalOpen = ref(false)

const formData = reactive({
  phone: '',
  email: '',
  website: '',
  tax_number: '',
  abn_number: '',
  established_date: ''
})

function openModal() {
  // Initialize form with current values
  formData.phone = company.value.phone || ''
  formData.email = company.value.email || ''
  formData.website = company.value.website || ''
  formData.tax_number = company.value.tax_number || ''
  formData.abn_number = company.value.abn_number || ''
  formData.established_date = company.value.established_date || ''
  isModalOpen.value = true
  // Prevent body scrolling when modal is open
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  isModalOpen.value = false
  // Restore body scrolling when modal is closed
  document.body.style.overflow = ''
}

async function saveDetails() {
  const updateData = {
    phone: formData.phone,
    email: formData.email,
    website: formData.website,
    tax_number: formData.tax_number,
    abn_number: formData.abn_number,
    established_date: formData.established_date
  }

  const success = await companyStore.updateCompany(updateData)
  if (success) {
    closeModal()
  }
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const handleWebsiteBlur = () => {
  if (formData.website && !formData.website.startsWith('http://') && !formData.website.startsWith('https://')) {
    formData.website = 'http://' + formData.website
  }
}
</script> 