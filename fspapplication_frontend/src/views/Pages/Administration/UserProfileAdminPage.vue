<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div class="rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
      <!-- Loading State -->
      <div v-if="loading" class="p-6 text-center">
        <div class="animate-pulse">
          <div class="h-8 bg-gray-200 rounded w-1/4 mx-auto mb-4"></div>
          <div class="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="p-6 text-center text-red-600 dark:text-red-400">
        {{ error }}
      </div>

      <!-- User Profile Content -->
      <div v-else-if="userData" class="p-5 lg:p-7">
        <div class="flex flex-col gap-6">
          <!-- Basic Info Section -->
          <div class="border-b border-gray-200 dark:border-gray-700 pb-6">
            <div class="flex flex-col items-center lg:flex-row lg:items-start gap-6">
              <div class="w-24 h-24 rounded-full overflow-hidden border-2 border-gray-200 dark:border-gray-700">
                <img 
                  :src="userData.avatar || `https://ui-avatars.com/api/?name=${userData.firstName}+${userData.lastName}&background=0D8ABC&color=fff&size=100`" 
                  :alt="userData.fullName"
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="flex-1 text-center lg:text-left">
                <h1 class="text-2xl font-semibold text-gray-800 dark:text-white/90 mb-2">
                  {{ userData.firstName }} {{ userData.lastName }}
                </h1>
                <p class="text-gray-500 dark:text-gray-400 mb-4">{{ userData.email }}</p>
                <div class="flex flex-wrap gap-3 justify-center lg:justify-start">
                  <span 
                    :class="[
                      'px-3 py-1 rounded-full text-sm font-medium',
                      userData.is_active 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-400' 
                        : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-400'
                    ]"
                  >
                    {{ userData.is_active ? 'Active' : 'Inactive' }}
                  </span>
                  <span class="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-400">
                    {{ userData.userType }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Job Details Section -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="p-4 rounded-xl border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-800 dark:text-white/90 mb-4">Job Information</h3>
              <div class="space-y-3">
                <div>
                  <span class="text-sm text-gray-500 dark:text-gray-400">Job Title</span>
                  <p class="text-gray-800 dark:text-white/90">{{ userData.employeeDetails?.jobTitle || 'N/A' }}</p>
                </div>
                <div>
                  <span class="text-sm text-gray-500 dark:text-gray-400">Department</span>
                  <p class="text-gray-800 dark:text-white/90">{{ userData.employeeDetails?.department || 'N/A' }}</p>
                </div>
              </div>
            </div>

            <!-- Groups Section -->
            <div class="p-4 rounded-xl border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-800 dark:text-white/90 mb-4">Groups & Permissions</h3>
              <div class="space-y-3">
                <div v-if="userData.functional_groups?.length">
                  <span class="text-sm text-gray-500 dark:text-gray-400">Functional Groups</span>
                  <div class="flex flex-wrap gap-2 mt-2">
                    <span 
                      v-for="group in userData.functional_groups" 
                      :key="group.id"
                      class="px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
                    >
                      {{ group.name }}
                    </span>
                  </div>
                </div>
                <div v-else>
                  <p class="text-gray-500 dark:text-gray-400">No groups assigned</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";

const route = useRoute();
const currentPageTitle = ref("User Profile");
const userData = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchUserData = async () => {
  try {
    loading.value = true;
    error.value = null;
    const response = await axios.get(`/api/account/users/${route.params.id}/`);
    userData.value = response.data;
    currentPageTitle.value = `${response.data.firstName} ${response.data.lastName}'s Profile`;
  } catch (err) {
    console.error('Error fetching user data:', err);
    error.value = 'Failed to load user profile. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUserData);
</script>

<style></style>
  