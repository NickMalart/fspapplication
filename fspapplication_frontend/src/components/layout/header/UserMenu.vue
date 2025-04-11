<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="flex items-center text-gray-700 dark:text-gray-400"
      @click.prevent="toggleDropdown"
    >
      <span class="mr-3 overflow-hidden rounded-full h-11 w-11">
        <img 
          v-if="avatarUrl"
          :src="avatarUrl"
          :alt="`${completeUser?.firstName || ''} ${completeUser?.lastName || ''}`" 
          class="h-full w-full object-cover"
          referrerpolicy="no-referrer"
        />
        <img 
          v-else
          :src="`https://ui-avatars.com/api/?name=${completeUser?.firstName || ''}+${completeUser?.lastName || ''}&background=0D8ABC&color=fff`" 
          alt="User" 
        />
      </span>

      <span class="block mr-1 font-medium text-theme-sm">{{ completeUser?.firstName || '' }} {{ completeUser?.lastName || '' }} </span>

      <ChevronDownIcon :class="{ 'rotate-180': dropdownOpen }" />
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute right-0 mt-[17px] flex w-[260px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark"
    >
      <div>
        <span class="block font-medium text-gray-700 text-theme-sm dark:text-gray-400">
          <span class="font-semibold">{{ completeUser?.firstName || '' }} {{ completeUser?.lastName || '' }}</span>
        </span>
        <span class="mt-0.5 block text-theme-xs text-gray-500 dark:text-gray-400">
          {{ completeUser?.email || auth.user.email }}
        </span>
      </div>

      <ul class="flex flex-col gap-1 pt-4 pb-3 border-b border-gray-200 dark:border-gray-800">
        <li v-for="item in menuItems" :key="item.href">
          <router-link
            :to="item.href"
            class="flex items-center gap-3 px-3 py-2 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
          >
            <!-- SVG icon would go here -->
            <component
              :is="item.icon"
              class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
            />
            {{ item.text }}
          </router-link>
        </li>
      </ul>
      <router-link
        to="/"
        @click="signOut"
        class="flex items-center gap-3 px-3 py-2 mt-3 font-medium text-gray-700 rounded-lg group text-theme-sm hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-white/5 dark:hover:text-gray-300"
      >
        <LogoutIcon
          class="text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-300"
        />
        Sign out
      </router-link>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup>
import { UserCircleIcon, ChevronDownIcon, LogoutIcon, SettingsIcon, InfoCircleIcon } from '@/icons'
import { RouterLink } from 'vue-router'
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/userProfileStore'
import { storeToRefs } from 'pinia'
import { fileService } from '@/service/fileService'

const dropdownOpen = ref(false)
const dropdownRef = ref(null)
const auth = useAuthStore()
const userStore = useUserStore()
const { completeUser } = storeToRefs(userStore)

// Computed property to get the avatar URL
const avatarUrl = computed(() => {
  const avatarPath = userStore.user?.profile?.avatar;
  if (!avatarPath) {
    // Use a default avatar if none is set
    return '/images/user/user-avatar.png';
  }
  // Get the public URL using the file service
  return fileService.getPublicFileUrl(avatarPath);
});

const menuItems = [
  { href: '/profile', icon: UserCircleIcon, text: 'Edit profile' },
  { href: '/chat', icon: SettingsIcon, text: 'Account settings' },
  { href: '/profile', icon: InfoCircleIcon, text: 'Support' },
]

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const signOut = () => {
  // Implement sign out logic here
  console.log('Signing out...')
  auth.removeToken()
  closeDropdown()
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (!completeUser.value) {
    userStore.fetchUserProfile()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
