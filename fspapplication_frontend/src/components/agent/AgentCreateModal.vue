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
          v-model="agentData.name"
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
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

defineProps<{
  show: boolean
}>();

const emit = defineEmits(['close', 'agent-created']);
const isLoading = ref(false);

interface AgentData {
  name: string;
  email: string;
  phone: string;
}

const agentData = ref<AgentData>({
  name: '',
  email: '',
  phone: ''
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = async () => {
  try {
    isLoading.value = true;
    
    // Use axios directly or create a dedicated agentService
    const response = await axios.post(`${API_URL}/agent/create-agent/`, agentData.value);
    
    emit('agent-created', response.data);
    resetForm();
    closeModal();
  } catch (error) {
    console.error('Error creating agent:', error);
    // Handle error appropriately
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  agentData.value.name = '';
  agentData.value.email = '';
  agentData.value.phone = '';
};
</script> 