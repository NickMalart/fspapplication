<template>
  <AdminLayout>
    <PageBreadcrumb :pageTitle="currentPageTitle" />
    <div class="space-y-6">
      <UserAvatarSection />
      <UserPersonalInformationCard />
      <UserAddressCard />
      <UserEmergencyContactCard />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref } from "vue";
import AdminLayout from "@/components/layout/AdminLayout.vue";
import PageBreadcrumb from "@/components/common/PageBreadcrumb.vue";
import UserAvatarSection from '@/components/profile/UserAvatarSection.vue';
import UserPersonalInformationCard from '@/components/profile/UserPersonalInformationCard.vue';
import UserAddressCard from '@/components/profile/UserAddressCard.vue';
import UserEmergencyContactCard from '@/components/profile/UserEmergencyContactCard.vue';

const currentPageTitle = ref('User Profile');
</script>
