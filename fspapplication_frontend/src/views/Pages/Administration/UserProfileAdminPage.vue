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
      <UserPersonalInformationAdminCard
        :userData="userProfile"
        :loading="loading"
        :error="error || ''"
        @update:user="handleUserUpdate"
      />
      <UserAddressAdminCard
        :userData="userProfile"
        :loading="loading"
        :error="error || ''"
        @update:user="handleUserUpdate"
      />
      <UserEmergencyContactAdminCard
        :userData="userProfile"
        :loading="loading"
        :error="error || ''"
        @update:user="handleUserUpdate"
      />
      <UserTypeProfileAdminCard
        :userData="userProfile"
        :loading="loading"
        :error="error || ''"
        @update:user="handleUserUpdate"
      />
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onActivated, watch } from "vue";
import { useRoute } from "vue-router";
import { useUserProfileAdminStore } from "@/stores/userProfileAdminStore";
import type { UserProfileAdmin } from "@/stores/userProfileAdminStore";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserAvatarSectionAdmin from '@/components/administration/accounts/UserAvatarSectionAdmin.vue';
import UserPersonalInformationAdminCard from '@/components/administration/accounts/UserPersonalInformationAdminCard.vue';
import UserAddressAdminCard from '@/components/administration/accounts/UserAddressAdminCard.vue';
import UserEmergencyContactAdminCard from "@/components/administration/accounts/UserEmergencyContactAdminCard.vue";
import UserTypeProfileAdminCard from "@/components/administration/accounts/UserTypeProfileAdminCard.vue";
import { convertObjectKeysToCamel } from "@/utils/caseConverter";
import { useUserStore } from "@/stores/userProfileStore";


const route = useRoute();
const userId = computed(() => route.params.id as string);
const currentPageTitle = ref('User Profile Administration');
const userProfileAdminStore = useUserProfileAdminStore();
const loading = computed(() => userProfileAdminStore.loading);
const error = computed(() => userProfileAdminStore.error);
const userProfile = computed(() => userProfileAdminStore.currentUser);

// Get the main user store instance
const userStore = useUserStore();

// Handle updates from the avatar component
const handleUserUpdate = (updatedUser: UserProfileAdmin) => {
  // Update the store's currentUser directly without a full refresh
  if (updatedUser) {
    userProfileAdminStore.$patch({ currentUser: updatedUser });

    // Also update the main user store if the updated user is the logged-in user
    const loggedInUserId = userStore.completeUser?.id;
    if (loggedInUserId && updatedUser.id === loggedInUserId) {
      userStore.$patch({ completeUser: updatedUser as any }); 
    }
  }
};

// Function to fetch user profile data
const fetchUserData = async () => {
  if (userId.value) {
    await userProfileAdminStore.fetchUserProfile(userId.value);
  }
};

// Initial data fetch on component mount
onMounted(fetchUserData);

// Watch for route changes to refresh data when navigating to this page
watch(
  () => route.fullPath,
  (newPath) => {
    // Check if the new path is for the admin user profile page
    if (newPath.includes('/admin/users/') && newPath.includes('/profile')) {
      fetchUserData();
    }
  }
);

// Also watch for userId changes (in case of switching between different user profiles)
watch(
  () => userId.value,
  (newUserId, oldUserId) => {
    if (newUserId && newUserId !== oldUserId) {
      fetchUserData();
    }
  }
);

// For Vue 3 kept-alive components
onActivated(fetchUserData);
</script> 