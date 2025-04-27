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

      <!-- Agent Profile Display -->
      <div v-if="isAgent && userData" class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">Company Name</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ agentProfileData.companyName || 'Not provided' }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-500 dark:text-gray-400">ABN</p>
          <p class="font-medium text-gray-800 dark:text-white/90">
            {{ agentProfileData.abn || 'Not provided' }}
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
import ComponentCard from '@/components/common/ComponentCard.vue';
import UserTypeProfileEditModal from '@/components/administration/accounts/EditUserTypeProfileAdminModal.vue';
import { convertObjectKeysToCamel } from '@/utils/caseConverter';
import { userProfileAdminService } from '@/service/userProfileAdminService';
import { companyService, type CompanyProfile } from '@/service/companyService';
import { type AgentProfileAdmin, type ClientProfile, type EmployeeProfile, type UserProfileAdmin } from '@/stores/userProfileAdminStore';

// Define interfaces for the different profile types
interface AgentProfileData {
  companyName?: string;
  abn?: string;
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

// Define user data interface
interface UserData extends Partial<UserProfileAdmin> {
  id?: string;
  username?: string;
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

// State for tenant company details
const tenantCompany = ref<CompanyProfile | null>(null);
const isLoadingCompany = ref(false);

// Function to fetch tenant company details
const fetchTenantCompany = async () => {
  // Prevent fetching if already loading or already fetched
  if (isLoadingCompany.value || tenantCompany.value) return;

  isLoadingCompany.value = true;
  try {
    tenantCompany.value = await companyService.getCompanyProfile();
    console.log('[UserTypeProfileAdminCard] Fetched Tenant Company:', tenantCompany.value);
  } catch (error) {
    console.error("[UserTypeProfileAdminCard] Failed to load company details.");
    // Handle error appropriately - maybe show a user message?
  } finally {
    isLoadingCompany.value = false;
  }
};

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
    return 'Not provided';
  }
};

// For debugging
const userTypeDebug = computed(() => {
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
  console.log('[Card Init] initializeProfileData called.'); // Log function entry

  // Log the conditions being checked
  console.log(`[Card Init] isAgent: ${isAgent.value}, has agentProfile: ${!!props.userData.agentProfile}`);
  console.log(`[Card Init] isClient: ${isClient.value}, has clientProfile: ${!!props.userData.clientProfile}`);
  console.log(`[Card Init] isEmployee: ${isEmployee.value}, has employeeProfile: ${!!props.userData.employeeProfile}`);
  
  // Explicitly reset all local profile refs first
  agentProfileData.value = {};
  clientProfileData.value = {};
  employeeProfileData.value = {};
  
  // Set the selected user type dropdown to match current user type
  if (props.userData?.userType) {
    selectedUserType.value = props.userData.userType.toLowerCase();
    // If the initial type is employee, fetch company details
    if (selectedUserType.value === 'employee') {
      fetchTenantCompany();
    }
  }
  
  if (isAgent.value && props.userData.agentProfile) {
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.agentProfile);
    agentProfileData.value = { 
      companyName: profile.companyName || '',
      abn: profile.abn || '',
      yearsOfExperience: profile.yearsOfExperience || 0
    };
    console.log('[Card Init] Populated agentProfileData'); // Added log
  } else if (isClient.value && props.userData.clientProfile) {
    console.log('[Card Init] Raw props.userData.clientProfile:', JSON.parse(JSON.stringify(props.userData.clientProfile)));
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.clientProfile);
    console.log('[Card Init] CamelCased profile:', JSON.parse(JSON.stringify(profile)));
    clientProfileData.value = { 
      companyName: profile.companyName || '',
      companyNameId: profile.companyNameId || '', // Check if this is present
      industry: profile.industry || null,
      clientSince: profile.clientSince || ''
    };
    console.log('[Card Init] Final clientProfileData ref (passed to modal):', JSON.parse(JSON.stringify(clientProfileData.value)));
    console.log('[Card Init] Populated clientProfileData'); // Added log
  } else if (isEmployee.value && props.userData.employeeProfile) {
    console.log('[Card Init] Raw props.userData.employeeProfile:', JSON.parse(JSON.stringify(props.userData.employeeProfile))); // Added log
    // Convert any snake_case keys to camelCase
    const profile = convertObjectKeysToCamel(props.userData.employeeProfile);
    console.log('[Card Init] CamelCased employee profile:', JSON.parse(JSON.stringify(profile))); // Added log
    employeeProfileData.value = { 
      companyName: profile.companyName || '',
      department: profile.department || '',
      employeeId: profile.employeeId || null,
      jobTitle: profile.jobTitle || null,
      startDate: profile.startDate || '',
      reportsTo: profile.reportsTo || null
    };
    console.log('[Card Init] Populated employeeProfileData'); // Added log
    // If company name is missing in profile but we fetched it, update
    if (!employeeProfileData.value.companyName && tenantCompany.value?.name) {
      employeeProfileData.value.companyName = tenantCompany.value.name;
    }
  }
};

// Function to change user type
const changeUserType = async () => {
  if (!props.userData || !props.userData.id) return;

  // Fetch company name if changing to employee and it's not loaded yet
  if (selectedUserType.value === 'employee' && !tenantCompany.value && !isLoadingCompany.value) {
    await fetchTenantCompany(); // Wait for fetch to complete
  }

  isChangingType.value = true;

  try {
    // Create a new user object with updated type and empty profile data
    const updatedUser: UserData = {
      ...props.userData,
      id: String(props.userData.id), // Ensure ID is string
      userType: selectedUserType.value
    };

    // First, clear all profile related data completely
    updatedUser.agentProfile = undefined;
    updatedUser.clientProfile = undefined;
    updatedUser.employeeProfile = undefined;

    // Then set only the new user type's profile to an empty or pre-filled object
    if (selectedUserType.value === 'agent') {
      updatedUser.agentProfile = {} as AgentProfileAdmin; // Type assertion for empty object
    } else if (selectedUserType.value === 'client') {
      updatedUser.clientProfile = {} as ClientProfile; // Type assertion for empty object
    } else if (selectedUserType.value === 'employee') {
      // Pre-fill company name if available
      updatedUser.employeeProfile = {
        companyName: tenantCompany.value?.name || '' // Use fetched name or empty string
      } as EmployeeProfile;
    }

    // --- BEGIN DEBUG LOGS ---
    console.log('[UserTypeProfileAdminCard] changeUserType - Tenant Company Value:', tenantCompany.value);
    console.log('[UserTypeProfileAdminCard] changeUserType - Payload being sent:', JSON.parse(JSON.stringify({
      userType: updatedUser.userType,
      agentProfile: updatedUser.agentProfile,
      clientProfile: updatedUser.clientProfile,
      employeeProfile: updatedUser.employeeProfile,
    })));
    // --- END DEBUG LOGS ---

    // Save to the database using the service
    // Using patchUserProfile might be better if the backend supports partial updates robustly
    // For now, using updateUser as it seems intended to replace the whole user object structure
    await userProfileAdminService.patchUserProfile(String(props.userData.id), {
      userType: updatedUser.userType,
      agentProfile: updatedUser.agentProfile,
      clientProfile: updatedUser.clientProfile,
      employeeProfile: updatedUser.employeeProfile,
    });

    // Fetch the user again to make sure we have the latest data
    const refreshedUser = await userProfileAdminService.getUserProfile(String(props.userData.id));

    // Emit the refreshed user to parent component to ensure UI is updated correctly
    emit('update:user', refreshedUser);

    showChangeTypeConfirm.value = false;
  } catch (error) {
    console.error("Error changing user type:", error);
    // Add user feedback for the error
  } finally {
    isChangingType.value = false;
  }
};

// Save handlers
const handleAgentSave = async (updatedData: AgentProfileData) => {
  isSaving.value = true;
  try {
    // Create a properly typed agent profile object
    const agentProfile = {
      companyName: updatedData.companyName || '',
      abn: updatedData.abn || '', // Ensure abn is never null
      yearsOfExperience: updatedData.yearsOfExperience || 0
    };
    
    // Create the updated user object with the new agent profile data
    // Only include the profile type being saved
    const updatedUser = { 
      // id: String(props.userData.id), // ID is in URL
      agentProfile,
    };
    
    // Save to the database using the service
    if (props.userData.id) {
      // Use patchUserProfile to only send the relevant profile data
      await userProfileAdminService.patchUserProfile(String(props.userData.id), updatedUser);
       // Fetch the user again to get the complete, updated state
      const refreshedUser = await userProfileAdminService.getUserProfile(String(props.userData.id));
      console.log('[UserTypeProfileAdminCard] Refreshed User (after patch):', JSON.parse(JSON.stringify(refreshedUser))); // Log the data
      // Emit the full refreshed user data
      emit('update:user', refreshedUser);
    } else {
      console.error("Cannot save profile: User ID is missing.");
      throw new Error("User ID is missing."); // Prevent modal closing
    }
    
    showEditForm.value = false; // Close modal on success
  } catch (error: any) {
    console.error("Error saving agent profile:", error);
    // Optional: Add user feedback (e.g., toast notification)
    // alert(`Failed to save agent profile: ${error.message}`); 
    // Keep the modal open on error
  } finally {
    isSaving.value = false;
  }
};

const handleClientSave = async (updatedData: ClientProfileData) => {
  isSaving.value = true;
  try {
    // Create a properly typed client profile object
    const clientProfile = {
      companyName: updatedData.companyName || '',
      companyNameId: updatedData.companyNameId || '', // Make sure ID is included
      industry: updatedData.industry || null,
      clientSince: updatedData.clientSince || new Date().toISOString().split('T')[0]
    };
    
    // Create the updated user object with just the client profile
    const updatedUser = { 
      // id: String(props.userData.id), // ID is in URL
      clientProfile,
    };
        
    // Save to the database using the service
    if (props.userData.id) {
      // Use patchUserProfile to only send the relevant profile data
      await userProfileAdminService.patchUserProfile(String(props.userData.id), updatedUser);
      // Fetch the user again to get the complete, updated state
      const refreshedUser = await userProfileAdminService.getUserProfile(String(props.userData.id));
      console.log('[UserTypeProfileAdminCard] Refreshed User (after patch):', JSON.parse(JSON.stringify(refreshedUser))); // Log the data
      // Emit the full refreshed user data
      emit('update:user', refreshedUser);
    } else {
      console.error("Cannot save profile: User ID is missing.");
      throw new Error("User ID is missing."); // Prevent modal closing
    }
    
    showEditForm.value = false; // Close modal on success
  } catch (error: any) {
    console.error("Error saving client profile:", error);
    // Optional: Add user feedback
    // alert(`Failed to save client profile: ${error.message}`);
     // Keep the modal open on error
  } finally {
    isSaving.value = false;
  }
};

const handleEmployeeSave = async (updatedData: EmployeeProfileData) => {
  isSaving.value = true;
  try {
    // Create a properly typed employee profile object
    // EXCLUDE companyName as it's read-only on the backend serializer
    // const finalCompanyName = updatedData.companyName || tenantCompany.value?.name || '';
    const employeeProfile = {
      // companyName: finalCompanyName, // DO NOT SEND read-only field
      department: updatedData.department || '',
      employeeId: updatedData.employeeId || null,
      jobTitle: updatedData.jobTitle || null,
      startDate: updatedData.startDate || new Date().toISOString().split('T')[0],
      reportsTo: updatedData.reportsTo || null
    };

    // Create the updated user object with just the employee profile
    const updatedUser = {
      // id: String(props.userData.id), // ID is in URL
      employeeProfile,
    };

    // --- BEGIN DEBUG LOG ---
    console.log('[UserTypeProfileAdminCard] handleEmployeeSave - Payload being sent:', JSON.parse(JSON.stringify(updatedUser)));
    // --- END DEBUG LOG ---

    // Save to the database using the service
    if (props.userData.id) {
      // Use patchUserProfile to only send the relevant profile data
      await userProfileAdminService.patchUserProfile(String(props.userData.id), updatedUser);
       // Fetch the user again to get the complete, updated state
      const refreshedUser = await userProfileAdminService.getUserProfile(String(props.userData.id));
      console.log('[UserTypeProfileAdminCard] Refreshed User (after patch):', JSON.parse(JSON.stringify(refreshedUser))); // Log the data
      // Emit the full refreshed user data
      emit('update:user', refreshedUser);
    } else {
      console.error("Cannot save profile: User ID is missing.");
      throw new Error("User ID is missing."); // Prevent modal closing
    }

    showEditForm.value = false; // Close modal on success
  } catch (error: any) {
    console.error("Error saving employee profile:", error);
    // Log detailed error response from backend if available
    if (error.response && error.response.data) {
      console.error("Backend validation error:", error.response.data);
    }
    // Optional: Add user feedback
    // alert(`Failed to save employee profile: ${error.message}`);
    // Keep the modal open on error
  } finally {
    isSaving.value = false;
  }
};

// Watcher to fetch company details when 'employee' is selected
watch(selectedUserType, (newType) => {
  if (newType === 'employee') {
    fetchTenantCompany();
  }
});

// Initialize on mount and when userData changes
onMounted(() => {
    initializeProfileData();
    // Optionally fetch company details immediately if the initial type is employee
    // Already handled within initializeProfileData
});
watch(() => props.userData, initializeProfileData, { deep: true });
</script> 