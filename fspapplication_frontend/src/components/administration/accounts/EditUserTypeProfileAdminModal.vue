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
        <form v-if="isAgent" @submit.prevent="handleAgentSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Company Name</label>
            <input
              type="text"
              v-model="localAgentData.companyName"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
              disabled
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">ABN</label>
            <input
              type="text"
              v-model="localAgentData.abn"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Years of Experience</label>
            <input
              type="number"
              v-model="localAgentData.yearsOfExperience"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          
          <!-- Form Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="handleClose"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-700"
            >
              Close
            </button>
            <button
              type="submit"
              class="rounded-md bg-brand-500 px-4 py-2 text-sm font-medium text-white hover:bg-brand-600 disabled:opacity-50"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <!-- Client Profile Form -->
        <form v-else-if="isClient" @submit.prevent="handleClientSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">
              Client
            </label>
            <select
              v-model="localClientData.companyNameId"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
              :disabled="isSaving || isLoadingClients"
              @change="updateSelectedClientFromId"
            >
              <option value="" disabled>Select a client</option>
              <option v-for="client in clients" :key="client.id" :value="client.id">
                {{ client.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Industry</label>
            <input
              type="text"
              v-model="localClientData.industry"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Client Since</label>
            <div class="relative date-picker-wrapper">
              <input
                type="date"
                ref="clientSinceInput"
                v-model="localClientData.clientSince"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700 appearance-none"
              />
              <div
                class="absolute right-4 top-1/2 transform -translate-y-1/2 cursor-pointer"
                @click="focusClientSincePicker"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">Format: MM/DD/YYYY</p>
          </div>
          
          <!-- Form Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="handleClose"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-700"
            >
              Close
            </button>
            <button
              type="submit"
              class="rounded-md bg-brand-500 px-4 py-2 text-sm font-medium text-white hover:bg-brand-600 disabled:opacity-50"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>

        <!-- Employee Profile Form -->
        <form v-else-if="isEmployee" @submit.prevent="handleEmployeeSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Company Name</label>
            <!-- Display fetched tenant company name -->
            <p class="mt-1 block w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2 text-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700">
              <span v-if="isLoadingCompany">Loading...</span>
              <span v-else>{{ tenantCompany?.name || 'Tenant Company Not Found' }}</span> 
            </p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Department</label>
            <input
              type="text"
              v-model="localEmployeeData.department"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Employee ID</label>
            <input
              type="text"
              v-model="localEmployeeData.employeeId"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Job Title</label>
            <input
              type="text"
              v-model="localEmployeeData.jobTitle"
              class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-400">Start Date</label>
            <div class="relative date-picker-wrapper">
              <input
                type="date"
                ref="startDateInput"
                v-model="localEmployeeData.startDate"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-white dark:border-gray-700 appearance-none"
              />
              <div 
                class="absolute right-4 top-1/2 transform -translate-y-1/2 cursor-pointer" 
                @click="focusStartDatePicker"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">Format: MM/DD/YYYY</p> 
          </div>
          
          <!-- Form Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="handleClose"
              class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-700"
            >
              Close
            </button>
            <button
              type="submit"
              class="rounded-md bg-brand-500 px-4 py-2 text-sm font-medium text-white hover:bg-brand-600 disabled:opacity-50"
              :disabled="isSaving"
            >
              <span v-if="isSaving" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, watchEffect } from 'vue';
import { clientService, type Client } from '@/service/clientService';
import { companyService, type CompanyProfile } from '@/service/companyService';

// Define interfaces for the different profile types
interface AgentProfileData {
  companyName?: string;
  abn?: string | null;
  yearsOfExperience?: number;
}

interface ClientProfileData {
  companyName?: string;
  companyNameId?: string;
  industry?: string | null;
  clientSince?: string | null; // Allow string or null
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

// Helper function to format date to YYYY-MM-DD or return undefined
const formatDateForInput = (dateString: string | null | undefined): string | undefined => {
  if (!dateString) return undefined;
  try {
    const date = new Date(dateString);
    if (!isNaN(date.getTime())) {
      return date.toISOString().split('T')[0];
    }
  } catch (e) {
    console.error('Error parsing date:', e);
  }
  return undefined; // Return undefined if invalid or parsing fails
};

// Create local copies for editing
const localAgentData = ref<AgentProfileData>({ ...props.agentProfileData });
// Initialize companyNameId as empty, let watchEffect handle setting it.
// Format clientSince date during initialization.
const localClientData = ref<ClientProfileData>({
  companyName: props.clientProfileData?.companyName || '',
  companyNameId: '', // Initialize as empty
  industry: props.clientProfileData?.industry || null,
  clientSince: formatDateForInput(props.clientProfileData?.clientSince) || null // Format on init
});
const localEmployeeData = ref<EmployeeProfileData>({ ...props.employeeProfileData });

// Log initial local state
console.log('[Modal Setup] Initial localClientData:', JSON.parse(JSON.stringify(localClientData.value)));

// State for available clients
const clients = ref<Client[]>([]);
const isLoadingClients = ref(false);

// State for tenant company details
const tenantCompany = ref<CompanyProfile | null>(null);
const isLoadingCompany = ref(false);

// Add refs for date inputs
const startDateInput = ref<HTMLInputElement | null>(null);
const clientSinceInput = ref<HTMLInputElement | null>(null); // Added ref for client since

// Function to fetch clients
const fetchClients = async () => {
  isLoadingClients.value = true;
  console.log('[fetchClients] Starting fetch...');
  try {
    // Request a larger page size to get more clients for the dropdown
    const response = await clientService.getClients({ status: 'active', pageSize: 100 });
    clients.value = response.results;
    console.log(`[fetchClients] Fetched ${clients.value.length} clients:`, JSON.parse(JSON.stringify(clients.value)));
    // Removed the explicit ID setting from here
  } catch (error) {
    console.error('[fetchClients] Error fetching clients:', error);
    // TODO: Add user-facing error message
  } finally {
    isLoadingClients.value = false;
  }
};

// Function to fetch tenant company details
const fetchTenantCompany = async () => {
  isLoadingCompany.value = true;
  try {
    tenantCompany.value = await companyService.getCompanyProfile();
  } catch (error) {
    console.error("Failed to load company details for modal display.");
    // Handle error appropriately - maybe show a default or error message
  } finally {
    isLoadingCompany.value = false;
  }
};

// Add function to focus start date picker
const focusStartDatePicker = () => {
  if (startDateInput.value) {
    startDateInput.value.showPicker();
  }
};

// Function to focus client since date picker
const focusClientSincePicker = () => {
  if (clientSinceInput.value) {
    clientSinceInput.value.showPicker();
  }
};

// Update selected client based on select event
const updateSelectedClientFromId = (event: Event) => {
  const select = event.target as HTMLSelectElement;
  const id = select.value;
  if (id) {
    localClientData.value.companyNameId = id;
    localClientData.value.companyName = clients.value.find(c => c.id === id)?.name || '';
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
  if (!localClientData.value.companyNameId && isClient.value) {
    alert('Please select a client before saving.');
    return;
  }
  
  // Create the data to send to the parent component
  const clientData = {
    ...localClientData.value,
    // Format date before emitting - needs to be string | null for ClientProfileData
    clientSince: formatDateForInput(localClientData.value.clientSince) || null, 
    // Include the client name for display purposes
    companyName: localClientData.value.companyName,
    companyNameId: localClientData.value.companyNameId
  };
  
  emit('save:client', clientData);
};

const handleEmployeeSubmit = () => {
  const employeeData = {
      ...localEmployeeData.value,
      startDate: formatDateForInput(localEmployeeData.value.startDate) // Format date before emitting
  };
  emit('save:employee', employeeData);
};

// Fetch necessary data when component is mounted
onMounted(() => {
  if (isClient.value) {
    fetchClients();
  }
  if (isEmployee.value) {
    fetchTenantCompany(); // Fetch company details if editing an employee
  }
  // Removed initForm call - let watchers handle initial state
});

// Watch for changes in the specific profile data props and update local state
watch(() => props.agentProfileData, (newData) => {
  localAgentData.value = { ...newData };
}, { deep: true, immediate: true }); // Add immediate

// Watch client profile data - primarily for non-ID fields now
watch(() => props.clientProfileData, (newData) => {
  console.log('[watch props.clientProfileData] Running. newData:', JSON.parse(JSON.stringify(newData)));
  // Update non-ID fields. ID setting is handled by watchEffect.
  // Preserve the ID potentially set by watchEffect.
  // Format date if props change after mount.
  localClientData.value = {
    ...localClientData.value, // Keep existing ID
    companyName: newData?.companyName || '', // Update name if provided
    industry: newData?.industry || null,
    clientSince: formatDateForInput(newData?.clientSince) || null
   };
  // Log current state but avoid setting ID here directly
  console.log('[watch props.clientProfileData] Updated localClientData (non-ID fields only):', JSON.parse(JSON.stringify(localClientData.value)));
}, { deep: true }); // Remove immediate: true

watch(() => props.employeeProfileData, (newData) => {
  console.log('[EditUserTypeProfileAdminModal] Watcher - newData:', JSON.parse(JSON.stringify(newData)));
  // Ensure companyName is copied correctly, even if initially null/undefined
  localEmployeeData.value = { 
      ...newData,
      startDate: formatDateForInput(newData?.startDate), // Format date on init/watch
      companyName: newData?.companyName || '' 
  };
  console.log('[EditUserTypeProfileAdminModal] Watcher - updated localEmployeeData:', JSON.parse(JSON.stringify(localEmployeeData.value)));
}, { deep: true, immediate: true }); // Add immediate

// Use watchEffect to synchronize the companyNameId when both props and clients are ready
watchEffect(() => {
  console.log(`[watchEffect] Running. isClient: ${isClient.value}, Clients loaded: ${clients.value.length > 0}, Props ID: ${props.clientProfileData?.companyNameId}`);

  // Ensure we are dealing with the client form, clients are loaded, and props have an ID
  if (isClient.value && clients.value.length > 0 && props.clientProfileData?.companyNameId) {
    const clientIdToSet = props.clientProfileData.companyNameId;
    console.log(`[watchEffect] Condition met: Has client ID from props (${clientIdToSet}). Current local ID: ${localClientData.value.companyNameId}`);

    // Check if the client ID exists in the fetched list
    const clientExists = clients.value.some(client => client.id === clientIdToSet);
    console.log(`[watchEffect] Does client ID ${clientIdToSet} exist in fetched clients? ${clientExists}`);

    if (clientExists) {
       // Only update if the ID is different from the current local state
       if (localClientData.value.companyNameId !== clientIdToSet) {
           console.log(`[watchEffect] Setting companyNameId from props to: ${clientIdToSet}`);
           localClientData.value.companyNameId = clientIdToSet;
           // Also update the name for consistency if it wasn't updated by the other watcher
           const selectedClient = clients.value.find(c => c.id === clientIdToSet);
           if (selectedClient && localClientData.value.companyName !== selectedClient.name) {
               localClientData.value.companyName = selectedClient.name;
               console.log(`[watchEffect] Updated companyName based on new ID to: ${selectedClient.name}`);
           }
       } else {
         console.log(`[watchEffect] companyNameId (${clientIdToSet}) already matches props ID. No change needed.`);
       }
    } else {
        console.warn(`[watchEffect] Client ID ${clientIdToSet} from props not found in fetched clients list. Will reset selection if currently set.`);
        // If the ID from props isn't valid according to the fetched list, reset the selection
        if (localClientData.value.companyNameId !== '') {
            console.log(`[watchEffect] Resetting companyNameId because ID from props (${clientIdToSet}) is invalid or not found.`);
            localClientData.value.companyNameId = '';
            localClientData.value.companyName = '';
        }
    }
  } else if (isClient.value && clients.value.length > 0 && !props.clientProfileData?.companyNameId) {
      console.log(`[watchEffect] Condition met: Clients loaded, but props has NO client ID.`);
      // If clients are loaded but props explicitly have no ID, ensure local state is reset
      if (localClientData.value.companyNameId !== '') {
          console.log(`[watchEffect] Resetting companyNameId as props has no ID.`);
          localClientData.value.companyNameId = '';
          localClientData.value.companyName = '';
      }
  } else if (isClient.value && clients.value.length === 0 && props.clientProfileData?.companyNameId) {
      // Handle case where props have ID but clients aren't loaded yet: pre-set the ID
      // The effect will run again when clients load to validate and potentially update the name
      console.log(`[watchEffect] Condition met: Props has client ID (${props.clientProfileData.companyNameId}), but clients NOT loaded yet.`);
      if (localClientData.value.companyNameId !== props.clientProfileData.companyNameId) {
          console.log(`[watchEffect] Pre-setting companyNameId to ${props.clientProfileData.companyNameId} while waiting for clients.`);
          localClientData.value.companyNameId = props.clientProfileData.companyNameId;
          // Keep existing name or name from props if available
          localClientData.value.companyName = props.clientProfileData.companyName || localClientData.value.companyName || '';
          console.log(`[watchEffect] Pre-set localClientData:`, JSON.parse(JSON.stringify(localClientData.value)));
      }
  } else {
      console.log(`[watchEffect] Conditions not met for ID synchronization or reset.`);
  }
  console.log(`[watchEffect] Finished run. Final localClientData.companyNameId: ${localClientData.value.companyNameId}`);
});
</script>

<!-- Add scoped styles -->
<style scoped>
/* Improve date picker styling for different browsers */
input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
}

/* Ensure clicking anywhere in the date picker wrapper activates the date input */
.date-picker-wrapper {
  position: relative;
}

/* Override browser default styling */
input[type="date"] {
  color-scheme: light dark;
}

/* Fix date picker text color in dark mode */
.dark input[type="date"] {
  color: rgb(229 231 235); /* Equivalent to text-gray-200 */
}
</style>

