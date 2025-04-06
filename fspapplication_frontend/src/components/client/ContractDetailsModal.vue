<template>
  <BaseModal 
    v-if="show"
    :title="'Contract Details'" 
    :isLoading="isLoading"
    :showSubmitButton="isEditing"
    :submitButtonText="'Save Changes'"
    :loadingText="'Saving...'"
    @close="closeModal"
    @save="handleSave"
  >
    <div class="space-y-6">
      <!-- Contract Information -->
      <div class="space-y-4">
        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Contract Name</h4>
          <div v-if="isEditing" class="mt-1">
            <input
              v-model="editedContract.name"
              type="text"
              class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              placeholder="Enter contract name"
              @keyup.enter="handleSave"
            />
          </div>
          <p v-else class="mt-1 text-base font-medium text-gray-900 dark:text-white">{{ contract.name }}</p>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Description</h4>
          <div v-if="isEditing" class="mt-1">
            <textarea
              v-model="editedContract.description"
              rows="3"
              class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white/90"
              placeholder="Enter contract description"
              @keyup.enter.exact="handleSave"
              @keydown.enter.shift.prevent
            ></textarea>
          </div>
          <p v-else class="mt-1 text-base text-gray-900 dark:text-white">
            {{ contract.description || 'No description provided' }}
          </p>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</h4>
          <span 
            :class="[
              'mt-1 inline-flex px-2.5 py-0.5 rounded-full text-sm font-medium',
              contract.isActive 
                ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400' 
                : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-400'
            ]"
          >
            {{ contract.isActive ? 'Active' : 'Inactive' }}
          </span>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Created</h4>
          <p class="mt-1 text-base text-gray-900 dark:text-white">
            {{ new Date(contract.createdAt).toLocaleDateString() }}
          </p>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</h4>
          <p class="mt-1 text-base text-gray-900 dark:text-white">
            {{ new Date(contract.updatedAt).toLocaleDateString() }}
          </p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
        <button
          v-if="!isEditing"
          @click="toggleStatus"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200',
            contract.isActive 
              ? 'text-white bg-red-600 hover:bg-red-700 focus:ring-red-500 dark:bg-red-500 dark:hover:bg-red-600'
              : 'text-white bg-green-600 hover:bg-green-700 focus:ring-green-500 dark:bg-green-500 dark:hover:bg-green-600'
          ]"
        >
          {{ contract.isActive ? 'Deactivate' : 'Activate' }}
        </button>
        <button
          v-if="!isEditing"
          @click="startEditing"
          class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400 dark:focus:ring-offset-gray-900 transition-colors duration-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          Edit Contract
        </button>
        <button
          v-if="isEditing"
          @click="cancelEditing"
          class="px-4 py-2 text-sm font-medium rounded-lg text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
        >
          Cancel
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import { clientContractService, type Contract } from '@/service/clientContractService';

const props = defineProps<{
  show: boolean;
  contract: Contract;
}>();

const emit = defineEmits(['close', 'status-updated', 'contract-updated']);

const isLoading = ref(false);
const isEditing = ref(false);
const editedContract = reactive<Partial<Contract>>({
  name: '',
  description: ''
});

const closeModal = () => {
  isEditing.value = false;
  emit('close');
};

const toggleStatus = async () => {
  try {
    isLoading.value = true;
    const updatedContract = await clientContractService.updateContractStatus(
      props.contract.id,
      !props.contract.isActive
    );
    emit('status-updated', updatedContract);
  } catch (error) {
    console.error('Error updating contract status:', error);
  } finally {
    isLoading.value = false;
  }
};

const startEditing = () => {
  editedContract.name = props.contract.name;
  editedContract.description = props.contract.description || '';
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};

const handleSave = async () => {
  try {
    isLoading.value = true;
    const updatedContract = await clientContractService.updateContract(
      props.contract.id,
      editedContract
    );
    emit('contract-updated', updatedContract);
    isEditing.value = false;
  } catch (error) {
    console.error('Error updating contract:', error);
  } finally {
    isLoading.value = false;
  }
};
</script> 