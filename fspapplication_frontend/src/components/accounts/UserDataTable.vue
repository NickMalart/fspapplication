<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <!-- Status Filter Section -->
    <div class="px-5 py-4 sm:px-6 sm:py-5 border-b border-gray-100 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90 mb-3 sm:mb-0">
          User Accounts
        </h3>
        
        <!-- Status Filter Buttons/Dropdown -->
        <div class="w-full sm:w-auto flex flex-col items-center">
          <!-- Mobile: Dropdown -->
          <div class="sm:hidden">
            <select 
              v-model="statusFilter" 
              class="form-select w-full rounded-lg border border-gray-300 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
            >
              <option value="active">Active Users</option>
              <option value="inactive">Inactive Users</option>
              <option value="all">All Users</option>
            </select>
          </div>
          
          <!-- Desktop: Button Group -->
          <div class="hidden sm:flex items-center space-x-2">
            <button 
              @click="setStatusFilter('active')"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
                statusFilter === 'active' 
                  ? 'bg-green-500 text-white' 
                  : 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400 hover:bg-green-200 dark:hover:bg-green-900/70'
              ]"
            >
              Active Users
            </button>
            <button 
              @click="setStatusFilter('inactive')"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
                statusFilter === 'inactive' 
                  ? 'bg-red-500 text-white' 
                  : 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/70'
              ]"
            >
              Inactive Users
            </button>
            <button 
              @click="setStatusFilter('all')"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200',
                statusFilter === 'all' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/70'
              ]"
            >
              All Users
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-100 p-5 dark:border-gray-800 sm:p-6">
      <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-800/50 pt-4">
        <!-- Controls: Show Entries & Search -->
        <div class="mb-4 flex flex-col gap-2 px-4 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-3">
            <span class="text-gray-500 dark:text-gray-400">Show</span>
            <select 
              v-model="perPage" 
              class="form-select rounded-lg border border-gray-300 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
            >
              <option v-for="option in pageOptions" :key="option" :value="option" class="dark:bg-gray-800 dark:text-white/90">
                {{ option }}
              </option>
            </select>
            <span class="text-gray-500 dark:text-gray-400">entries</span>
          </div>

          <!-- Search input with clear text -->
          <div class="relative flex items-center w-full sm:w-64 md:w-80 lg:w-96 xl:w-[400px]">
            <input 
              ref="searchInput"
              v-model="search" 
              type="text" 
              placeholder="Search users..." 
              class="pl-3 pr-10 py-2 form-input rounded-lg border border-gray-300 w-full dark:bg-gray-700 dark:border-gray-600 dark:text-white/90 dark:placeholder-gray-400 transition-all duration-300 ease-in-out"
            />
            <button 
              v-if="search" 
              @click="search = ''" 
              class="absolute right-2 text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 cursor-pointer text-sm"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- User Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th @click="sortBy('avatar')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer w-24">
                  Avatar
                  <span v-if="sortColumn === 'avatar'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('firstName')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Name
                  <span v-if="sortColumn === 'firstName'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('email')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Email
                  <span v-if="sortColumn === 'email'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('employeeProfile.jobTitle')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Job Title
                  <span v-if="sortColumn === 'employeeProfile.jobTitle'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('employeeProfile.department')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Department
                  <span v-if="sortColumn === 'employeeProfile.department'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('isActive')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Status
                  <span v-if="sortColumn === 'isActive'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  User Profile
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="paginatedUsers.length === 0" class="text-center">
                <td colspan="7" class="px-6 py-4 text-gray-500 dark:text-gray-400">
                  No users found
                </td>
              </tr>
              <tr v-else v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                <td class="px-6 py-4 whitespace-nowrap w-24">
                  <img 
                    class="h-10 w-10 rounded-full object-cover mx-auto" 
                    :src="getCachedAvatarUrl(user)" 
                    :alt="`${user.firstName} ${user.lastName}'s avatar`"
                    @error="handleAvatarError($event, user)"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white/90">
                    {{ user.firstName }} {{ user.lastName }}
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    {{ user.userType }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ getUserJobTitle(user) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ getUserDepartment(user) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                      user.isActive 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ user.isActive ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button 
                    @click="viewUserDetails(user)" 
                    class="inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-lg text-blue-600 hover:text-blue-700 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/50 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    View Profile
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="bg-white dark:bg-gray-900 px-4 py-3 border-t border-gray-200 dark:border-gray-700 sm:px-6">
          <div class="flex flex-col items-center">
            <div class="text-sm text-gray-700 dark:text-gray-300 mb-2">
              {{ totalUsers === 0 
                ? 'Showing 0 to 0 of 0 entries' 
                : `Showing ${startIndex} to ${endIndex} of ${totalUsers} entries` 
              }}
            </div>
            
            <div class="flex items-center space-x-2">
              <button 
                @click="prevPage" 
                :disabled="currentPage === 1"
                class="p-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 dark:text-white/90"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="dark:stroke-white/90">
                  <path d="M15 18l-6-6 6-6"/>
                </svg>
              </button>
              
              <div class="flex items-center space-x-1">
                <button 
                  v-for="page in pageNumbers" 
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    'w-10 h-10 rounded-lg text-sm font-medium',
                    currentPage === page 
                      ? 'bg-blue-50 text-blue-600 border border-blue-300 dark:bg-blue-900/50 dark:text-blue-400 dark:border-blue-800' 
                      : 'text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                  ]"
                >
                  {{ page }}
                </button>
              </div>
              
              <button 
                @click="nextPage" 
                :disabled="currentPage === totalPages"
                class="p-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 dark:text-white/90"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="dark:stroke-white/90">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import debounce from 'lodash/debounce'
import { useRouter } from 'vue-router'
import { useUserAccountsStore } from '@/stores/userAccountsStore'
import { fileService } from '@/service/fileService'

const router = useRouter()
const userAccountsStore = useUserAccountsStore()

// Reactive state
const search = ref('')
const statusFilter = ref('active') // Default to active users
const pageOptions = [5, 10, 25, 50]

// Use values from the store with computed properties for reactivity
const users = computed(() => userAccountsStore.users)
const currentPage = computed({
  get: () => userAccountsStore.currentPage,
  set: (value) => userAccountsStore.currentPage = value
})
const perPage = computed({
  get: () => userAccountsStore.perPage,
  set: (value) => userAccountsStore.setPerPage(value)
})
const totalUsers = computed(() => userAccountsStore.totalUsers)
const totalPages = computed(() => userAccountsStore.totalPages)
const sortColumn = computed(() => userAccountsStore.sortColumn)
const sortDirection = computed(() => userAccountsStore.sortDirection)
const startIndex = computed(() => userAccountsStore.startIndex)
const endIndex = computed(() => userAccountsStore.endIndex)
const pageNumbers = computed(() => userAccountsStore.pageNumbers)
const loading = computed(() => userAccountsStore.loading)

// Computed properties
const paginatedUsers = computed(() => users.value)

// Cache for locally generated avatars and loaded custom avatars
const avatarCache = ref(new Map())

// Preload custom avatars in the background
const preloadCustomAvatars = (usersWithAvatars) => {
  if (!usersWithAvatars || usersWithAvatars.length === 0) return
  
  // Use a single image element for sequential loading to avoid flooding the network
  const preloadImage = new Image()
  let currentIndex = 0
  
  const loadNextAvatar = () => {
    if (currentIndex >= usersWithAvatars.length) return
    
    const user = usersWithAvatars[currentIndex]
    const avatarPath = user.avatar
    
    // Generate a cache key for this avatar
    const cacheKey = `custom-${user.id}`
    
    // Skip if already cached
    if (avatarCache.value.has(cacheKey)) {
      currentIndex++
      loadNextAvatar()
      return
    }
    
    // Get proper URL
    let avatarUrl
    if (avatarPath.startsWith('https://d1elaz1f509qmb.cloudfront.net/')) {
      avatarUrl = avatarPath
    } else {
      avatarUrl = fileService.getCloudFrontUrl(avatarPath)
    }
    
    // Initialize with the URL even before loading completes
    avatarCache.value.set(cacheKey, avatarUrl)
    
    // Move to next image once this one loads or errors
    preloadImage.onload = preloadImage.onerror = () => {
      currentIndex++
      if (currentIndex < usersWithAvatars.length) {
        loadNextAvatar()
      }
    }
    
    // Start loading
    preloadImage.src = avatarUrl
  }
  
  // Begin loading process
  loadNextAvatar()
}

// Get properly formatted avatar URL with improved caching
const getAvatarUrl = (user) => {
  if (!user.avatar) {
    // Use local SVG generation for default avatars
    return generateAvatarSvg(user.firstName, user.lastName)
  }
  
  // For custom avatars, check if we've already processed this one
  const cacheKey = `custom-${user.id}`
  if (avatarCache.value.has(cacheKey)) {
    return avatarCache.value.get(cacheKey)
  }
  
  // Otherwise process and cache it
  const avatarPath = user.avatar
  let avatarUrl
  
  // If it's already a CloudFront URL, use it as-is
  if (avatarPath.startsWith('https://d1elaz1f509qmb.cloudfront.net/')) {
    avatarUrl = avatarPath
  } else {
    // Otherwise, construct the CloudFront URL
    avatarUrl = fileService.getCloudFrontUrl(avatarPath)
  }
  
  // Cache for future use
  avatarCache.value.set(cacheKey, avatarUrl)
  return avatarUrl
}

// Generate inline SVG avatar
const generateAvatarSvg = (firstName = '', lastName = '') => {
  const cacheKey = `${firstName}-${lastName}`
  
  // Check cache first
  if (avatarCache.value.has(cacheKey)) {
    return avatarCache.value.get(cacheKey)
  }
  
  // Generate a color based on the name (consistent for same name)
  const getInitialsColor = (name) => {
    const colors = [
      '#1E88E5', '#43A047', '#E53935', '#5E35B1', '#FB8C00', 
      '#00897B', '#3949AB', '#8E24AA', '#D81B60', '#039BE5'
    ]
    
    // Simple hash function for name
    let hash = 0
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash)
    }
    
    // Use hash to pick a color
    return colors[Math.abs(hash) % colors.length]
  }
  
  // Get initials (maximum 2 characters)
  const firstInitial = firstName ? firstName.charAt(0).toUpperCase() : ''
  const lastInitial = lastName ? lastName.charAt(0).toUpperCase() : ''
  const initials = firstInitial + lastInitial
  const bgColor = getInitialsColor(`${firstName}${lastName}`)
  
  // Generate SVG with proper XML escaping 
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
    <rect width="100%" height="100%" fill="${bgColor}"/>
    <text x="50" y="55" font-size="35" text-anchor="middle" fill="white" font-family="Arial, sans-serif" dominant-baseline="middle">${initials}</text>
  </svg>`
  
  // Convert to data URL
  const svgUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
  
  // Store in cache
  avatarCache.value.set(cacheKey, svgUrl)
  
  return svgUrl
}

// Get cached avatar URL - now simplified to just use local SVGs for default avatars
const getCachedAvatarUrl = (user) => {
  // If user has a custom avatar, use it
  if (user.avatar) {
    return getAvatarUrl(user)
  }
  
  // Otherwise, use our locally generated SVG
  return generateAvatarSvg(user.firstName, user.lastName)
}

// Debounced search to prevent excessive API calls
const debouncedSearch = debounce(() => {
  userAccountsStore.setSearch(search.value)
}, 500) // 500ms delay

// Methods
const sortBy = (column) => {
  userAccountsStore.setSorting(column)
}

const prevPage = () => {
  userAccountsStore.prevPage()
}

const nextPage = () => {
  userAccountsStore.nextPage()
}

const goToPage = (page) => {
  userAccountsStore.goToPage(page)
}

const viewUserDetails = (user) => {
  router.push(`/user-profile-admin/${user.id}`)
}

// Method to set status filter
const setStatusFilter = (status) => {
  statusFilter.value = status
  userAccountsStore.setStatusFilter(status)
}

// Enhanced search method
const performSearch = () => {
  userAccountsStore.setSearch(search.value)
}

// Add to template
const searchInput = ref(null)

// Handle avatar image loading errors
const handleAvatarError = (event, user) => {
  // Fall back to locally generated SVG avatar
  event.target.src = generateAvatarSvg(user.firstName, user.lastName)
}

// Watchers
watch(search, (newSearch) => {
  debouncedSearch()
})

watch(perPage, () => {
  userAccountsStore.setPerPage(perPage.value)
})

watch(statusFilter, () => {
  userAccountsStore.setStatusFilter(statusFilter.value)
})

watch(users, (newUsers) => {
  if (!newUsers || newUsers.length === 0) return
  
  // Split users into those with and without custom avatars
  const usersWithCustomAvatars = newUsers.filter(user => user.avatar)
  
  // Only preload if there are custom avatars
  if (usersWithCustomAvatars.length > 0) {
    preloadCustomAvatars(usersWithCustomAvatars)
  }
}, { immediate: true })

// Helper methods for user profile data
const getUserJobTitle = (user) => {
  if (user.userType === 'employee' && user.employeeProfile) {
    return user.employeeProfile.jobTitle || 'N/A'
  }
  return 'N/A'
}

const getUserDepartment = (user) => {
  if (user.userType === 'employee' && user.employeeProfile) {
    return user.employeeProfile.department || 'N/A'
  }
  return 'N/A'
}

// Initial fetch
onMounted(() => {
  userAccountsStore.fetchUsers()
})
</script> 