<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <div class="px-5 py-4 sm:px-6 sm:py-5">
      <h3 class="text-base font-medium text-gray-800 dark:text-white/90">
        User Accounts
      </h3>
    </div>
    
    <div class="border-t border-gray-100 p-5 dark:border-gray-800 sm:p-6">
      <div class="overflow-hidden rounded-xl border border-gray-200 bg-white pt-4 dark:border-gray-800 dark:bg-white/[0.03]">
        <!-- Controls: Show Entries & Search -->
        <div class="mb-4 flex flex-col gap-2 px-4 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-3">
            <span class="text-gray-500 dark:text-gray-400">Show</span>
            <select 
              v-model="perPage" 
              class="form-select rounded-lg border border-gray-300 text-sm"
            >
              <option v-for="option in pageOptions" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
            <span class="text-gray-500 dark:text-gray-400">entries</span>
          </div>

          <div class="relative">
            <input 
              v-model="search" 
              type="text" 
              placeholder="Search users..." 
              class="pl-10 form-input rounded-lg border border-gray-300 w-full sm:w-64 md:w-80 lg:w-96 xl:w-[400px] transition-all duration-300 ease-in-out"
            />
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">
              <i class="fas fa-search"></i>
            </span>
          </div>
        </div>

        <!-- User Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th @click="sortBy('avatar')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer w-24">
                  Avatar
                  <span v-if="sortColumn === 'avatar'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('firstName')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                  Name
                  <span v-if="sortColumn === 'firstName'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('email')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                  Email
                  <span v-if="sortColumn === 'email'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('employeeDetails.jobTitle')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                  Job Title
                  <span v-if="sortColumn === 'employeeDetails.jobTitle'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('employeeDetails.department')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                  Department
                  <span v-if="sortColumn === 'employeeDetails.department'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('is_active')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer">
                  Status
                  <span v-if="sortColumn === 'is_active'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="user in paginatedUsers" :key="user.id">
                <td class="px-6 py-4 whitespace-nowrap w-24">
                  <img 
                    class="h-10 w-10 rounded-full object-cover mx-auto" 
                    :src="user.avatar ? user.avatar : '/default-avatar.png'" 
                    :alt="user.fullName"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    {{ user.fullName }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ user.userType }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ user.employeeDetails?.jobTitle || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
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
                    class="text-indigo-600 hover:text-indigo-900"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
          <div class="flex flex-col items-center">
            <div class="text-sm text-gray-700 mb-2">
              Showing {{ startIndex }} to {{ endIndex }} of {{ totalUsers }} entries
            </div>
            
            <div class="flex items-center space-x-2">
              <button 
                @click="prevPage" 
                :disabled="currentPage === 1"
                class="p-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                      ? 'bg-blue-50 text-blue-600 border border-blue-300' 
                      : 'text-gray-500 hover:bg-gray-100'
                  ]"
                >
                  {{ page }}
                </button>
              </div>
              
              <button 
                @click="nextPage" 
                :disabled="currentPage === totalPages"
                class="p-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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

// Reactive state
const users = ref([])
const search = ref('')
const sortColumn = ref('firstName')
const sortDirection = ref('asc')
const currentPage = ref(1)
const perPage = ref(10)
const pageOptions = [5, 10, 25, 50]

// Fetch users
const fetchUsers = async () => {
  try {
    const response = await axios.get('/api/account/users/', {
      params: {
        search: search.value,
        ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
        page: currentPage.value,
        page_size: perPage.value
      }
    })
    // Adjust based on your backend response structure
    users.value = response.data.results || response.data
    totalUsers.value = response.data.count || response.data.length
  } catch (error) {
    console.error('Error fetching users:', error)
    // Optionally set some default or error state
    users.value = []
    totalUsers.value = 0
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
const totalPages = computed(() => Math.ceil(totalUsers.value / perPage.value))

const startIndex = computed(() => (currentPage.value - 1) * perPage.value + 1)
const endIndex = computed(() => Math.min(currentPage.value * perPage.value, totalUsers.value))

const pageNumbers = computed(() => {
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
  // Implement user details view logic
  console.log('View user details:', user)
}

// Watchers
watch(search, () => {
  currentPage.value = 1
  fetchUsers()
})

watch(perPage, () => {
  currentPage.value = 1
  fetchUsers()
})

// Initial fetch
onMounted(fetchUsers)
</script> 