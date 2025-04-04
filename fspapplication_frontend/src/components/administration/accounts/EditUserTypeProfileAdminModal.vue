<template>
  <div class="fixed inset-0 flex items-center justify-center p-5 overflow-y-auto modal z-99999">
    <!-- Background overlay -->
    <div 
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]" 
      aria-hidden="true"
      @click="handleClose"
    ></div>

    <!-- Modal panel -->
    <div class="relative w-full max-w-[584px] rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-10">
      <!-- close btn -->
      <button 
        @click="handleClose" 
        class="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11"
      >
        <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z" fill=""></path>
        </svg>
      </button>
      
      <h4 class="mb-6 text-lg font-medium text-gray-800 dark:text-white/90">
        Edit {{ getTitle() }}
      </h4>

      <div class="space-y-6">
        <!-- Agent Profile Form -->
        <form v-if="isAgent" @submit.prevent="handleAgentSubmit" class="space-y-6">
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Company Name</label>
            <input
              type="text"
              v-model="localAgentData.companyName"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              disabled
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">License Number</label>
            <input
              type="text"
              v-model="localAgentData.licenseNumber"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Years of Experience</label>
            <input
              type="number"
              v-model="localAgentData.yearsOfExperience"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          
          <!-- Form Actions -->
          <div class="flex items-center justify-end gap-3 mt-6">
            <button
              type="button"
              @click="handleClose"
              class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
            >
              Close
            </button>
            <button
              type="submit"
              class="flex items-center justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:bg-opacity-70"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <!-- Client Profile Form -->
        <form v-else-if="isClient" @submit.prevent="handleClientSubmit" class="space-y-6">
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Client</label>
            <multiselect
              v-model="selectedClient"
              :options="clients"
              :searchable="true"
              :close-on-select="true"
              :show-labels="true"
              placeholder="Select a client"
              label="name"
              track-by="id"
              :allow-empty="true"
              :loading="isLoadingClients"
              :disabled="isSaving"
              @input="updateSelectedClient"
              deselect-label="◀ Click to remove"
              selected-label="✓"
              class="dark:text-white/90"
            ></multiselect>
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Industry</label>
            <input
              type="text"
              v-model="localClientData.industry"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Client Since</label>
            <input
              type="date"
              v-model="localClientData.clientSince"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          
          <!-- Form Actions -->
          <div class="flex items-center justify-end gap-3 mt-6">
            <button
              type="button"
              @click="handleClose"
              class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
            >
              Close
            </button>
            <button
              type="submit"
              class="flex items-center justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:bg-opacity-70"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <!-- Employee Profile Form -->
        <form v-else-if="isEmployee" @submit.prevent="handleEmployeeSubmit" class="space-y-6">
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Company Name</label>
            <input
              type="text"
              v-model="localEmployeeData.companyName"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
              disabled
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Department</label>
            <input
              type="text"
              v-model="localEmployeeData.department"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Employee ID</label>
            <input
              type="text"
              v-model="localEmployeeData.employeeId"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Job Title</label>
            <input
              type="text"
              v-model="localEmployeeData.jobTitle"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          <div class="space-y-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">Start Date</label>
            <input
              type="date"
              v-model="localEmployeeData.startDate"
              class="dark:bg-dark-900 h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
            />
          </div>
          
          <!-- Form Actions -->
          <div class="flex items-center justify-end gap-3 mt-6">
            <button
              type="button"
              @click="handleClose"
              class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
            >
              Close
            </button>
            <button
              type="submit"
              class="flex items-center justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:bg-opacity-70"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';
import { clientService, type Client } from '@/service/clientService';
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';

// Define interfaces for the different profile types
interface AgentProfileData {
  companyName?: string;
  licenseNumber?: string | null;
  yearsOfExperience?: number;
}

interface ClientProfileData {
  companyName?: string;
  companyNameId?: string;
  industry?: string | null;
  clientSince?: string; // Date as string in YYYY-MM-DD format
}

interface EmployeeProfileData {
  companyName?: string;
  department?: string;
  employeeId?: string | null;
  jobTitle?: string | null;
  startDate?: string;
  reportsTo?: string | null;
}

const props = defineProps({
  userData: {
    type: Object,
    required: true
  },
  userType: {
    type: String,
    required: true
  },
  agentProfileData: {
    type: Object as () => AgentProfileData,
    default: () => ({})
  },
  clientProfileData: {
    type: Object as () => ClientProfileData,
    default: () => ({})
  },
  employeeProfileData: {
    type: Object as () => EmployeeProfileData,
    default: () => ({})
  },
  isSaving: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'save:agent', 'save:client', 'save:employee']);

// Create local copies for editing
const localAgentData = ref<AgentProfileData>({ ...props.agentProfileData });
const localClientData = ref<ClientProfileData>({
  companyName: props.clientProfileData?.companyName || '',
  companyNameId: props.clientProfileData?.companyNameId || '',
  industry: props.clientProfileData?.industry || null,
  clientSince: props.clientProfileData?.clientSince || new Date().toISOString().split('T')[0]
});
const localEmployeeData = ref<EmployeeProfileData>({ ...props.employeeProfileData });

// State for available clients
const clients = ref<Client[]>([]);
const isLoadingClients = ref(false);
const selectedClient = ref<Client | null>(null);

// Function to fetch clients
const fetchClients = async () => {
  isLoadingClients.value = true;
  try {
    const response = await clientService.getClients({ status: 'active' });
    clients.value = response.results;
    
    // If we have a companyNameId, find the corresponding client and set it as selected
    if (localClientData.value.companyNameId) {
      selectedClient.value = clients.value.find(c => c.id === localClientData.value.companyNameId) || null;
    }
    // If we have a companyName but not a companyNameId, try to match it
    else if (localClientData.value.companyName && !localClientData.value.companyNameId) {
      const matchingClient = clients.value.find(c => c.name === localClientData.value.companyName);
      if (matchingClient) {
        selectedClient.value = matchingClient;
        localClientData.value.companyNameId = matchingClient.id;
      }
    }
  } catch (error) {
    console.error('Error fetching clients:', error);
  } finally {
    isLoadingClients.value = false;
  }
};

// Update selected client
const updateSelectedClient = (client: Client | null) => {
  console.log('Selected client changed:', client);
  if (client) {
    localClientData.value.companyNameId = client.id;
    localClientData.value.companyName = client.name;
  } else {
    localClientData.value.companyNameId = '';
    localClientData.value.companyName = '';
  }
};

// Computed properties to check user type
const isAgent = computed(() => props.userType === 'agent' || props.userType === 'AGENT');
const isClient = computed(() => props.userType === 'client' || props.userType === 'CLIENT');
const isEmployee = computed(() => props.userType === 'employee' || props.userType === 'EMPLOYEE');

// Get form title
const getTitle = () => {
  if (isAgent.value) return 'Agent Profile';
  if (isClient.value) return 'Client Profile';
  if (isEmployee.value) return 'Employee Profile';
  return 'User Profile';
};

// Event handlers
const handleClose = () => {
  emit('close');
};

const handleAgentSubmit = () => {
  emit('save:agent', localAgentData.value);
};

const handleClientSubmit = () => {
  // Check if a client is selected
  if (!selectedClient.value && isClient.value) {
    alert('Please select a client before saving.');
    return;
  }
  
  // Create the data to send to the parent component
  const clientData = {
    ...localClientData.value,
    // Include the client name for display purposes
    companyName: selectedClient.value ? selectedClient.value.name : localClientData.value.companyName,
    companyNameId: selectedClient.value ? selectedClient.value.id : localClientData.value.companyNameId
  };
  
  emit('save:client', clientData);
};

const handleEmployeeSubmit = () => {
  emit('save:employee', localEmployeeData.value);
};

// Watch for changes in props
watch(() => props.clientProfileData, (newData) => {
  if (newData && newData.companyNameId && clients.value.length > 0) {
    selectedClient.value = clients.value.find(c => c.id === newData.companyNameId) || null;
  }
}, { deep: true });

// Fetch clients when component is mounted
onMounted(() => {
  if (isClient.value) {
    fetchClients();
  }
});
</script>

<style>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Multiselect custom styling */
.multiselect {
  min-height: 44px;
}

.multiselect__tags {
  min-height: 44px;
  border-radius: 0.5rem;
  border-color: rgb(209, 213, 219);
  background-color: transparent;
  padding-top: 0.625rem;
  font-size: 0.875rem;
}

.dark .multiselect__tags {
  border-color: rgb(55, 65, 81);
  background-color: rgb(17, 24, 39);
  color: rgba(255, 255, 255, 0.9);
}

.multiselect__placeholder {
  margin-bottom: 10px;
  padding-top: 0;
  color: rgb(156, 163, 175);
}

.dark .multiselect__placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.multiselect__input, 
.multiselect__single {
  background-color: transparent;
  font-size: 0.875rem;
  margin-bottom: 0;
  padding-top: 0;
}

.dark .multiselect__input,
.dark .multiselect__single {
  color: rgba(255, 255, 255, 0.9);
}

.multiselect__content-wrapper {
  border-radius: 0 0 0.5rem 0.5rem;
  border-color: rgb(209, 213, 219);
}

.dark .multiselect__content-wrapper {
  border-color: rgb(55, 65, 81);
  background-color: rgb(17, 24, 39);
}

.multiselect__option {
  font-size: 0.875rem;
  padding: 12px;
  min-height: 40px;
}

.dark .multiselect__option {
  color: rgba(255, 255, 255, 0.9);
}

.multiselect__option--highlight {
  background: rgb(59, 130, 246);
  color: white;
}

.dark .multiselect__option--highlight {
  color: white;
}

.multiselect__option--selected {
  background: rgba(59, 130, 246, 0.1);
  color: rgb(31, 41, 55);
  font-weight: 500;
}

.dark .multiselect__option--selected {
  background: rgba(59, 130, 246, 0.2);
  color: rgba(255, 255, 255, 0.9);
}

.multiselect__option--selected:hover,
.multiselect__option--selected.multiselect__option--highlight {
  background: rgb(239, 68, 68);
  color: white;
}

.multiselect__option--selected:hover:after,
.multiselect__option--selected.multiselect__option--highlight:after {
  color: white;
}

.multiselect__spinner {
  background: #fff;
}

.dark .multiselect__spinner {
  background: rgb(17, 24, 39);
}

.multiselect--disabled {
  opacity: 0.6;
}

/* Fix for deselect label */
.multiselect__select {
  height: 42px;
}

.multiselect__select:before {
  border-color: #666 transparent transparent;
}

.dark .multiselect__select:before {
  border-color: rgba(255, 255, 255, 0.6) transparent transparent;
}

.multiselect__tag {
  background: rgb(59, 130, 246);
  color: white;
}

/* Selection labels styling */
.multiselect__strong,
.multiselect__option span.multiselect__option--selected {
  display: inline-block;
  vertical-align: middle;
  font-weight: 600;
  color: #2c3e50;
}

.dark .multiselect__strong,
.dark .multiselect__option span.multiselect__option--selected {
  color: rgba(255, 255, 255, 0.9);
}

/* Selected label */
.multiselect__option--selected:after {
  content: "✓";
  margin-left: 5px;
  color: #409EFF;
}

.dark .multiselect__option--selected:after {
  color: rgb(59, 130, 246);
}

/* Deselect label - make it more visible */
.multiselect__option--selected .multiselect__option__desc {
  color: rgb(239, 68, 68);
  font-weight: 500;
}

.dark .multiselect__option--selected .multiselect__option__desc {
  color: rgb(248, 113, 113);
}

/* Clear selection button */
.multiselect__clear {
  position: absolute;
  right: 41px;
  height: 40px;
  width: 40px;
  display: block;
  cursor: pointer;
  z-index: 2;
}

.multiselect__clear:before,
.multiselect__clear:after {
  content: "";
  display: block;
  position: absolute;
  width: 2px;
  height: 10px;
  background: #999;
  top: 50%;
  right: 19px;
}

.dark .multiselect__clear:before,
.dark .multiselect__clear:after {
  background: rgba(255, 255, 255, 0.6);
}

.multiselect__clear:before {
  transform: rotate(45deg) translateY(-50%);
}

.multiselect__clear:after {
  transform: rotate(-45deg) translateY(-50%);
}

.multiselect__option span.multiselect__option__deselect {
  color: #f44336;
  font-weight: bold;
  margin-left: 5px;
}

.dark .multiselect__option span.multiselect__option__deselect {
  color: #ff6b6b;
}

/* Override default styling for deselect label */
.multiselect__option--highlight span.multiselect__option__deselect {
  color: white !important;
}
</style> 