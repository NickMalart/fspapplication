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
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.firstName }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedUser.firstName" 
                type="text" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="First Name"
              />
            </div>

            <!-- Last Name -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Last Name</p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.lastName }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedUser.lastName" 
                type="text" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="Last Name"
              />
            </div>

            <!-- Email -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">
                Email address
              </p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.email }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedUser.email" 
                type="email" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="Email Address"
              />
            </div>

            <!-- Phone Number -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Phone</p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.profile?.phoneNumber || 'Not set' }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedUser.phoneNumber" 
                type="tel" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="Phone Number"
              />
            </div>

            <!-- Groups (Placeholder) -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Groups</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                **Groups Placeholder**
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  isEditMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:personalInfo'])

const authStore = useAuthStore()
const user = computed(() => authStore.user)

// Create a reactive copy of user data for editing
const editedUser = ref({
  firstName: user.value.firstName,
  lastName: user.value.lastName,
  email: user.value.email,
  phoneNumber: user.value.profile?.phoneNumber || ''
})

// Watch for changes in edit mode
watch(() => props.isEditMode, (newEditMode) => {
  if (newEditMode) {
    // Reset edited user to current user data when entering edit mode
    editedUser.value = {
      firstName: user.value.firstName,
      lastName: user.value.lastName,
      email: user.value.email,
      phoneNumber: user.value.profile?.phoneNumber || ''
    }
  } else {
    // When exiting edit mode, emit changes
    const changedFields = {}
    
    if (editedUser.value.firstName !== user.value.firstName) {
      changedFields.firstName = editedUser.value.firstName
    }
    
    if (editedUser.value.lastName !== user.value.lastName) {
      changedFields.lastName = editedUser.value.lastName
    }
    
    if (editedUser.value.email !== user.value.email) {
      changedFields.email = editedUser.value.email
    }
    
    if (editedUser.value.phoneNumber !== (user.value.profile?.phoneNumber || '')) {
      changedFields.profile = {
        phoneNumber: editedUser.value.phoneNumber
      }
    }

    // Only emit if there are changes
    if (Object.keys(changedFields).length > 0) {
      emit('update:personalInfo', changedFields)
    }
  }
}, { immediate: false })
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
