<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0f172a] text-white">
    <div class="flex flex-col lg:flex-row items-center gap-10 px-6 py-12 w-full max-w-6xl">
      <!-- Login Box -->
      <div class="bg-[#1e293b] rounded-xl p-10 w-full max-w-md shadow-lg">
        <div class="flex flex-col items-center">
          <h2 class="text-2xl font-bold mb-1">Welcome</h2>
          <p class="text-sm text-gray-400 mb-8">
            Sign in to access your account
          </p>
        </div>

        <!-- Kinde Sign In Button -->
        <button
          @click="redirectToKinde"
          type="button"
          class="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-md text-lg font-semibold transition flex items-center justify-center gap-2"
        >
          <!-- Optional: Add Kinde logo or generic login icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          Sign In / Sign Up
        </button>

        <!-- Removed Email/Password Form, Social Buttons, etc. -->

      </div>

      <!-- Right Side Image -->
      <div class="hidden lg:block">
        <img
          :src="loginImg"
          alt="Login Illustration"
          class="w-[1000px] max-w-full"
        />
      </div>
    </div>
  </div>
</template>

<script>
// Removed axios and apiClient imports as they are no longer needed here
import loginImg from '@/assets/103.png'
// Removed useAuthStore import - login state is handled by Kinde redirect and backend session

export default {
  name: 'LoginPage',
  data() {
    return {
      loginImg,
      // Removed email, password, error data properties
    }
  },
  methods: {
    redirectToKinde() {
      // Construct the absolute URL to the backend login endpoint
      // Use an environment variable for the backend base URL in production
      const backendBaseUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'; 
      const backendLoginUrl = `${backendBaseUrl}/auth/login/`;
      
      // Redirect the user's browser
      window.location.href = backendLoginUrl;
    }
    // Removed handleLogin method
  }
}
</script>



