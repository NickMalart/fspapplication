<template>
  <div 
    class="fixed inset-0 z-999 overflow-y-auto"
    aria-labelledby="modal-title" 
    role="dialog" 
    aria-modal="true"
  >
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
        aria-hidden="true"
        @click="handleClose"
      ></div>

      <!-- Modal panel -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white dark:bg-boxdark rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="px-6 py-4 border-b border-stroke dark:border-strokedark">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-medium text-black dark:text-white">
              Edit {{ getTitle() }}
            </h3>
            <button 
              @click="handleClose" 
              class="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400 focus:outline-none"
            >
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6">
          <!-- Agent Profile Form -->
          <form v-if="isAgent" @submit.prevent="handleAgentSubmit">
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Company Name</label>
              <input
                type="text"
                v-model="localAgentData.company_name"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                disabled
              />
            </div>
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">License Number</label>
              <input
                type="text"
                v-model="localAgentData.license_number"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-6">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Years of Experience</label>
              <input
                type="number"
                v-model="localAgentData.years_of_experience"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="flex items-center justify-end gap-4.5">
              <button
                type="button"
                @click="handleClose"
                class="flex justify-center rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="flex items-center justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 disabled:bg-opacity-70"
                :disabled="isSaving"
              >
                <span v-if="isSaving" class="mr-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>

          <!-- Client Profile Form -->
          <form v-else-if="isClient" @submit.prevent="handleClientSubmit">
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Company Name</label>
              <input
                type="text"
                v-model="localClientData.company_name"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Industry</label>
              <input
                type="text"
                v-model="localClientData.industry"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-6">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Client Since</label>
              <input
                type="date"
                v-model="localClientData.client_since"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="flex items-center justify-end gap-4.5">
              <button
                type="button"
                @click="handleClose"
                class="flex justify-center rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="flex items-center justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 disabled:bg-opacity-70"
                :disabled="isSaving"
              >
                <span v-if="isSaving" class="mr-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>

          <!-- Employee Profile Form -->
          <form v-else-if="isEmployee" @submit.prevent="handleEmployeeSubmit">
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Company Name</label>
              <input
                type="text"
                v-model="localEmployeeData.company_name"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                disabled
              />
            </div>
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Department</label>
              <input
                type="text"
                v-model="localEmployeeData.department"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Employee ID</label>
              <input
                type="text"
                v-model="localEmployeeData.employee_id"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-4">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Job Title</label>
              <input
                type="text"
                v-model="localEmployeeData.job_title"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="mb-6">
              <label class="mb-2.5 block text-sm font-medium text-black dark:text-white">Start Date</label>
              <input
                type="date"
                v-model="localEmployeeData.start_date"
                class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              />
            </div>
            <div class="flex items-center justify-end gap-4.5">
              <button
                type="button"
                @click="handleClose"
                class="flex justify-center rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="flex items-center justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 disabled:bg-opacity-70"
                :disabled="isSaving"
              >
                <span v-if="isSaving" class="mr-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Define interfaces for the different profile types
interface AgentProfileData {
  company_name?: string;
  license_number?: string;
  years_of_experience?: number;
}

interface ClientProfileData {
  company_name?: string;
  industry?: string;
  client_since?: string; // Date as string in YYYY-MM-DD format
}

interface EmployeeProfileData {
  company_name?: string;
  department?: string;
  employee_id?: string;
  job_title?: string;
  start_date?: string; // Date as string in YYYY-MM-DD format
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
const localClientData = ref<ClientProfileData>({ ...props.clientProfileData });
const localEmployeeData = ref<EmployeeProfileData>({ ...props.employeeProfileData });

// Computed properties to check user type
const isAgent = computed(() => {
  const userType = props.userType?.toLowerCase();
  return userType === 'agent';
});

const isClient = computed(() => {
  const userType = props.userType?.toLowerCase();
  return userType === 'client';
});

const isEmployee = computed(() => {
  const userType = props.userType?.toLowerCase();
  return userType === 'employee';
});

// Get appropriate title based on user type
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
  emit('save:agent', { ...localAgentData.value });
};

const handleClientSubmit = () => {
  emit('save:client', { ...localClientData.value });
};

const handleEmployeeSubmit = () => {
  emit('save:employee', { ...localEmployeeData.value });
};

// Initialize local data when component is mounted
onMounted(() => {
  localAgentData.value = { ...props.agentProfileData };
  localClientData.value = { ...props.clientProfileData };
  localEmployeeData.value = { ...props.employeeProfileData };
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style> 