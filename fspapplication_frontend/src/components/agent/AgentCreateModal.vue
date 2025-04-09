<template>
  <BaseModal 
    v-if="show"
    :title="'Create New Agent'" 
    :isLoading="isLoading"
    :submitButtonText="'Create Agent'"
    :loadingText="'Creating...'"
    @close="closeModal"
    @save="handleSubmit"
  >
    <p class="mb-6 text-sm text-gray-500 dark:text-gray-400">
      Add basic agent information to get started. Additional details can be added later.
    </p>
    
    <div class="space-y-4">
      <!-- Company Name -->
      <div>
        <label for="companyName" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Company Name <span class="text-red-500">*</span>
        </label>
        <input
          id="companyName"
          v-model="agentData.agentProfile!.companyName"
          type="text"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter company name"
        />
      </div>

      <!-- Email -->
      <div>
        <label for="email" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Email <span class="text-red-500">*</span>
        </label>
        <input
          id="email"
          v-model="agentData.email"
          type="email"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter email address"
        />
      </div>

      <!-- ABN -->
      <div>
        <label for="abn" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          ABN <span class="text-red-500">*</span>
        </label>
        <input
          id="abn"
          v-model="agentData.agentProfile!.abn"
          type="text"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter Australian Business Number"
        />
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import { userAccountsService } from '@/service/userAccountsService';
import type { UserAccount } from '@/service/userAccountsService';

defineProps<{
  show: boolean
}>();

const emit = defineEmits(['close', 'user-created']);
const isLoading = ref(false);

interface AgentProfile {
  companyName: string;
  abn: string | null;
  yearsOfExperience: number;
}

interface ExtendedUserAccount extends UserAccount {
  agentProfile?: AgentProfile;
}

const agentData = ref<Partial<ExtendedUserAccount>>({
  email: '',
  userType: 'agent',
  isActive: true,
  profile: {
    id: '',
    phoneNumber: '',
    emergencyContact: null,
    emergencyContactFirstName: null,
    emergencyContactLastName: null,
    streetNumber: null,
    streetName: null,
    suburb: null,
    city: null,
    state: null,
    postalCode: null,
    country: null,
    latitude: null,
    longitude: null,
    googlePlaceId: null,
    dateOfBirth: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  agentProfile: {
    companyName: '',
    abn: null,
    yearsOfExperience: 0
  }
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = async () => {
  try {
    const userData: Partial<ExtendedUserAccount> = {
      email: agentData.value.email,
      userType: 'agent',
      isActive: true,
      profile: agentData.value.profile,
      agentProfile: agentData.value.agentProfile
    };

    const newUser = await userAccountsService.createUser(userData);
    emit('user-created', newUser);
    closeModal();
  } catch (error) {
    console.error('Error creating agent:', error);
    // Handle error appropriately
  }
};

const resetForm = () => {
  agentData.value.email = '';
  agentData.value.agentProfile!.companyName = '';
  agentData.value.agentProfile!.abn = null;
};
</script> 