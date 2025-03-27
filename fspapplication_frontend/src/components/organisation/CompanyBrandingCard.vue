<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90">Branding</h4>
            <button 
              @click="openModal" 
              class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit
            </button>
          </div>
          
          <div class="grid grid-cols-1 gap-y-6 gap-x-4 lg:grid-cols-2 lg:gap-y-8 lg:gap-x-7 2xl:gap-x-32">
            <div class="text-center lg:text-left">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Primary Color</p>
              <div class="flex items-center gap-2 justify-center lg:justify-start">
                <div 
                  class="w-6 h-6 rounded-full border border-gray-200 dark:border-gray-700" 
                  :style="{ backgroundColor: company.primary_color || '#3B82F6' }"
                ></div>
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.primary_color || '#3B82F6' }}</p>
              </div>
            </div>

            <div class="text-center lg:text-left">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Secondary Color</p>
              <div class="flex items-center gap-2 justify-center lg:justify-start">
                <div 
                  class="w-6 h-6 rounded-full border border-gray-200 dark:border-gray-700" 
                  :style="{ backgroundColor: company.secondary_color || '#1E40AF' }"
                ></div>
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">{{ company.secondary_color || '#1E40AF' }}</p>
              </div>
            </div>

            <div class="text-center lg:text-left">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Logo</p>
              <div v-if="company.logo" class="flex justify-center lg:justify-start">
                <img :src="company.logo" alt="Company Logo" class="max-w-[200px] w-full h-auto rounded border border-gray-200 dark:border-gray-700" />
              </div>
              <p v-else class="text-sm font-medium text-gray-800 dark:text-white/90">No logo uploaded</p>
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
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Branding</h3>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveBranding">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Primary Color</label>
            <div class="flex items-center gap-2">
              <input 
                type="color" 
                v-model="formData.primary_color" 
                class="h-10 w-10 p-0 border-0 rounded cursor-pointer"
              />
              <input 
                type="text" 
                v-model="formData.primary_color" 
                class="flex-1 py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Secondary Color</label>
            <div class="flex items-center gap-2">
              <input 
                type="color" 
                v-model="formData.secondary_color" 
                class="h-10 w-10 p-0 border-0 rounded cursor-pointer"
              />
              <input 
                type="text" 
                v-model="formData.secondary_color" 
                class="flex-1 py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
              />
            </div>
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Logo</label>
            <div class="flex items-center justify-center w-full">
              <label for="logo-upload" class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 dark:border-gray-600">
                <div v-if="previewLogo" class="flex flex-col items-center justify-center h-full">
                  <img :src="previewLogo" alt="Preview" class="max-h-28 max-w-full object-contain" />
                </div>
                <div v-else class="flex flex-col items-center justify-center">
                  <svg class="w-8 h-8 mb-1 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                  </svg>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Upload logo (SVG, PNG, JPG)</p>
                </div>
                <input id="logo-upload" type="file" class="hidden" @change="handleFileUpload" accept="image/*" />
              </label>
            </div>
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
  logo: '',
  primary_color: '#3B82F6',
  secondary_color: '#1E40AF'
})

const loading = computed(() => companyStore.loading)
const error = computed(() => companyStore.error)
const isModalOpen = ref(false)
const logoFile = ref<File | null>(null)
const previewLogo = ref<string | null>(null)

const formData = reactive({
  primary_color: '',
  secondary_color: '',
  logo: null as string | null
})

function openModal() {
  formData.primary_color = company.value.primary_color || '#3B82F6'
  formData.secondary_color = company.value.secondary_color || '#1E40AF'
  formData.logo = company.value.logo || null
  previewLogo.value = company.value.logo || null
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  isModalOpen.value = false
  logoFile.value = null
  previewLogo.value = null
  document.body.style.overflow = ''
}

function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    logoFile.value = input.files[0]
    previewLogo.value = URL.createObjectURL(input.files[0])
  }
}

async function saveBranding() {
  const updateData = {
    primary_color: formData.primary_color,
    secondary_color: formData.secondary_color
  }

  const success = await companyStore.updateCompany(updateData)
  if (success) {
    closeModal()
  }
}
</script>