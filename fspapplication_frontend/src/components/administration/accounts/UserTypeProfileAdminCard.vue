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
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ agentProfileData.companyName || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">License Number</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ agentProfileData.licenseNumber || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Years of Experience</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ agentProfileData.yearsOfExperience || 'Not provided' }}
          </p>
        </div>
      </div>

      <!-- Client Profile Display -->
      <div v-else-if="isClient && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ clientProfileData.companyName || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Industry</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ clientProfileData.industry || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Client Since</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ formatDate(clientProfileData.clientSince) }}
          </p>
        </div>
      </div>

      <!-- Employee Profile Display -->
      <div v-else-if="isEmployee && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ employeeProfileData.companyName || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Department</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ employeeProfileData.department || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Employee ID</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ employeeProfileData.employeeId || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Job Title</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ employeeProfileData.jobTitle || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Start Date</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ formatDate(employeeProfileData.startDate) }}
          </p>
        </div>
      </div>

      <!-- No profile type detected -->
      <div v-else class="py-4 text-center text-gray-500 dark:text-gray-400">
        No specific profile type detected for this user (Type: {{ userTypeDebug }}). <br>
        Please ensure the user account is properly configured with one of the following types: agent, client, or employee.
      </div>

      <!-- Change User Type Section -->
      <div class="mt-8 pt-6 border-t border-gray-200 dark:border-strokedark">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between">
          <div class="mb-4 md:mb-0">
            <h4 class="text-sm font-medium text-gray-800 dark:text-white/90 mb-1">Change User Type</h4>
            <p class="text-xs text-gray-500 dark:text-gray-400">Change the user's profile type and associated data</p>
          </div>
          <div class="flex items-center space-x-3">
            <select 
              v-model="selectedUserType" 
              class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-800"
            >
              <option value="agent" class="py-1 bg-white text-gray-800 dark:bg-gray-800 dark:text-white">Agent</option>
              <option value="client" class="py-1 bg-white text-gray-800 dark:bg-gray-800 dark:text-white">Client</option>
              <option value="employee" class="py-1 bg-white text-gray-800 dark:bg-gray-800 dark:text-white">Employee</option>
            </select>
            <button 
              @click="showChangeTypeConfirm = true"
              :disabled="userData?.userType?.toLowerCase() === selectedUserType"
              class="inline-flex items-center rounded-lg bg-brand-500 px-4 py-2.5 text-center text-sm font-medium text-white hover:bg-brand-600 disabled:bg-opacity-50 disabled:cursor-not-allowed"
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
      class="fixed inset-0 z-99999 flex items-center justify-center p-5 overflow-y-auto modal"
      aria-labelledby="modal-title" 
      role="dialog" 
      aria-modal="true"
    >
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]" 
        aria-hidden="true"
        @click="showChangeTypeConfirm = false"
      ></div>

      <!-- Modal panel -->
      <div class="relative w-full max-w-[584px] rounded-3xl bg-white p-6 dark:bg-gray-900 lg:p-10">
        <!-- close btn -->
        <button 
          @click="showChangeTypeConfirm = false" 
          class="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11"
        >
          <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z" fill=""></path>
          </svg>
        </button>
        
        <h4 class="mb-6 text-lg font-medium text-gray-800 dark:text-white/90">
          Change User Type
        </h4>
        
        <div class="space-y-6">
          <div class="space-y-4">
            <p class="text-sm text-gray-700 dark:text-gray-300">
              Are you sure you want to change this user from <strong>{{ userTypeLabel(userData?.userType) }}</strong> to <strong>{{ userTypeLabel(selectedUserType) }}</strong>?
            </p>
            <p class="text-sm text-gray-700 dark:text-gray-300">
              This will clear any existing profile data for the current user type. You will need to set up the new profile type information afterward.
            </p>
            <div class="p-3 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700 rounded-md">
              <p class="text-sm text-yellow-700 dark:text-yellow-200">
                <span class="font-bold">Warning:</span> This action cannot be undone.
              </p>
            </div>
          </div>
          
          <div class="flex items-center justify-end gap-3 mt-6">
            <button
              type="button"
              @click="showChangeTypeConfirm = false"
              class="flex justify-center rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200"
            >
              Close
            </button>
            <button
              @click="changeUserType"
              class="flex items-center justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-medium text-white shadow-theme-xs hover:bg-brand-600 disabled:bg-opacity-70"
              :disabled="isChangingType"
            >
              <span v-if="isChangingType" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></span>
              {{ isChangingType ? 'Changing...' : 'Confirm Change' }}
            </button>
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
import { convertObjectKeysToCamel } from '@/utils/caseConverter';

// Define interfaces for the different profile types
interface AgentProfileData {
  companyName?: string;
  licenseNumber?: string | null;
  yearsOfExperience?: number;
}

interface ClientProfileData {
  companyName?: string;
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

// Define user data interface
interface UserData {
  id?: number | string;
  userType?: string;
  username?: string;
  email?: string;
  firstName?: string;
  lastName?: string;
  isActive?: boolean;
  isStaff?: boolean;
  isTenantOwner?: boolean;
  dateJoined?: string;
  lastLogin?: string | null;
  profile?: any;
  functionalGroups?: any[];
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
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.agentProfile);
    agentProfileData.value = { 
      companyName: profile.companyName || '',
      licenseNumber: profile.licenseNumber || null,
      yearsOfExperience: profile.yearsOfExperience || 0
    };
  } else if (isClient.value && props.userData.clientProfile) {
    console.log('Client profile found:', props.userData.clientProfile);
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.clientProfile);
    clientProfileData.value = { 
      companyName: profile.companyName || '',
      industry: profile.industry || null,
      clientSince: profile.clientSince || ''
    };
  } else if (isEmployee.value && props.userData.employeeProfile) {
    console.log('Employee profile found:', props.userData.employeeProfile);
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.employeeProfile);
    employeeProfileData.value = { 
      companyName: profile.companyName || '',
      department: profile.department || '',
      employeeId: profile.employeeId || null,
      jobTitle: profile.jobTitle || null,
      startDate: profile.startDate || '',
      reportsTo: profile.reportsTo || null
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