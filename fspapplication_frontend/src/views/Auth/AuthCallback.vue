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

  // 1. Parse the URL fragment
  const hash = window.location.hash.substring(1); // Remove the leading #
  const params = new URLSearchParams(hash);

  const accessToken = params.get('access_token');
  const refreshToken = params.get('refresh_token');
  const tenantSchemaName = params.get('tenant_schema_name'); // Optional: get tenant if needed

  // 2. Check if tokens exist
  if (accessToken && refreshToken) {
    // 3. Update the auth store
    authStore.setToken({ access: accessToken, refresh: refreshToken });

    // 4. Set tenant (optional, if you need it in the store)
    if (tenantSchemaName) {
      authStore.setTenant(tenantSchemaName);
    }

    router.push('/dashboard'); 
  } else {
    router.push('/login'); // Or a dedicated error page
  }
});
</script> 