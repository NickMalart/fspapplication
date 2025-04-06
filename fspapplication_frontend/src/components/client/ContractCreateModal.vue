<template>
  <BaseModal 
    v-if="show"
    :title="'Create New Contract'" 
    :isLoading="isLoading"
    :submitButtonText="'Create Contract'"
    :loadingText="'Creating...'"
    @close="closeModal"
    @save="handleSubmit"
  >
    <p class="mb-6 text-sm text-gray-500 dark:text-gray-400">
      Add contract information for {{ clientName }}
    </p>
    
    <div class="space-y-4">
      <!-- Contract Information -->
      <div>
        <label for="name" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Contract Name <span class="text-red-500">*</span>
        </label>
        <input
          id="name"
          v-model="contractData.name"
          type="text"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
          placeholder="Enter contract name"
        />
      </div>
      
      <div>
        <label for="description" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Description
        </label>
        <textarea
          id="description"
          v-model="contractData.description"
          rows="3"
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
          placeholder="Enter contract description"
        ></textarea>
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive, type PropType } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import { clientContractService, type Contract } from '@/service/clientContractService';

const props = defineProps<{
  show: boolean;
  clientName: string;
  clientId: string;
}>();

const emit = defineEmits(['close', 'contract-created']);

const isLoading = ref(false);
const contractData = reactive<Partial<Contract>>({
  name: '',
  description: '',
  isActive: true, // Set default value but don't show in UI
  client: props.clientId // Initialize with the client ID
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = async () => {
  try {
    isLoading.value = true;
    // Ensure client ID is set before submitting
    contractData.client = props.clientId;
    const newContract = await clientContractService.createContract(contractData);
    
    if (newContract) {
      emit('contract-created', newContract);
      resetForm();
      closeModal();
    } else {
      console.error('Contract creation failed');
    }
  } catch (error) {
    console.error('Error creating contract:', error);
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  contractData.name = '';
  contractData.description = '';
  // Reset while maintaining the client ID
  contractData.client = props.clientId;
};
</script> 