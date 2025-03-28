<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-[100000] flex items-center justify-center overflow-hidden">
      <!-- Backdrop -->
      <div 
        class="fixed inset-0 bg-gray-300 bg-opacity-70 dark:bg-black dark:bg-opacity-50" 
        @click="close"
      ></div>
      
      <!-- Modal Content -->
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-md mx-4 p-6 relative">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Edit Personal Information</h3>
          <button 
            @click="close" 
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <!-- First Name (Read-only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              First Name
            </label>
            <input 
              type="text" 
              :value="user.firstName"
              disabled
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700/50 dark:border-gray-600 dark:text-gray-400"
            />
          </div>

          <!-- Last Name (Read-only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Last Name
            </label>
            <input 
              type="text" 
              :value="user.lastName"
              disabled
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700/50 dark:border-gray-600 dark:text-gray-400"
            />
          </div>

          <!-- Email (Read-only) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email
            </label>
            <input 
              type="email" 
              :value="user.email"
              disabled
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700/50 dark:border-gray-600 dark:text-gray-400"
            />
          </div>

          <!-- Phone Number (Editable) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Phone Number
            </label>
            <input 
              v-model="editedPhone"
              type="tel" 
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:border-blue-600 dark:focus:ring-blue-800/50"
              placeholder="Enter phone number"
            />
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
              type="button" 
              @click="saveChanges"
              :disabled="!hasChanges"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])
const authStore = useAuthStore()
const user = computed(() => authStore.user)

const editedPhone = ref(user.value.profile?.phoneNumber || '')
const loading = ref(false)

const hasChanges = computed(() => {
  return editedPhone.value !== (user.value.profile?.phoneNumber || '')
})

async function saveChanges() {
  if (!hasChanges.value) return

  try {
    loading.value = true
    const response = await axios.patch('/api/account/user/update/', {
      profile: {
        phone_number: editedPhone.value
      }
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Update auth store
    authStore.updateUser(response.data)
    close()
  } catch (error) {
    console.error('Failed to update phone number:', error)
  } finally {
    loading.value = false
  }
}

function close() {
  // Reset state
  editedPhone.value = user.value.profile?.phoneNumber || ''
  emit('close')
}
</script> 