<template>
    <AdminLayout>
      <PageBreadcrumb :pageTitle="currentPageTitle" />
      <div
        class="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12"
      >
        <div class="mx-auto w-full max-w-[630px] text-center">
          <h3
            class="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl"
          >
            User Accounts
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 sm:text-base">
            Below is the list of user accounts currently available.
          </p>
        </div>
        <DataTable :data="users" />
      </div>
    </AdminLayout>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import AdminLayout from "@/components/layout/AdminLayout.vue";
  import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
  import DataTable from "@/components/common/DataTable.vue";
  import axios from "axios";
  
  const currentPageTitle = ref("Accounts Page");
  const users = ref([]);
  
  onMounted(async () => {
    try {
      const response = await axios.get('/api/users/');
      users.value = response.data;
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  });
  </script>
  
  <style></style>
  