<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0f172a] text-white">
    <div class="flex flex-col lg:flex-row items-center gap-10 px-6 py-12 w-full max-w-6xl">
      <!-- Selection Box -->
      <div class="bg-[#1e293b] rounded-xl p-10 w-full max-w-md shadow-lg">
        <div class="flex flex-col items-center">
          <h2 class="text-2xl font-bold mb-1">Select Tenant</h2>
          <p class="text-sm text-gray-400 mb-8">
            Choose the account you want to access.
          </p>
        </div>

        <!-- Tenant List -->
        <div v-if="tenantList && tenantList.length > 0" class="space-y-4">
          <button
            v-for="tenant in tenantList"
            :key="tenant.schema_name"
            @click="selectTenant(tenant)"
            :disabled="!tempToken"
            type="button"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-md text-lg font-semibold transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ tenant.name }}
          </button>
        </div>
        <div v-else-if="isLoading">
           <p class="text-center text-gray-400">Loading tenant information...</p>
           <!-- Optional: Add spinner -->
        </div>
         <div v-else>
           <p class="text-center text-red-400">Could not load tenant information or no tenants assigned. Please try logging in again.</p>
           <button
             @click="goToLogin"
             class="mt-4 mx-auto block px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md text-sm font-semibold transition"
           >
             Return to Login
          </button>
        </div>

      </div>

      <!-- Right Side Image -->
      <div class="hidden lg:block">
        <img
          :src="loginImg"
          alt="Illustration"
          class="w-[1000px] max-w-full"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import loginImg from '@/assets/103.png';

// Interface for tenant data
interface TenantInfo {
  name: string;
  schema_name: string;
  domain: string | null;
}

const router = useRouter();
const authStore = useAuthStore();
const isLoading = ref(true);

// Computed properties to get data from the store
const tenantList = computed(() => authStore.tenantListForSelection);
const tempToken = computed(() => authStore.tempTokenForSelection);

onMounted(() => {
  // Data should already be in the store, set by AuthCallback.vue
  isLoading.value = false;

  // Optional: Check if data is missing and redirect if necessary
  if (!tenantList.value || !tempToken.value) {
      // Consider setting an error message or redirecting
      // goToLogin();
  }
});

const selectTenant = (tenant: TenantInfo) => {
  if (!tempToken.value) {
      // TODO: Show error to user?
      return;
  }

  if (tenant.domain) {
    // Construct the finalization URL on the tenant domain
    const port = window.location.port ? `:${window.location.port}` : '';
    // Use http for localhost development, adjust protocol if needed for production
    const finalizeUrl = `http://${tenant.domain}${port}/auth/finalize/?token=${encodeURIComponent(tempToken.value)}`;

    // Consider clearing selection state *after* successful finalization?
    window.location.href = finalizeUrl; // Perform the redirect
  } else {
    // Handle configuration error - show a message to the user
    alert(`Configuration error: Domain is missing for tenant ${tenant.name}. Please contact support.`);
  }
};

// Function to handle redirecting to login
const goToLogin = () => {
  authStore.clearTenantSelectionInfo(); // Clear state before going back
  router.push({ name: 'Signin' }); // Assuming 'Signin' is the name of your login route
};

</script>

<style scoped>
/* Add any specific styles if needed */
</style> 