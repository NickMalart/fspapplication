<!-- Client Warehouse Table -->
<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <!-- Header Section -->
    <div class="px-5 py-4 sm:px-6 sm:py-5 border-b border-gray-100 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90">
          Client Warehouses
        </h3>
        
        <div class="flex flex-col items-end space-y-3">
          <!-- Create Warehouse Button -->
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400 dark:focus:ring-offset-gray-900 transition-colors duration-200 border border-transparent whitespace-nowrap"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 stroke-current" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create Warehouse
          </button>

          <!-- Status Filter Buttons/Dropdown -->
          <div class="w-full sm:w-auto">
            <!-- Mobile: Dropdown -->
            <div class="sm:hidden w-full">
              <select 
                v-model="statusFilter" 
                class="form-select w-full rounded-lg border border-gray-300 text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white/90"
              >
                <option value="active">Active Warehouses</option>
                <option value="inactive">Inactive Warehouses</option>
                <option value="all">All Warehouses</option>
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
                Active Warehouses
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
                Inactive Warehouses
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
                All Warehouses
              </button>
            </div>
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
          <div class="relative flex items-center w-full sm:w-64 md:w-80 lg:w-96">
            <input 
              ref="searchInput"
              v-model="search" 
              type="text" 
              placeholder="Search warehouses..." 
              class="pl-3 pr-10 py-2 form-input rounded-lg border border-gray-300 w-full dark:bg-gray-700 dark:border-gray-600 dark:text-white/90 dark:placeholder-gray-400"
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

        <!-- Warehouses Table -->
        <div class="overflow-x-auto">
          <div class="max-h-[500px] overflow-y-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-800/50">
                <tr>
                  <th @click="sortBy('name')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                    NAME
                  </th>
                  <th @click="sortBy('city')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                    LOCATION
                  </th>
                  <th @click="sortBy('isPrimary')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                    TYPE
                  </th>
                  <th @click="sortBy('isActive')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                    STATUS
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    ACTIONS
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-if="loading" class="text-center">
                  <td colspan="5" class="px-4 py-3">
                    <div class="flex justify-center">
                      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="warehouses.length === 0" class="text-center">
                  <td colspan="5" class="px-4 py-3 text-gray-500 dark:text-gray-400">
                    No warehouses found
                  </td>
                </tr>
                <tr 
                  v-else
                  v-for="warehouse in warehouses" 
                  :key="warehouse.id" 
                  class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200"
                >
                  <td class="px-4 py-3 text-sm text-gray-900 dark:text-white/90">
                    {{ warehouse.name }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                    <div class="max-w-xs">
                      <span 
                        :title="formatLocation(warehouse)" 
                        class="block truncate"
                      >
                        {{ formatLocation(warehouse) }}
                      </span>
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <span 
                      :class="[
                        'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                        warehouse.isPrimary 
                          ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-400' 
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-400'
                      ]"
                    >
                      {{ warehouse.isPrimary ? 'Primary' : 'Secondary' }}
                    </span>
                  </td>
                  <td class="px-4 py-3">
                    <span 
                      :class="[
                        'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                        warehouse.isActive 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400' 
                          : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-400'
                      ]"
                    >
                      {{ warehouse.isActive ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-sm whitespace-nowrap">
                    <button 
                      @click="viewWarehouseDetails(warehouse)" 
                      class="flex items-center text-blue-600 hover:text-blue-700 dark:text-blue-400"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      View Details
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
              {{ totalWarehouses === 0 
                ? 'Showing 0 to 0 of 0 entries' 
                : `Showing ${startIndex} to ${endIndex} of ${totalWarehouses} entries` 
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

  <!-- Warehouse Create Modal -->
  <ClientWarehouseCreateModal
    v-if="showCreateModal"
    :show="showCreateModal"
    :client-name="clientName"
    :client-id="clientId"
    @close="showCreateModal = false"
    @warehouse-created="handleWarehouseCreated"
  />

  <!-- Warehouse Details Modal -->
  <ClientWarehouseDetailsModal
    v-if="showDetailsModal && selectedWarehouse"
    :show="showDetailsModal"
    :warehouse="selectedWarehouse"
    @close="closeDetailsModal"
    @status-updated="handleStatusUpdated"
    @warehouse-updated="handleWarehouseUpdated"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';
import debounce from 'lodash/debounce';
import ClientWarehouseCreateModal from '@/components/client/ClientWarehouseCreateModal.vue';
import ClientWarehouseDetailsModal from '@/components/client/ClientWarehouseDetailsModal.vue';

// Define the Warehouse interface
interface Warehouse {
  id: string;
  name: string;
  client: string;
  description: string | null;
  streetNumber: string | null;
  streetName: string | null;
  suburb: string | null;
  city: string | null;
  state: string | null;
  postalCode: string | null;
  country: string | null;
  latitude: number | null;
  longitude: number | null;
  contactName: string | null;
  contactPhone: string | null;
  contactEmail: string | null;
  isPrimary: boolean;
  operatingHours: string | null;
  storageCapacity: string | null;
  specialInstructions: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

const API_URL = import.meta.env.VITE_API_URL || '/api';
const router = useRouter();
const props = defineProps<{
  clientId: string;
  clientName: string;
}>();

// State
const warehouses = ref<Warehouse[]>([]);
const loading = ref(false);
const search = ref('');
const pageOptions = [5, 10, 25, 50];
const currentPage = ref(1);
const perPage = ref(10);
const totalWarehouses = ref(0);
const sortColumn = ref('name');
const sortDirection = ref<'asc' | 'desc'>('asc');
const showCreateModal = ref(false);
const showDetailsModal = ref(false);
const selectedWarehouse = ref<Warehouse | null>(null);
const statusFilter = ref<'active' | 'inactive' | 'all'>('active'); // Default to active warehouses

// Computed properties
const totalPages = computed(() => Math.ceil(totalWarehouses.value / perPage.value));
const startIndex = computed(() => (currentPage.value - 1) * perPage.value + 1);
const endIndex = computed(() => Math.min(currentPage.value * perPage.value, totalWarehouses.value));
const pageNumbers = computed(() => {
  const pages = [];
  const maxVisiblePages = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
  let end = Math.min(totalPages.value, start + maxVisiblePages - 1);
  
  if (end - start + 1 < maxVisiblePages) {
    start = Math.max(1, end - maxVisiblePages + 1);
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

// Helper function to format location
const formatLocation = (warehouse: Warehouse): string => {
  const parts = [];
  if (warehouse.city) parts.push(warehouse.city);
  if (warehouse.state) parts.push(warehouse.state);
  if (warehouse.country) parts.push(warehouse.country);
  
  return parts.length > 0 ? parts.join(', ') : 'No location';
};

// Methods
const fetchWarehouses = async () => {
  loading.value = true;
  try {
    const apiParams = {
      search: search.value,
      ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`,
      page: currentPage.value,
      page_size: perPage.value,
      status: statusFilter.value
    };
    
    const response = await axios.get(`${API_URL}/client/clients/${props.clientId}/warehouses/`, { params: apiParams });
    
    warehouses.value = response.data.results.map((warehouse: any) => convertObjectKeysToCamel(warehouse));
    totalWarehouses.value = response.data.count;
  } catch (error) {
    console.error('Error fetching warehouses:', error);
  } finally {
    loading.value = false;
  }
};

const sortBy = (column: string) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortColumn.value = column;
    sortDirection.value = 'asc';
  }
  fetchWarehouses();
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchWarehouses();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    fetchWarehouses();
  }
};

const goToPage = (page: number) => {
  currentPage.value = page;
  fetchWarehouses();
};

const viewWarehouseDetails = (warehouse: Warehouse) => {
  selectedWarehouse.value = warehouse;
  showDetailsModal.value = true;
};

const closeDetailsModal = () => {
  showDetailsModal.value = false;
  selectedWarehouse.value = null;
};

const handleStatusUpdated = (updatedWarehouse: Warehouse) => {
  // Update the warehouse in the list
  const index = warehouses.value.findIndex(w => w.id === updatedWarehouse.id);
  if (index !== -1) {
    warehouses.value[index] = updatedWarehouse;
    // Update the selected warehouse in the modal
    if (selectedWarehouse.value && selectedWarehouse.value.id === updatedWarehouse.id) {
      selectedWarehouse.value = updatedWarehouse;
    }
  }
};

const handleWarehouseUpdated = (updatedWarehouse: Warehouse) => {
  // Update the warehouse in the list
  const index = warehouses.value.findIndex(w => w.id === updatedWarehouse.id);
  if (index !== -1) {
    warehouses.value[index] = updatedWarehouse;
  }
  closeDetailsModal();
};

const handleWarehouseCreated = (newWarehouse: Warehouse) => {
  // Refresh the warehouses list
  fetchWarehouses();
};

// Method to set status filter
const setStatusFilter = (status: 'active' | 'inactive' | 'all') => {
  statusFilter.value = status;
  currentPage.value = 1; // Reset to first page when changing filter
  fetchWarehouses();
};

// Debounced search
const debouncedSearch = debounce(() => {
  currentPage.value = 1;
  fetchWarehouses();
}, 300);

// Watchers
watch(search, () => {
  debouncedSearch();
});

watch(perPage, () => {
  currentPage.value = 1;
  fetchWarehouses();
});

watch(statusFilter, () => {
  currentPage.value = 1;
  fetchWarehouses();
});

// Initialize
onMounted(() => {
  fetchWarehouses();
});
</script> 