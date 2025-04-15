<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <!-- Status Filter Section -->
    <div class="px-5 py-4 sm:px-6 sm:py-5 border-b border-gray-100 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90 mb-3 sm:mb-0">
          Agent Accounts
        </h3>
        
        <!-- Status Filter Buttons/Dropdown -->
        <div class="w-full sm:w-auto flex flex-col items-center">
          <!-- Mobile: Dropdown -->
          <div class="sm:hidden">
            <select 
              v-model="statusFilter" 
              class="form-select w-full rounded-lg border border-gray-300 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
            >
              <option value="active">Active Agents</option>
              <option value="inactive">Inactive Agents</option>
              <option value="all">All Agents</option>
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
              Active Agents
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
              Inactive Agents
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
              All Agents
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
              placeholder="Search agents..." 
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

        <!-- Agent Table -->
        <div class="overflow-x-auto">
          <div class="max-h-[500px] overflow-y-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-800/50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider w-16">
                    LOGO
                  </th>
                  <th @click="sortBy('name')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer w-1/4">
                    NAME
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider w-1/4">
                    ROLE
                  </th>
                  <th @click="sortBy('isActive')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer w-1/4">
                    STATUS
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider w-1/4">
                    VIEW PROFILE
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-if="paginatedAgents.length === 0" class="text-center">
                  <td colspan="5" class="px-4 py-3 text-gray-500 dark:text-gray-400">
                    No agents found
                  </td>
                </tr>
                <tr v-else v-for="agent in paginatedAgents" :key="agent.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                  <td class="px-4 py-3 w-16">
                    <img 
                      :src="getLogoUrl(agent)" 
                      :alt="`${agent.name} logo`"
                      class="h-10 w-10 rounded-full object-cover mx-auto border border-gray-200 dark:border-gray-700"
                      referrerpolicy="no-referrer"
                    />
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-900 dark:text-white/90">
                    {{ getFullName(agent) }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                    {{ getRole(agent) }}
                  </td>
                  <td class="px-4 py-3">
                    <span 
                      :class="[
                        'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                        agent.isActive 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      ]"
                    >
                      {{ agent.isActive ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-sm whitespace-nowrap">
                    <button 
                      @click="viewAgentDetails(agent)" 
                      class="flex items-center text-blue-600 hover:text-blue-700 dark:text-blue-400"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
        </div>

        <!-- Pagination -->
        <div class="bg-white dark:bg-gray-900 px-4 py-3 border-t border-gray-200 dark:border-gray-700 sm:px-6">
          <div class="flex flex-col items-center">
            <div class="text-sm text-gray-700 dark:text-gray-300 mb-2">
              {{ totalAgents === 0 
                ? 'Showing 0 to 0 of 0 entries' 
                : `Showing ${startIndex} to ${endIndex} of ${totalAgents} entries` 
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

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import debounce from 'lodash/debounce'
import { useRouter } from 'vue-router'
import { useAgentStore } from '@/stores/agentStore'
import { fileService } from '@/service/fileService'
import type { Agent } from '@/service/agentService'

type StatusFilter = 'active' | 'inactive' | 'all';
type SortColumn = 'name' | 'email' | 'phone' | 'isActive';

const router = useRouter()
const agentStore = useAgentStore()

// Reactive state
const search = ref('')
const statusFilter = ref<StatusFilter>('active') // Default to active agents
const pageOptions = [5, 10, 25, 50]

// Use values from the store with computed properties for reactivity
const agents = computed(() => agentStore.agents)
const currentPage = computed({
  get: () => agentStore.currentPage,
  set: (value: number) => agentStore.currentPage = value
})
const perPage = computed({
  get: () => agentStore.perPage,
  set: (value: number) => agentStore.setPerPage(value)
})
const totalAgents = computed(() => agentStore.totalAgents)
const totalPages = computed(() => agentStore.totalPages)
const startIndex = computed(() => agentStore.startIndex)
const endIndex = computed(() => agentStore.endIndex)
const pageNumbers = computed(() => agentStore.pageNumbers)

// Use paginatedAgents directly from the store
const paginatedAgents = computed(() => agentStore.agents)

// Debounced search to prevent excessive API calls
const debouncedSearch = debounce(() => {
  agentStore.setSearch(search.value)
}, 500) // 500ms delay

// Methods
const sortBy = (column: SortColumn) => {
  agentStore.setSorting(column)
}

const prevPage = () => {
  agentStore.prevPage()
}

const nextPage = () => {
  agentStore.nextPage()
}

const goToPage = (page: number) => {
  agentStore.goToPage(page)
}

const viewAgentDetails = (agent: Agent) => {
  router.push(`/agent/${agent.id}`)
}

// Method to set status filter
const setStatusFilter = (status: StatusFilter) => {
  if (statusFilter.value === status) return // Don't update if already selected
  statusFilter.value = status
  agentStore.setStatusFilter(status)
}

// Add watcher for statusFilter
watch(statusFilter, (newStatus: StatusFilter) => {
  agentStore.setStatusFilter(newStatus)
})

// Add to template
const searchInput = ref<HTMLInputElement | null>(null)

// Watchers
watch(search, (newSearch) => {
  debouncedSearch()
})

watch(perPage, () => {
  agentStore.setPerPage(perPage.value)
})

// Initial fetch
onMounted(() => {
  // Set initial status filter to 'active' and fetch data
  statusFilter.value = 'active'
  agentStore.setStatusFilter('active')
})

// Default avatar generation function
const generateDefaultAvatar = (name: string) => {
  // Simple hash function for name to get consistent colors for same name
  const getColor = (name: string) => {
    const colors = [
      '#1E88E5', '#43A047', '#E53935', '#5E35B1', '#FB8C00', 
      '#00897B', '#3949AB', '#8E24AA', '#D81B60', '#039BE5'
    ]
    
    let hash = 0
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash)
    }
    
    return colors[Math.abs(hash) % colors.length]
  }

  const initials = name ? name.charAt(0).toUpperCase() : 'A'
  const bgColor = getColor(name || 'Agent')
  
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
    <rect width="100%" height="100%" fill="${bgColor}"/>
    <text x="50" y="50" font-size="40" text-anchor="middle" fill="white" font-family="Arial, sans-serif" dominant-baseline="central">${initials}</text>
  </svg>`
  
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
}

// Function to get proper avatar URL
const getLogoUrl = (agent: Agent) => {
  if (agent.logo) {
    // If logo path exists, use the file service to get the public URL
    return fileService.getPublicFileUrl(agent.logo);
  }
  // Otherwise, generate the default SVG avatar directly
  return generateDefaultAvatar(agent.name || 'Agent');
};

// Update the template to use the correct field names
const getFullName = (agent: Agent) => agent.name;
const getRole = (agent: Agent) => 'Agent';
</script>
