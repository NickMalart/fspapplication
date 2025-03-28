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
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Change Avatar</h3>
          <button 
            @click="close" 
            class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="flex flex-col items-center">
          <div 
            class="w-40 h-40 mb-6 overflow-hidden border-4 border-gray-200 rounded-full dark:border-gray-700 relative group"
          >
            <img 
              :src="avatarPreview || currentAvatar" 
              alt="User Avatar" 
              class="w-full h-full object-cover"
            />
            <input 
              type="file" 
              ref="avatarInput" 
              @change="handleAvatarUpload" 
              accept="image/*" 
              class="hidden"
            />
            <button 
              @click="triggerAvatarUpload"
              class="absolute inset-0 bg-black/50 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>

          <p class="text-sm text-gray-500 dark:text-gray-400 mb-6 text-center">
            Click on the avatar to upload a new profile picture
          </p>

          <div class="flex justify-end space-x-2 w-full">
            <button 
              type="button" 
              @click="close" 
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
            >
              Cancel
            </button>
            <button 
              type="button" 
              @click="saveAvatar"
              :disabled="!avatarFile"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Save Avatar
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
const avatarInput = ref<HTMLInputElement | null>(null)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const loading = ref(false)

const currentAvatar = computed(() => {
  const user = authStore.user
  const avatarUrl = (user as any).avatar // Use type assertion to bypass linter
  return avatarUrl || 
    `https://ui-avatars.com/api/?name=${user.firstName}+${user.lastName}&background=0D8ABC&color=fff&size=200`
})

function triggerAvatarUpload() {
  avatarInput.value?.click()
}

function handleAvatarUpload(event: Event) {
  const input = event.target as HTMLInputElement
  if (input?.files && input.files[0]) {
    avatarFile.value = input.files[0]
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      const result = e.target?.result
      if (typeof result === 'string') {
        avatarPreview.value = result
      }
    }
    reader.readAsDataURL(input.files[0])
  }
}

async function saveAvatar() {
  if (!avatarFile.value) return

  try {
    loading.value = true
    
    // Prepare form data for upload
    const formData = new FormData()
    formData.append('avatar', avatarFile.value)

    const response = await axios.patch('/api/account/user/update/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Update auth store
    authStore.updateUser(response.data)

    // Reset and close
    avatarFile.value = null
    avatarPreview.value = null
    close()
  } catch (error) {
    console.error('Avatar upload failed:', error)
  } finally {
    loading.value = false
  }
}

function close() {
  // Reset state
  avatarFile.value = null
  avatarPreview.value = null
  
  emit('close')
  document.body.style.overflow = ''
}
</script> 