<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div class="space-y-6">
      <UserPersonalInformationCard />
      <UserProfileDisplay />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserPersonalInformationCard from '@/components/profile/UserPersonalInformationCard.vue';
import UserProfileDisplay from '@/components/profile/UserProfileDisplay.vue';

const currentPageTitle = ref('User Profile');
</script>
