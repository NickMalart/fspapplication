<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-[100000] flex items-center justify-center overflow-hidden">
      <!-- Backdrop -->
      <div 
        class="fixed inset-0 bg-gray-300 bg-opacity-70 dark:bg-black dark:bg-opacity-50" 
        @click="close"
      ></div>
      
      <!-- Modal Content -->
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl mx-4 p-6 relative">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Profile</h3>
          <button 
            @click="close" 
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveProfile">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Personal Information -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">First Name</label>
              <input 
                type="text" 
                v-model="formData.firstName" 
                class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
              />
            </div>

            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Last Name</label>
              <input 
                type="text" 
                v-model="formData.lastName" 
                class="w-full py-2 px-3 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white"
              />
            </div>

            <!-- Contact Information -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone Number</label>
              <input 
                type="tel" 
                v-model="formData.profile.phoneNumber" 
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
          </div>

          <div class="flex justify-end space-x-2 mt-6">
            <button 
              type="button" 
              @click="close" 
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
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const loading = ref(false)

const formData = reactive({
  firstName: authStore.user.firstName,
  lastName: authStore.user.lastName,
  email: authStore.user.email,
  profile: {
    phoneNumber: authStore.user.profile.phoneNumber
  }
})

function close() {
  emit('close')
  document.body.style.overflow = ''
}

async function saveProfile() {
  try {
    loading.value = true
    await authStore.updateUserProfile(formData)
    close()
  } catch (error) {
    console.error('Failed to update profile', error)
  } finally {
    loading.value = false
  }
}
</script> 