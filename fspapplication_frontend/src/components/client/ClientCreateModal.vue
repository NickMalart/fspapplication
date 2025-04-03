<template>
  <BaseModal 
    v-if="show"
    :title="'Create New Client'" 
    :isLoading="isLoading"
    :submitButtonText="'Create Client'"
    :loadingText="'Creating...'"
    @close="closeModal"
    @save="handleSubmit"
  >
    <p class="mb-6 text-sm text-gray-500 dark:text-gray-400">
      Add basic client information to get started
    </p>
    
    <div class="space-y-4">
      <!-- Basic Information -->
      <div>
        <label for="name" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Client Name <span class="text-red-500">*</span>
        </label>
        <input
          id="name"
          v-model="clientData.name"
          type="text"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter client name"
        />
      </div>
      
      <div>
        <label for="abn" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          ABN
        </label>
        <input
          id="abn"
          v-model="clientData.abn"
          type="text"
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter ABN"
        />
      </div>
      
      <div>
        <label for="email" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Email <span class="text-red-500">*</span>
        </label>
        <input
          id="email"
          v-model="clientData.email"
          type="email"
          required
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter email address"
        />
      </div>
      
      <div>
        <label for="phone" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Phone
        </label>
        <input
          id="phone"
          v-model="clientData.phone"
          type="text"
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="Enter phone number"
        />
      </div>
      
      <div>
        <label for="website" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-200">
          Website
        </label>
        <input
          id="website"
          v-model="clientData.website"
          type="url"
          class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700"
          placeholder="https://example.com"
        />
      </div>
    </div>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import BaseModal from '@/components/ui/BaseModal.vue';
import { useClientStore } from '@/stores/clientStore';
import type { Client } from '@/service/clientService';

defineProps<{
  show: boolean
}>();

const emit = defineEmits(['close', 'client-created']);
const clientStore = useClientStore();

const isLoading = ref(false);
const clientData = reactive<Partial<Client>>({
  name: '',
  abn: '',
  email: '',
  phone: '',
  website: ''
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = async () => {
  try {
    isLoading.value = true;
    const newClient = await clientStore.addClient(clientData); 
    
    if (newClient) {
      emit('client-created', newClient);
      resetForm();
      closeModal();
    } else {
      console.error('Client creation failed'); // Added error handling for client creation
    }
  } catch (error) {
    console.error('Error creating client:', error);
    // Handle error (show notification, etc.)
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  clientData.name = '';
  clientData.abn = '';
  clientData.email = '';
  clientData.phone = '';
  clientData.website = '';
};
</script> 