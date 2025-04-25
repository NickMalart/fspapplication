<template>
  <div class="flex h-screen items-center justify-center bg-[#0f172a]">
    <div class="text-center p-6 bg-[#1e293b] rounded-lg shadow-xl">
      <p class="text-lg font-semibold text-gray-200">Processing authentication...</p>
      <p v-if="!errorMessage" class="mt-2 text-sm text-gray-400">Please wait while we securely log you in.</p>
      <!-- Basic Spinner -->
      <svg v-if="!errorMessage" class="animate-spin h-8 w-8 text-blue-500 mx-auto mt-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p v-if="errorMessage" class="mt-4 text-sm text-red-400">{{ errorMessage }}</p>
      <button 
        v-if="errorMessage" 
        @click="goToLogin"
        class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-semibold transition"
      >
        Return to Login
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Assuming your auth store path

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const errorMessage = ref<string | null>(null);

// Function to handle redirecting to login
const goToLogin = () => {
  router.push({ name: 'Signin' }); // Assuming 'Signin' is the name of your login route
};

onMounted(() => {
  console.log('AuthCallback mounted. Processing redirect from backend...');

  // --- Read data from URL query parameters ---
  const status = route.query.status as string | undefined;
  const tempToken = route.query.temp_token as string | undefined;
  const tenantsJson = route.query.tenants as string | undefined;
  const errorParam = route.query.error as string | undefined; // Check for errors passed from backend redirect

  console.log('Query Params:', { status, tempToken, tenantsJson, errorParam });

  // Handle potential errors passed from backend
  if (errorParam) {
      errorMessage.value = `Authentication failed: ${errorParam}. Please try again or contact support.`;
      console.error('Error received from backend redirect:', errorParam);
      // setTimeout(goToLogin, 5000);
      return;
  }

  // Process based on status
  try {
    switch (status) {
      case 'select_tenant':
        if (!tempToken || !tenantsJson) {
          throw new Error('Missing tenant list or temporary token in redirect parameters.');
        }
        // Parse the JSON string back into an array
        const tenants = JSON.parse(tenantsJson);

        console.log('Status: select_tenant. Storing temp token and tenants, redirecting to selection.');
        authStore.setTenantSelectionInfo(tenants, tempToken);
        router.push('/select-tenant');
        break;

      // Add cases here if backend could redirect with other statuses (e.g., 'success' if only 1 tenant)
      // case 'success':
      //   const accessToken = route.query.access_token as string | undefined;
      //   const refreshToken = route.query.refresh_token as string | undefined;
      //   const tenantSchema = route.query.tenant_schema_name as string | undefined;
      //   if (!accessToken || !refreshToken) throw new Error('Missing tokens in redirect.');
      //   console.log('Status: success. Storing tokens and redirecting to dashboard.');
      //   authStore.setToken({ access: accessToken, refresh: refreshToken });
      //   if (tenantSchema) authStore.setTenant(tenantSchema);
      //   router.push('/dashboard');
      //   break;

      default:
        throw new Error(`Unexpected status received in redirect: ${status || 'missing'}`);
    }
  } catch (error) {
      console.error('Error processing redirect parameters:', error);
      // Try to decode JSON parsing errors specifically
      if (error instanceof SyntaxError && tenantsJson) {
           errorMessage.value = 'Failed to parse tenant data from redirect. Please try again.';
      } else {
          errorMessage.value = error instanceof Error ? error.message : 'An unexpected error occurred processing login. Please try again.';
      }
      // setTimeout(goToLogin, 5000);
  }
});
</script>

<style scoped>
/* Add styles for the spinner if needed */
</style> 