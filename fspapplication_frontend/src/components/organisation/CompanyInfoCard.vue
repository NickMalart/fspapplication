<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
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
        <button 
          @click="openModal" 
          class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 self-center xl:self-start"
        >
          Edit
        </button>
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
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Company Info</h3>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveInfo">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company Name</label>
            <input 
              type="text" 
              v-model="formData.name" 
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
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone</label>
            <input 
              type="text" 
              v-model="formData.phone" 
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
  name: '',
  email: '',
  phone: '',
  unit: '',
  number: '',
  street: ''
})

const loading = computed(() => companyStore.loading)
const isModalOpen = ref(false)

const formData = reactive({
  name: '',
  email: '',
  phone: ''
})

function openModal() {
  // Initialize form with current values
  formData.name = company.value.name || ''
  formData.email = company.value.email || ''
  formData.phone = company.value.phone || ''
  isModalOpen.value = true
  // Prevent body scrolling when modal is open
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  isModalOpen.value = false
  // Restore body scrolling when modal is closed
  document.body.style.overflow = ''
}

async function saveInfo() {
  const updateData = {
    name: formData.name,
    email: formData.email,
    phone: formData.phone
  }

  const success = await companyStore.updateCompany(updateData)
  if (success) {
    closeModal()
  }
}

const getFullAddress = (): string => {
  if (!company.value) return 'No address'
  
  const parts: string[] = []
  if (company.value.unit) parts.push(company.value.unit)
  if (company.value.number) parts.push(company.value.number)
  if (company.value.street) parts.push(company.value.street)
  
  return parts.length > 0 ? parts.join(' ') : 'No address'
}
</script> 