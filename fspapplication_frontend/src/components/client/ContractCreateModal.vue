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
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
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
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter contract description"
        ></textarea>
      </div>
      
      <div>
        <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Status
        </label>
        <div class="flex items-center space-x-4">
          <label class="inline-flex items-center">
            <input
              type="radio"
              v-model="contractData.isActive"
              :value="true"
              class="form-radio text-primary focus:ring-primary"
            />
            <span class="ml-2">Active</span>
          </label>
          <label class="inline-flex items-center">
            <input
              type="radio"
              v-model="contractData.isActive"
              :value="false"
              class="form-radio text-primary focus:ring-primary"
            />
            <span class="ml-2">Inactive</span>
          </label>
        </div>
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import { contractService, type Contract } from '@/service/contractService';

defineProps<{
  show: boolean;
  clientName: string;
}>();

const emit = defineEmits(['close', 'contract-created']);

const isLoading = ref(false);
const contractData = reactive<Partial<Contract>>({
  name: '',
  description: '',
  isActive: true
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = async () => {
  try {
    isLoading.value = true;
    const newContract = await contractService.createContract(contractData);
    
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
  contractData.isActive = true;
};
</script> 