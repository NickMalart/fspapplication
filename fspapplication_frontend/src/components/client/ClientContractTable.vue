<!-- Client Contract Table -->
<template>
  <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <!-- Header Section -->
    <div class="px-5 py-4 sm:px-6 sm:py-5 border-b border-gray-100 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-3 sm:space-y-0">
        <h3 class="text-base font-medium text-gray-800 dark:text-white/90 mb-3 sm:mb-0">
          Client Contracts
        </h3>
      </div>
    </div>

    <div class="border-t border-gray-100 p-5 dark:border-gray-800 sm:p-6">
      <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-800/50">
        <!-- Search Bar -->
        <div class="p-4 border-b border-gray-200 dark:border-gray-700">
          <div class="relative flex items-center w-full sm:w-64 md:w-80 lg:w-96">
            <input 
              ref="searchInput"
              v-model="search" 
              type="text" 
              placeholder="Search contracts..." 
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

        <!-- Contracts Table -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-800/50">
              <tr>
                <th @click="sortBy('name')" class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer">
                  CONTRACT NAME
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="loading" class="text-center">
                <td class="px-4 py-3">
                  <div class="flex justify-center">
                    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                  </div>
                </td>
              </tr>
              <tr v-else-if="contracts.length === 0" class="text-center">
                <td class="px-4 py-3 text-gray-500 dark:text-gray-400">
                  No contracts found
                </td>
              </tr>
              <tr 
                v-else
                v-for="contract in contracts" 
                :key="contract.id" 
                class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200"
              >
                <td class="px-4 py-3 text-sm text-gray-900 dark:text-white/90">
                  {{ contract.name }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { contractService, type Contract } from '@/service/contractService';
import debounce from 'lodash/debounce';

const props = defineProps<{
  clientId: string;
}>();

// State
const contracts = ref<Contract[]>([]);
const loading = ref(false);
const search = ref('');
const sortColumn = ref('name');
const sortDirection = ref<'asc' | 'desc'>('asc');

// Methods
const fetchContracts = async () => {
  loading.value = true;
  try {
    const response = await contractService.getContracts({
      client: props.clientId,
      search: search.value,
      ordering: `${sortDirection.value === 'desc' ? '-' : ''}${sortColumn.value}`
    });
    contracts.value = response.results;
  } catch (error) {
    console.error('Error fetching contracts:', error);
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
  fetchContracts();
};

// Debounced search
const debouncedSearch = debounce(() => {
  fetchContracts();
}, 300);

// Watch for search changes
watch(search, () => {
  debouncedSearch();
});

// Initialize
onMounted(() => {
  fetchContracts();
});
</script> 