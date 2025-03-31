<template>
  <ComponentCard :title="getProfileTitle()">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-900 text-red-700 dark:text-red-300 px-4 py-3 rounded">
      {{ error }}
    </div>

    <!-- Data Display with Edit Button in Relative Position -->
    <div v-else class="relative">
      <!-- Edit Button -->
      <button 
        v-if="userData" 
        @click="showEditForm = true"
        class="absolute top-0 right-0 p-1.5 hover:bg-gray-100 dark:hover:bg-boxdark-2 rounded-full"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
      </button>

      <!-- Debugging info for development -->
      <div v-if="isDevelopment" class="mb-4 p-3 bg-gray-100 dark:bg-gray-800 rounded text-xs">
        <p>Debug - User Type: {{ userTypeDebug }}</p>
        <p>Is Agent: {{ isAgent }}</p>
        <p>Is Client: {{ isClient }}</p>
        <p>Is Employee: {{ isEmployee }}</p>
      </div>

      <!-- Agent Profile Display -->
      <div v-if="isAgent && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-black dark:text-white">
            {{ agentProfileData.company_name || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">License Number</p>
          <p class="font-medium text-black dark:text-white">
            {{ agentProfileData.license_number || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Years of Experience</p>
          <p class="font-medium text-black dark:text-white">
            {{ agentProfileData.years_of_experience || 'Not provided' }}
          </p>
        </div>
      </div>

      <!-- Client Profile Display -->
      <div v-else-if="isClient && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-black dark:text-white">
            {{ clientProfileData.company_name || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Industry</p>
          <p class="font-medium text-black dark:text-white">
            {{ clientProfileData.industry || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Client Since</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatDate(clientProfileData.client_since) }}
          </p>
        </div>
      </div>

      <!-- Employee Profile Display -->
      <div v-else-if="isEmployee && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-black dark:text-white">
            {{ employeeProfileData.company_name || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Department</p>
          <p class="font-medium text-black dark:text-white">
            {{ employeeProfileData.department || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Employee ID</p>
          <p class="font-medium text-black dark:text-white">
            {{ employeeProfileData.employee_id || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Job Title</p>
          <p class="font-medium text-black dark:text-white">
            {{ employeeProfileData.job_title || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Start Date</p>
          <p class="font-medium text-black dark:text-white">
            {{ formatDate(employeeProfileData.start_date) }}
          </p>
        </div>
      </div>

      <!-- No profile type detected -->
      <div v-else class="py-4 text-center text-gray-500">
        No specific profile type detected for this user (Type: {{ userTypeDebug }}). <br>
        Please ensure the user account is properly configured with one of the following types: agent, client, or employee.
      </div>

      <!-- Change User Type Section -->
      <div class="mt-8 pt-6 border-t border-gray-200 dark:border-strokedark">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between">
          <div class="mb-4 md:mb-0">
            <h4 class="text-sm font-medium text-black dark:text-white mb-1">Change User Type</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400">Change the user's profile type and associated data</p>
          </div>
          <div class="flex items-center space-x-3">
            <select 
              v-model="selectedUserType" 
              class="rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 text-sm text-black outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
            >
              <option value="agent">Agent</option>
              <option value="client">Client</option>
              <option value="employee">Employee</option>
            </select>
            <button 
              @click="showChangeTypeConfirm = true"
              :disabled="userData?.userType?.toLowerCase() === selectedUserType"
              class="inline-flex items-center rounded bg-primary py-2 px-4 text-center text-sm font-medium text-white hover:bg-opacity-90 disabled:bg-opacity-50 disabled:cursor-not-allowed"
            >
              Change Type
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <UserTypeProfileEditModal
      v-if="showEditForm && userData"
      :userData="userData"
      :userType="userTypeDebug"
      :agentProfileData="agentProfileData"
      :clientProfileData="clientProfileData"
      :employeeProfileData="employeeProfileData"
      :isSaving="isSaving"
      @close="showEditForm = false"
      @save:agent="handleAgentSave"
      @save:client="handleClientSave"
      @save:employee="handleEmployeeSave"
    />

    <!-- Change Type Confirmation Modal -->
    <div 
      v-if="showChangeTypeConfirm" 
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
          @click="showChangeTypeConfirm = false"
        ></div>

        <!-- Modal panel -->
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white dark:bg-boxdark rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="px-6 py-4 border-b border-stroke dark:border-strokedark">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-medium text-black dark:text-white">
                Change User Type
              </h3>
              <button 
                @click="showChangeTypeConfirm = false" 
                class="text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400 focus:outline-none"
              >
                <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <div class="p-6">
            <div class="mb-6">
              <p class="text-sm text-gray-700 dark:text-gray-300 mb-4">
                Are you sure you want to change this user from <strong>{{ userTypeLabel(userData?.userType) }}</strong> to <strong>{{ userTypeLabel(selectedUserType) }}</strong>?
              </p>
              <p class="text-sm text-gray-700 dark:text-gray-300 mb-4">
                This will clear any existing profile data for the current user type. You will need to set up the new profile type information afterward.
              </p>
              <div class="p-3 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-900 rounded-md">
                <p class="text-sm text-yellow-700 dark:text-yellow-200">
                  <span class="font-bold">Warning:</span> This action cannot be undone.
                </p>
              </div>
            </div>
            <div class="flex items-center justify-end gap-4.5">
              <button
                type="button"
                @click="showChangeTypeConfirm = false"
                class="flex justify-center rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
              >
                Cancel
              </button>
              <button
                @click="changeUserType"
                class="flex items-center justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 disabled:bg-opacity-70"
                :disabled="isChangingType"
              >
                <span v-if="isChangingType" class="mr-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isChangingType ? 'Changing...' : 'Confirm Change' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </ComponentCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useToast } from '@/composables/useToast';
import ComponentCard from '@/components/common/ComponentCard.vue';
import UserTypeProfileEditModal from './UserTypeProfileEditModal.vue';

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

// Define user data interface
interface UserData {
  id?: number | string;
  userType?: string;
  username?: string;
  email?: string;
  agentProfile?: AgentProfileData;
  clientProfile?: ClientProfileData;
  employeeProfile?: EmployeeProfileData;
  [key: string]: any; // Allow for additional properties
}

const props = defineProps({
  userData: {
    type: Object as () => UserData,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:user']);
const { showToast } = useToast();
const isSaving = ref(false);
const showEditForm = ref(false);

// User type change state
const selectedUserType = ref('agent');
const showChangeTypeConfirm = ref(false);
const isChangingType = ref(false);

// Create separate refs for each profile type
const agentProfileData = ref<AgentProfileData>({});
const clientProfileData = ref<ClientProfileData>({});
const employeeProfileData = ref<EmployeeProfileData>({});

// Helper function to get a nice label for user types
const userTypeLabel = (type?: string) => {
  if (!type) return 'Unknown';
  
  const typeMap: Record<string, string> = {
    'agent': 'Agent',
    'client': 'Client',
    'employee': 'Employee'
  };
  
  return typeMap[type.toLowerCase()] || type;
};

// Format date for display
const formatDate = (dateString?: string) => {
  if (!dateString) return 'Not provided';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Not provided';
    
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  } catch (e) {
    console.error('Error formatting date:', e);
    return 'Not provided';
  }
};

// Check if in development mode - safe to use in script section
const isDevelopment = computed(() => {
  try {
    return import.meta.env.DEV === true;
  } catch (e) {
    return false;
  }
});

// For debugging
const userTypeDebug = computed(() => {
  console.log('User data:', props.userData);
  console.log('User type:', props.userData?.userType);
  return props.userData?.userType || 'undefined';
});

// Improved computed properties to check user type with more flexibility
const isAgent = computed(() => {
  const userType = props.userData?.userType;
  return userType === 'agent' || userType === 'AGENT';
});

const isClient = computed(() => {
  const userType = props.userData?.userType;
  return userType === 'client' || userType === 'CLIENT';
});

const isEmployee = computed(() => {
  const userType = props.userData?.userType;
  return userType === 'employee' || userType === 'EMPLOYEE';
});

// Get appropriate title based on user type
const getProfileTitle = () => {
  if (isAgent.value) return 'Agent Profile Information';
  if (isClient.value) return 'Client Profile Information';
  if (isEmployee.value) return 'Employee Profile Information';
  return `Profile Information (Type: ${userTypeDebug.value})`;
};

// Initialize profile data based on user type
const initializeProfileData = () => {
  console.log('Initializing profile data for user type:', props.userData?.userType);
  
  // Set the selected user type to match current user type
  if (props.userData?.userType) {
    selectedUserType.value = props.userData.userType.toLowerCase();
  }
  
  if (isAgent.value && props.userData.agentProfile) {
    console.log('Agent profile found:', props.userData.agentProfile);
    agentProfileData.value = { 
      company_name: props.userData.agentProfile.company_name || '',
      license_number: props.userData.agentProfile.license_number || '',
      years_of_experience: props.userData.agentProfile.years_of_experience || 0
    };
  } else if (isClient.value && props.userData.clientProfile) {
    console.log('Client profile found:', props.userData.clientProfile);
    clientProfileData.value = { 
      company_name: props.userData.clientProfile.company_name || '',
      industry: props.userData.clientProfile.industry || '',
      client_since: props.userData.clientProfile.client_since || ''
    };
  } else if (isEmployee.value && props.userData.employeeProfile) {
    console.log('Employee profile found:', props.userData.employeeProfile);
    employeeProfileData.value = { 
      company_name: props.userData.employeeProfile.company_name || '',
      department: props.userData.employeeProfile.department || '',
      employee_id: props.userData.employeeProfile.employee_id || '',
      job_title: props.userData.employeeProfile.job_title || '',
      start_date: props.userData.employeeProfile.start_date || ''
    };
  } else {
    console.log('No matching profile type found');
  }
};

// Function to change user type
const changeUserType = async () => {
  if (!props.userData) return;
  
  isChangingType.value = true;
  
  try {
    // Create a new user object with updated type and empty profile data
    const updatedUser = { 
      ...props.userData,
      userType: selectedUserType.value
    };
    
    // Remove existing profile data for the old type
    if (selectedUserType.value === 'agent') {
      updatedUser.agentProfile = {}; // Create empty agent profile
      updatedUser.clientProfile = undefined;
      updatedUser.employeeProfile = undefined;
    } else if (selectedUserType.value === 'client') {
      updatedUser.clientProfile = {}; // Create empty client profile
      updatedUser.agentProfile = undefined;
      updatedUser.employeeProfile = undefined;
    } else if (selectedUserType.value === 'employee') {
      updatedUser.employeeProfile = {}; // Create empty employee profile
      updatedUser.agentProfile = undefined;
      updatedUser.clientProfile = undefined;
    }
    
    // Emit the updated user to parent component
    emit('update:user', updatedUser);
    
    showToast(`User type changed to ${userTypeLabel(selectedUserType.value)}`, 'success');
    showChangeTypeConfirm.value = false;
  } catch (error) {
    showToast('Failed to change user type', 'error');
    console.error('Error changing user type:', error);
  } finally {
    isChangingType.value = false;
  }
};

// Save handlers
const handleAgentSave = async (updatedData: AgentProfileData) => {
  isSaving.value = true;
  try {
    // API call would go here
    const updatedUser = { ...props.userData, agentProfile: updatedData };
    emit('update:user', updatedUser);
    showToast('Agent profile updated successfully', 'success');
    showEditForm.value = false;
  } catch (error) {
    showToast('Failed to update agent profile', 'error');
    console.error('Error updating agent profile:', error);
  } finally {
    isSaving.value = false;
  }
};

const handleClientSave = async (updatedData: ClientProfileData) => {
  isSaving.value = true;
  try {
    // API call would go here
    const updatedUser = { ...props.userData, clientProfile: updatedData };
    emit('update:user', updatedUser);
    showToast('Client profile updated successfully', 'success');
    showEditForm.value = false;
  } catch (error) {
    showToast('Failed to update client profile', 'error');
    console.error('Error updating client profile:', error);
  } finally {
    isSaving.value = false;
  }
};

const handleEmployeeSave = async (updatedData: EmployeeProfileData) => {
  isSaving.value = true;
  try {
    // API call would go here
    const updatedUser = { ...props.userData, employeeProfile: updatedData };
    emit('update:user', updatedUser);
    showToast('Employee profile updated successfully', 'success');
    showEditForm.value = false;
  } catch (error) {
    showToast('Failed to update employee profile', 'error');
    console.error('Error updating employee profile:', error);
  } finally {
    isSaving.value = false;
  }
};

// Initialize on mount and when userData changes
onMounted(initializeProfileData);
watch(() => props.userData, initializeProfileData, { deep: true });
</script> 