<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <!-- Status Filter Section -->
    <div class="px-5 py-4 sm:px-6 sm:py-5 border-b border-gray-100 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90 mb-3 sm:mb-0">
          Client Accounts
        </h3>
        
        <!-- Status Filter Buttons/Dropdown -->
        <div class="w-full sm:w-auto flex flex-col items-center">
          <!-- Mobile: Dropdown -->
          <div class="sm:hidden">
            <select 
              v-model="statusFilter" 
              class="form-select w-full rounded-lg border border-gray-300 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
            >
              <option value="active">Active Clients</option>
              <option value="inactive">Inactive Clients</option>
              <option value="all">All Clients</option>
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
              Active Clients
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
              Inactive Clients
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
              All Clients
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
              placeholder="Search clients..." 
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

        <!-- Client Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th @click="sortBy('name')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Name
                  <span v-if="sortColumn === 'name'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('abn')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  ABN
                  <span v-if="sortColumn === 'abn'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('email')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Email
                  <span v-if="sortColumn === 'email'">
                    {{ sortDirection === 'asc' ? '▲' : '▼' }}
                  </span>
                </th>
                <th @click="sortBy('phone')" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  Phone
                  <span v-if="sortColumn === 'phone'">
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
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="paginatedClients.length === 0" class="text-center">
                <td colspan="6" class="px-6 py-4 text-gray-500 dark:text-gray-400">
                  No clients found
                </td>
              </tr>
              <tr v-else v-for="client in paginatedClients" :key="client.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white/90">
                    {{ client.name }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ client.abn || 'Not provided' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ client.email }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ client.phone || 'Not provided' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                      client.isActive 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ client.isActive ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button 
                    @click="viewClientDetails(client)" 
                    class="inline-flex items-center px-3 py-1.5 mr-2 text-sm font-medium rounded-lg text-blue-600 hover:text-blue-700 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/50 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    View
                  </button>
                  <button 
                    @click="toggleClientStatus(client)" 
                    :class="[
                      'inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
                      client.isActive 
                        ? 'text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/50' 
                        : 'text-green-600 hover:text-green-700 hover:bg-green-50 dark:text-green-400 dark:hover:bg-green-900/50'
                    ]"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path v-if="client.isActive" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ client.isActive ? 'Deactivate' : 'Activate' }}
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
              {{ totalClients === 0 
                ? 'Showing 0 to 0 of 0 entries' 
                : `Showing ${startIndex} to ${endIndex} of ${totalClients} entries` 
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
import { useClientStore } from '@/stores/clientStore'

const router = useRouter()
const clientStore = useClientStore()

// Reactive state
const search = ref('')
const statusFilter = ref('active') // Default to active clients
const pageOptions = [5, 10, 25, 50]

// Use values from the store with computed properties for reactivity
const clients = computed(() => clientStore.clients)
const currentPage = computed({
  get: () => clientStore.currentPage,
  set: (value) => clientStore.currentPage = value
})
const perPage = computed({
  get: () => clientStore.perPage,
  set: (value) => clientStore.setPerPage(value)
})
const totalClients = computed(() => clientStore.totalClients)
const totalPages = computed(() => clientStore.totalPages)
const sortColumn = computed(() => clientStore.sortColumn)
const sortDirection = computed(() => clientStore.sortDirection)
const startIndex = computed(() => clientStore.startIndex)
const endIndex = computed(() => clientStore.endIndex)
const pageNumbers = computed(() => clientStore.pageNumbers)
const loading = computed(() => clientStore.loading)

// Computed properties
const paginatedClients = computed(() => clients.value)

// Debounced search to prevent excessive API calls
const debouncedSearch = debounce(() => {
  clientStore.setSearch(search.value)
}, 500) // 500ms delay

// Methods
const sortBy = (column) => {
  clientStore.setSorting(column)
}

const prevPage = () => {
  clientStore.prevPage()
}

const nextPage = () => {
  clientStore.nextPage()
}

const goToPage = (page) => {
  clientStore.goToPage(page)
}

const viewClientDetails = (client) => {
  router.push(`/client/${client.id}`)
}

const toggleClientStatus = async (client) => {
  await clientStore.updateClientStatus(client.id, !client.isActive)
}

// Method to set status filter
const setStatusFilter = (status) => {
  statusFilter.value = status
  clientStore.setStatusFilter(status)
}

// Enhanced search method
const performSearch = () => {
  clientStore.setSearch(search.value)
}

// Add to template
const searchInput = ref(null)

// Watchers
watch(search, (newSearch) => {
  debouncedSearch()
})

watch(perPage, () => {
  clientStore.setPerPage(perPage.value)
})

watch(statusFilter, () => {
  clientStore.setStatusFilter(statusFilter.value)
})

// Initial fetch
onMounted(() => {
  clientStore.fetchClients()
})
</script> 