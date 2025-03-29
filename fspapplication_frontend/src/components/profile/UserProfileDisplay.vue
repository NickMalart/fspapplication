<template>
    <div class="bg-white shadow-md rounded-lg p-6">
      <h1 class="text-2xl font-bold mb-6">User Profile</h1>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center my-4">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {{ error }}
      </div>
      
      <!-- Data Display -->
      <div v-else-if="profile" class="space-y-6">
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold mb-2">Personal Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Phone Number</p>
              <p>{{ profile.phone_number || 'Not provided' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Date of Birth</p>
              <p>{{ profile.date_of_birth || 'Not provided' }}</p>
            </div>
          </div>
        </div>
        
        <div class="border-b pb-4">
          <h2 class="text-xl font-semibold mb-2">Address</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Street</p>
              <p>{{ formatAddress() }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">City/Suburb</p>
              <p>{{ profile.suburb || 'Not provided' }}, {{ profile.city || '' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">State/Postal Code</p>
              <p>{{ profile.state || 'Not provided' }} {{ profile.postal_code || '' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Country</p>
              <p>{{ profile.country || 'Not provided' }}</p>
            </div>
          </div>
        </div>
        
        <div>
          <h2 class="text-xl font-semibold mb-2">Emergency Contact</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Name</p>
              <p>{{ formatEmergencyName() }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Contact Number</p>
              <p>{{ profile.emergency_contact || 'Not provided' }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- No Data State -->
      <div v-else class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
        No profile data available.
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    name: 'UserProfileDisplay',
    setup() {
      const profile = ref(null);
      const loading = ref(false);
      const error = ref(null);
      
      const fetchProfile = async () => {
        loading.value = true;
        error.value = null;
        
        try {
          // Get the JWT token from localStorage
          const token = localStorage.getItem('token');
          
          // Make the API call with the authorization header
          const response = await axios.get('/api/account/user/profile/', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          profile.value = response.data;
        } catch (err) {
          console.error('Error fetching profile:', err);
        } finally {
          loading.value = false;
        }
      };
      
      const formatAddress = () => {
        if (!profile.value) return 'Not provided';
        
        const { street_number, street_name } = profile.value;
        if (street_number && street_name) {
          return `${street_number} ${street_name}`;
        }
        return street_name || street_number || 'Not provided';
      };
      
      const formatEmergencyName = () => {
        if (!profile.value) return 'Not provided';
        
        const { emergency_contact_first_name, emergency_contact_last_name } = profile.value;
        if (emergency_contact_first_name && emergency_contact_last_name) {
          return `${emergency_contact_first_name} ${emergency_contact_last_name}`;
        }
        return emergency_contact_first_name || emergency_contact_last_name || 'Not provided';
      };
      
      onMounted(() => {
        fetchProfile();
      });
      
      return {
        profile,
        loading,
        error,
        formatAddress,
        formatEmergencyName
      };
    }
  });
  </script>