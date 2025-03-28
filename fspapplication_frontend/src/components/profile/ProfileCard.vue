<template>
  <div class="mb-6">
    <div class="p-5 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
        <div class="flex flex-col items-center w-full gap-6 xl:flex-row">
          <div
            class="w-20 h-20 overflow-hidden border border-gray-200 rounded-full dark:border-gray-800 relative group"
          >
            <img 
              :src="avatarPreview || `https://ui-avatars.com/api/?name=${user.firstName}+${user.lastName}&background=0D8ABC&color=fff&size=100`" 
              alt="user" 
              class="w-full h-full object-cover"
            />
            <input 
              v-if="isEditMode" 
              type="file" 
              ref="avatarInput" 
              @change="handleAvatarUpload" 
              accept="image/*" 
              class="hidden"
            />
            <button 
              v-if="isEditMode" 
              @click="triggerAvatarUpload"
              class="absolute inset-0 bg-black/50 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
          <div class="order-3 xl:order-2 flex-grow">
            <h4
              class="mb-2 text-lg font-semibold text-center text-gray-800 dark:text-white/90 xl:text-left"
            >
              {{ user.firstName }} {{ user.lastName }}
            </h4>
            <div
              class="flex flex-col items-center gap-1 text-center xl:flex-row xl:gap-3 xl:text-left"
            >
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">**Place Holder for Groups**</p>
              <div class="hidden h-3.5 w-px bg-gray-300 dark:bg-gray-700 xl:block"></div>
              <p class="text-sm text-gray-500 dark:text-gray-400">**Place Holder for Location**</p>
            </div>
            <div v-if="isEditMode" class="mt-2 text-center xl:text-left">
              <button 
                @click="triggerAvatarUpload"
                class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline"
              >
                Change Avatar
              </button>
            </div>
          </div>
          <div v-if="!isEditMode" class="ml-auto">
            <button 
              @click="$emit('edit')"
              class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  isEditMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:avatar', 'edit'])

const authStore = useAuthStore()
const user = authStore.user
const avatarInput = ref(null)
const avatarPreview = ref(null)

const triggerAvatarUpload = () => {
  avatarInput.value.click()
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (file) {
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)

    // Prepare form data for upload
    const formData = new FormData()
    formData.append('avatar', file)

    try {
      const response = await axios.patch(`/api/account/users/${user.id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      // Emit update to parent
      emit('update:avatar', response.data.avatar)

      // Update auth store
      authStore.updateUser(response.data)
    } catch (error) {
      console.error('Avatar upload failed:', error)
    }
  }
}
</script>
