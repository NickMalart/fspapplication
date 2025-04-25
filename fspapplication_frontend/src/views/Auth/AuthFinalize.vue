<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0f172a] text-white">
    <div class="text-center">
      <h2 class="text-2xl font-bold mb-4">Finalizing Authentication...</h2>
      <p v-if="errorMessage" class="text-red-400 mb-4">{{ errorMessage }}</p>
      <p v-else class="text-gray-400">Please wait while we securely log you in.</p>
      <!-- Optional: Add a loading spinner here -->
       <button 
         v-if="errorMessage" 
         @click="goToLogin"
         class="mt-4 mx-auto block px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md text-sm font-semibold transition"
       >
         Return to Login
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { apiClient } from '@/service/api'; // Import the configured apiClient

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const errorMessage = ref<string | null>(null);

onMounted(async () => {
  const token = route.query.token as string | undefined;

  console.log('AuthFinalize mounted. Token from query:', token);

  if (!token) {
    errorMessage.value = 'Authentication token missing. Please try logging in again.';
    console.error('Finalization failed: Token missing from URL query parameters.');
    return;
  }

  try {
    // 1. Call the actual backend API to finalize authentication
    console.log(`Calling finalize API with token: ${token}`);
    const response = await apiClient.get('/account/auth/finalize/', { // Use the correct path relative to baseURL '/api'
        params: { token } // Pass token as query parameter
    });

    const apiResponse = response.data; // Axios puts response data in .data
    console.log('API call successful. Response:', apiResponse);
    
    // Check for expected fields in the response (using camelCase keys)
    if (!apiResponse.accessToken || !apiResponse.refreshToken || !apiResponse.user || !apiResponse.tenantSchemaName) {
        throw new Error('Incomplete data received from finalization API.');
    }
    
    // 2. Store the final token, user details, and tenant in the auth store (using camelCase keys)
    authStore.setToken({ 
      access: apiResponse.accessToken, 
      refresh: apiResponse.refreshToken 
    });
    authStore.setUser(apiResponse.user); // Assuming user object structure matches store expectation
    authStore.setTenant(apiResponse.tenantSchemaName); 

    // 3. Redirect to the dashboard or intended page
    console.log('Authentication successful. Redirecting to dashboard...');
    router.push({ name: 'Dashboard' }); // Adjust route name if needed

  } catch (error: any) {
    console.error('Error during authentication finalization:', error);
    // Extract more specific error from Axios if available
    const backendError = error.response?.data?.error || error.message || 'An unknown error occurred.';
    errorMessage.value = `Login failed: ${backendError}. Please try again.`;
    // Optionally clear any partial auth state
    authStore.removeToken(); 
  }
});

const goToLogin = () => {
  authStore.removeToken();
  // Redirect to the main domain's login page explicitly
  const publicHostname = 'localhost'; 
  const port = window.location.port ? `:${window.location.port}` : '';
  const publicLoginUrl = `${window.location.protocol}//${publicHostname}${port}/`;
  window.location.href = publicLoginUrl;
};

</script>

<style scoped>
/* Add any specific styles if needed */
</style> 