<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90">
              Personal Information
            </h4>
            <button 
              @click="showEditModal = true"
              class="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Edit
            </button>
          </div>

          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-7 2xl:gap-x-32">
            <!-- First Name -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">First Name</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.firstName }}
              </p>
            </div>

            <!-- Last Name -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Last Name</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.lastName }}
              </p>
            </div>

            <!-- Email -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">
                Email address
              </p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.email }}
              </p>
            </div>

            <!-- Phone Number -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Phone</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.profile?.phoneNumber || 'Not set' }}
              </p>
            </div>

            <!-- Groups -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Groups</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.groups?.join(', ') || 'No groups assigned' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Personal Information Modal -->
  <modal-dialog v-model="showEditModal" title="Edit Personal Information">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">First Name</label>
          <input
            type="text"
            v-model="formData.firstName"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Last Name</label>
          <input
            type="text"
            v-model="formData.lastName"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">Phone Number</label>
          <input
            type="tel"
            v-model="formData.phoneNumber"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
          />
        </div>
      </div>
      
      <div class="mt-4 flex justify-end space-x-3">
        <button
          type="button"
          @click="showEditModal = false"
          class="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-200 dark:hover:bg-gray-700"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Save Changes
        </button>
      </div>
    </form>
  </modal-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ModalDialog from '@/components/common/ModalDialog.vue'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
const showEditModal = ref(false)

const formData = ref({
  firstName: '',
  lastName: '',
  phoneNumber: ''
})

// Initialize form data when modal opens
watch(showEditModal, (newValue) => {
  if (newValue) {
    formData.value = {
      firstName: user.value.firstName,
      lastName: user.value.lastName,
      phoneNumber: user.value.profile?.phoneNumber || ''
    }
  }
})

const handleSubmit = async () => {
  try {
    await authStore.updateProfile(formData.value)
    showEditModal.value = false
  } catch (error) {
    console.error('Failed to update profile:', error)
  }
}
</script>

<style scoped>
.form-input {
  transition: all 0.3s ease;
}
.form-input:focus {
  border-color: rgb(59 130 246); /* blue-500 */
  box-shadow: 0 0 0 2px rgba(191, 219, 254, 0.5); /* ring-2 ring-blue-200 */
}
.dark .form-input:focus {
  border-color: rgb(37 99 235); /* dark:border-blue-600 */
  box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.5); /* dark:ring-blue-800 */
}
</style>
