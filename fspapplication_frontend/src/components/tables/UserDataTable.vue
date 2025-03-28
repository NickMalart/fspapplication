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
                <th @click="sortBy('employeeDetails.jobTitle')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Job Title
                  <span v-if="sortColumn === 'employeeDetails.jobTitle'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('employeeDetails.department')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Department
                  <span v-if="sortColumn === 'employeeDetails.department'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('is_active')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Status
                  <span v-if="sortColumn === 'is_active'">
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
                    :src="user.avatar || `https://ui-avatars.com/api/?name=${user.firstName}+${user.lastName}&background=0D8ABC&color=fff&size=100`" 
                    :alt="`${user.fullName}'s avatar`"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white/90">
                    {{ user.fullName }}
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    {{ user.userType }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ user.employeeDetails?.jobTitle || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ user.employeeDetails?.department || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                      user.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ user.is_active ? 'Active' : 'Inactive' }}
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
import axios from 'axios'
import debounce from 'lodash/debounce'
import { useRouter } from 'vue-router'

const router = useRouter()
// Reactive state
const users = ref([])
const search = ref('')
const sortColumn = ref('firstName')
const sortDirection = ref('asc')
const currentPage = ref(1)
const perPage = ref(10)
const pageOptions = [5, 10, 25, 50]
const statusFilter = ref('active') // Default to active users

// Debounced search to prevent excessive API calls
const debouncedSearch = debounce(() => {
  currentPage.value = 1
  fetchUsers()
}, 500) // 500ms delay

// Fetch users with improved search and filtering
const fetchUsers = async () => {
  try {
    const response = await axios.get('/api/account/users/', {
      params: {
        search: search.value, // Full-text search
        status: statusFilter.value, // Status filter
        ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
        page: currentPage.value,
        page_size: perPage.value
      }
    })
    
    // Robust handling of different possible response structures
    const data = response.data
    users.value = data.results || data.data || data || []
    
    // Carefully set totalUsers with fallback
    totalUsers.value = data.count || data.total || data.length || 0
    
    // Set total pages with fallback
    totalPages.value = data.total_pages || Math.ceil(totalUsers.value / perPage.value) || 1
    
    // Ensure currentPage doesn't exceed total pages
    if (currentPage.value > totalPages.value) {
      currentPage.value = 1
    }
  } catch (error) {
    console.error('Error fetching users:', error)
    users.value = []
    totalUsers.value = 0
    totalPages.value = 1
    currentPage.value = 1
  }
}

// Computed properties
const filteredUsers = computed(() => {
  return users.value
})

const paginatedUsers = computed(() => {
  return filteredUsers.value
})

const totalUsers = ref(0)
const totalPages = ref(0)

const startIndex = computed(() => {
  if (totalUsers.value === 0) return 0
  return (currentPage.value - 1) * perPage.value + 1
})

const endIndex = computed(() => {
  if (totalUsers.value === 0) return 0
  return Math.min(currentPage.value * perPage.value, totalUsers.value)
})

const pageNumbers = computed(() => {
  if (totalPages.value === 0) return []
  
  const range = 2
  let pages = []
  for (
    let i = Math.max(1, currentPage.value - range);
    i <= Math.min(totalPages.value, currentPage.value + range);
    i++
  ) {
    pages.push(i)
  }
  return pages
})

// Methods
const sortBy = (column) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
  fetchUsers()
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchUsers()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchUsers()
  }
}

const goToPage = (page) => {
  currentPage.value = page
  fetchUsers()
}

const viewUserDetails = (user) => {
  router.push(`/user-profile-admin/${user.id}`)
}

// Method to set status filter
const setStatusFilter = (status) => {
  statusFilter.value = status
  currentPage.value = 1 // Reset to first page
  fetchUsers()
}

// Enhanced search method
const performSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

// Add to template
const searchInput = ref(null)

// Watchers
watch(search, (newSearch) => {
  debouncedSearch()
})

watch(perPage, () => {
  currentPage.value = 1
  fetchUsers()
})

watch(statusFilter, () => {
  fetchUsers()
})

// Initial fetch
onMounted(fetchUsers)
</script> 