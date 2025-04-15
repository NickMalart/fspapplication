<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
      {{ error }}
    </div>
    <div v-else class="space-y-6">
      <UserAvatarSection :user="userProfile" />
      <UserPersonalInformationCard :user="userProfile" />
      <UserAddressCard :user="userProfile" />
      <UserEmergencyContactCard :user="userProfile" />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import { useUserStore } from "@/stores/userProfileStore";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserAvatarSection from '@/components/userSettings/profile/UserAvatarSection.vue';
import UserPersonalInformationCard from '@/components/userSettings/profile/UserPersonalInformationCard.vue';
import UserAddressCard from '@/components/userSettings/profile/UserAddressCard.vue';
import UserEmergencyContactCard from '@/components/userSettings/profile/UserEmergencyContactCard.vue';

const currentPageTitle = ref('User Profile');
const userStore = useUserStore();
const loading = computed(() => userStore.loading);
const error = computed(() => userStore.error);
const userProfile = computed(() => userStore.completeUser);

// Function to fetch user profile data  
const fetchUserData = async () => {
  await userStore.fetchUserProfile();
};

// Function to force refresh data
const forceRefresh = async () => {
  userStore.$patch({ completeUser: null });
  await fetchUserData();
};

// Initial data fetch on component mount
onMounted(() => {
  // Perform initial data fetch
  forceRefresh();
  
  // Expose forceRefresh globally so it can be called from sidebar
  window.forceProfileRefresh = forceRefresh;
});

// Clean up handlers on unmount
onBeforeUnmount(() => {
  // Remove global function
  delete window.forceProfileRefresh;
});
</script>
