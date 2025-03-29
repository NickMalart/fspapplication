<template>
  <div class="fixed inset-0 flex items-center justify-center overflow-y-auto modal z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>
    
    <div class="relative w-full max-w-lg rounded-2xl bg-white p-8 dark:bg-gray-800">
      <!-- Modal Header -->
      <div class="mb-6 flex items-center justify-between">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          Edit Personal Information
        </h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <!-- First Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
              First Name
            </label>
            <input
              type="text"
              v-model="formData.firstName"
              class="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-700 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300"
              required
            />
          </div>

          <!-- Last Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
              Last Name
            </label>
            <input
              type="text"
              v-model="formData.lastName"
              class="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-700 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300"
              required
            />
          </div>

          <!-- Phone Number -->
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
              Phone Number
            </label>
            <input
              type="tel"
              v-model="formData.phoneNumber"
              class="mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-gray-700 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="mt-6 flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('close')"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-500 dark:hover:bg-blue-600"
          >
            Save Changes
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const emit = defineEmits(['close', 'updated'])

const formData = ref({
  firstName: '',
  lastName: '',
  phoneNumber: ''
})

onMounted(() => {
  // Initialize form data with current user data
  const user = authStore.user
  formData.value = {
    firstName: user.firstName,
    lastName: user.lastName,
    phoneNumber: user.profile?.phoneNumber || ''
  }
})

const handleSubmit = async () => {
  try {
    await authStore.updateProfile(formData.value)
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Failed to update profile:', error)
  }
}
</script>

<style scoped>
.modal {
  z-index: 99999;
}
</style> 