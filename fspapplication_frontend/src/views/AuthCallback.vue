<template>
  <div class="flex h-screen items-center justify-center">
    <div class="text-center">
      <p class="text-lg font-semibold text-gray-700 dark:text-gray-300">Processing authentication...</p>
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Please wait while we securely log you in.</p>
      <!-- Optional: Add a spinner here -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; // Assuming your auth store path

const router = useRouter();
const authStore = useAuthStore();

onMounted(() => {
  console.log('AuthCallback mounted. Hash:', window.location.hash);

  // 1. Parse the URL fragment
  const hash = window.location.hash.substring(1); // Remove the leading #
  const params = new URLSearchParams(hash);

  const accessToken = params.get('access_token');
  const refreshToken = params.get('refresh_token');
  const tenantSchemaName = params.get('tenant_schema_name'); // Optional: get tenant if needed

  console.log('Parsed Access Token:', accessToken ? accessToken.substring(0, 10) + '...' : 'null');
  console.log('Parsed Refresh Token:', refreshToken ? refreshToken.substring(0, 10) + '...' : 'null');
  console.log('Parsed Tenant Schema:', tenantSchemaName);

  // 2. Check if tokens exist
  if (accessToken && refreshToken) {
    // 3. Update the auth store
    authStore.setToken({ access: accessToken, refresh: refreshToken });
    console.log('Tokens set in auth store.');

    // 4. Set tenant (optional, if you need it in the store)
    if (tenantSchemaName) {
      authStore.setTenant(tenantSchemaName);
      console.log('Tenant set in auth store.');
    }
    
    // Store user info if needed - Requires another API call usually
    // Consider fetching user info after redirect or add it to backend callback response
    // Example: await authStore.fetchUser(); 

    // 5. Redirect to dashboard (or intended page)
    console.log('Redirecting to /dashboard...');
    router.push('/dashboard'); 
  } else {
    // Handle error: Tokens not found in URL
    console.error('Authentication callback error: Tokens not found in URL fragment.');
    // Redirect to login or an error page
    router.push('/login'); // Or a dedicated error page
  }
});
</script> 