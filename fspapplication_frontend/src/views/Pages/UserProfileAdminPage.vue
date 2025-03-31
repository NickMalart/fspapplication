<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
      {{ error }}
    </div>
    <div v-else-if="!userProfile" class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-600">
      No user profile data found for ID: {{ userId }}
    </div>
    <div v-else class="space-y-6">
      <UserAvatarSectionAdmin 
        :userId="userId" 
        :user="userProfile" 
        @update:user="handleUserUpdate"
      />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useUserProfileAdminStore } from "@/stores/userProfileAdminStore";
import type { UserProfileAdmin } from "@/stores/userProfileAdminStore";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserAvatarSectionAdmin from '@/components/administration/accounts/UserAvatarSectionAdmin.vue';

const route = useRoute();
const userId = computed(() => route.params.id as string);
const currentPageTitle = ref('User Profile Administration');
const userProfileAdminStore = useUserProfileAdminStore();
const loading = computed(() => userProfileAdminStore.loading);
const error = computed(() => userProfileAdminStore.error);
const userProfile = computed(() => userProfileAdminStore.currentUser);

// Handle updates from the avatar component
const handleUserUpdate = (updatedUser: UserProfileAdmin) => {
  // Update the store's currentUser directly without a full refresh
  if (updatedUser) {
    userProfileAdminStore.$patch({ currentUser: updatedUser });
  }
};

onMounted(async () => {
  if (userId.value) {
    await userProfileAdminStore.fetchUserProfile(userId.value);
  }
});
</script> 