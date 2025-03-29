<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <UserProfileDisplay />
  </AdminLayout>
</template>

<script setup>
import { ref } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserProfileDisplay from '@/components/profile/UserProfileDisplay.vue';

const currentPageTitle = ref('User Profile');
</script>
