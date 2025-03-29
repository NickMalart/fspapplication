<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90">
              Personal Information
            </h4>
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
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
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
