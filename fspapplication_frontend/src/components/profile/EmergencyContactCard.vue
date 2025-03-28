<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90 lg:mb-6">Emergency Contact</h4>
          
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-7 2xl:gap-x-32">
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Contact Name</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ (user.profile?.emergencyContactFirstName && user.profile?.emergencyContactLastName) 
                   ? `${user.profile.emergencyContactFirstName} ${user.profile.emergencyContactLastName}` 
                   : 'Not set' }}
              </p>
            </div>

            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Contact Phone</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ user.profile?.emergencyContact || 'Not set' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = authStore.user
</script>

<style></style> 