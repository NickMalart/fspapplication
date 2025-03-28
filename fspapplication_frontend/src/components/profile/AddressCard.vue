<template>
  <div>
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="w-full">
          <h4 class="text-lg font-semibold text-gray-800 dark:text-white/90 lg:mb-6">Address</h4>
          
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-7 2xl:gap-x-32">
            <!-- Country -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Country</p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.profile?.country || 'Not set' }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedAddress.country" 
                type="text" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="Country"
              />
            </div>

            <!-- City/State -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">City/State</p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ (user.profile?.city && user.profile?.state) 
                     ? `${user.profile.city}, ${user.profile.state}` 
                     : 'Not set' }}
                </p>
              </template>
              <div v-else class="flex space-x-2">
                <input 
                  v-model="editedAddress.city" 
                  type="text" 
                  class="form-input w-1/2 rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                  placeholder="City"
                />
                <input 
                  v-model="editedAddress.state" 
                  type="text" 
                  class="form-input w-1/2 rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                  placeholder="State"
                />
              </div>
            </div>

            <!-- Postal Code -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">
                Postal Code
              </p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.profile?.postalCode || 'Not set' }}
                </p>
              </template>
              <input 
                v-else 
                v-model="editedAddress.postalCode" 
                type="text" 
                class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                placeholder="Postal Code"
              />
            </div>

            <!-- Address Lines -->
            <div>
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">Address</p>
              <template v-if="!isEditMode">
                <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                  {{ user.profile?.addressLine1 || 'Not set' }}
                  <span v-if="user.profile?.addressLine2" class="block">
                    {{ user.profile.addressLine2 }}
                  </span>
                </p>
              </template>
              <div v-else class="space-y-2">
                <input 
                  v-model="editedAddress.addressLine1" 
                  type="text" 
                  class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                  placeholder="Address Line 1"
                />
                <input 
                  v-model="editedAddress.addressLine2" 
                  type="text" 
                  class="form-input w-full rounded-lg border border-gray-300 px-3 py-2 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
                  placeholder="Address Line 2 (Optional)"
                />
              </div>
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

const emit = defineEmits(['update:address'])

const authStore = useAuthStore()
const user = computed(() => authStore.user)

// Create a reactive copy of address data for editing
const editedAddress = ref({
  country: user.value.profile?.country || '',
  city: user.value.profile?.city || '',
  state: user.value.profile?.state || '',
  postalCode: user.value.profile?.postalCode || '',
  addressLine1: user.value.profile?.addressLine1 || '',
  addressLine2: user.value.profile?.addressLine2 || ''
})

// Watch for changes in edit mode
watch(() => props.isEditMode, (newEditMode) => {
  if (newEditMode) {
    // Reset edited address to current address data when entering edit mode
    editedAddress.value = {
      country: user.value.profile?.country || '',
      city: user.value.profile?.city || '',
      state: user.value.profile?.state || '',
      postalCode: user.value.profile?.postalCode || '',
      addressLine1: user.value.profile?.addressLine1 || '',
      addressLine2: user.value.profile?.addressLine2 || ''
    }
  } else {
    // When exiting edit mode, emit changes
    const changedFields = {}
    
    const addressFields = [
      'country', 'city', 'state', 'postalCode', 
      'addressLine1', 'addressLine2'
    ]

    addressFields.forEach(field => {
      const currentValue = user.value.profile?.[field] || ''
      if (editedAddress.value[field] !== currentValue) {
        changedFields[field] = editedAddress.value[field]
      }
    })

    // Only emit if there are changes
    if (Object.keys(changedFields).length > 0) {
      emit('update:address', changedFields)
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
