<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0f172a] text-white">
    <div class="flex flex-col lg:flex-row items-center gap-10 px-6 py-12 w-full max-w-6xl">
      <!-- Login Box -->
      <div class="bg-[#1e293b] rounded-xl p-10 w-full max-w-md shadow-lg">
        <div class="flex flex-col items-center">
          <img
            src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600"
            alt="Flowbite"
            class="h-10 mb-4"
          />
          <h2 class="text-2xl font-bold mb-1">Welcome back</h2>
          <p class="text-sm text-gray-400">
            Please log into your account @ **Company Name Place Holder**
          </p>
        </div>

        <!-- Email Field -->
        <form @submit.prevent="handleLogin" class="mt-8 space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="name@company.com"
              required
              class="w-full rounded-md bg-gray-700 border border-gray-600 px-4 py-2 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          <!-- Password Field -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-1">Password</label>
            <input
              v-model="password"
              type="password"
              placeholder="••••••••"
              required
              class="w-full rounded-md bg-gray-700 border border-gray-600 px-4 py-2 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          <!-- Remember & Forgot -->
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2">
              <input type="checkbox" class="form-checkbox rounded bg-gray-700 border-gray-600 text-blue-500" />
              Remember me
            </label>
            <a href="#" class="text-blue-400 hover:underline">Forgot password?</a>
          </div>

          <div class="flex items-center justify-center gap-4">
            <hr class="flex-grow border-gray-600" />
            <span class="text-gray-400 text-sm">or</span>
            <hr class="flex-grow border-gray-600" />
          </div>

          <!-- Google Sign In -->
          <button
            type="button"
            class="flex items-center justify-center gap-2 w-full px-4 py-2 border border-gray-600 rounded-md text-sm bg-gray-800 hover:bg-gray-700"
          >
            <img src="https://www.svgrepo.com/show/475656/google-color.svg" class="h-5 w-5" alt="Google" />
            Sign in with Google
          </button>

          <!-- Apple Sign In -->
          <button
            type="button"
            class="flex items-center justify-center gap-2 w-full px-4 py-2 border border-gray-600 rounded-md text-sm bg-gray-800 hover:bg-gray-700"
          >
            <img src="https://www.svgrepo.com/show/452255/apple.svg" class="h-5 w-5 invert" alt="Apple" />
            Sign in with Apple
          </button>

          <button
            type="submit"
            class="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-md text-sm font-semibold transition"
          >
            Sign in to your account
          </button>
        </form>
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
import axios from 'axios'
import apiClient from '@/service/api'
import loginImg from '@/assets/103.png'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      loginImg,
      error: null,
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      const auth = useAuthStore()  

      try {
        // Extract tenant from hostname
        const hostname = window.location.hostname
        const tenant = hostname.split('.')[0]
        
        // Setup axios defaults temporarily for the login request ONLY 
        // (Ideally, login should also use apiClient, but requires modifying backend potentially
        // if it doesn't expect standard Auth Bearer for login itself)
        axios.defaults.headers.common["X-DTS-TENANT"] = tenant
        
        // Use global axios for login POST for now
        const response = await axios.post(`/api/account/login/`, { 
          email: this.email,
          password: this.password,
        })
        
        // Clean up temporary header setting
        delete axios.defaults.headers.common["X-DTS-TENANT"]

        console.log('Login response:', response.data)
        auth.setToken({
          access: response.data.access,
          refresh: response.data.refresh
        })
        
        auth.setTenant(tenant)

        // Use apiClient for the user request - interceptors will add headers
        const userResponse = await apiClient.get(`account/user/`) 
        console.log('Raw user response data:', userResponse.data)
        console.log('User data before conversion:', userResponse.data)
        auth.setUser(userResponse.data)
        console.log('User data after conversion:', auth.user)

        alert('✅ Login successful!')
        this.$router.push('/dashboard')
      } catch (error) {
        // Clean up temporary header setting in case of error during login POST
        delete axios.defaults.headers.common["X-DTS-TENANT"]
        
        if (axios.isAxiosError(error)) { // Type check error
          if (error.response) {
            // Handle specific error codes if needed
            this.error = error.response.data.detail || 'Login failed. Please check credentials.';
            if (error.response.status === 404 && error.config?.url?.includes('login')) {
                this.error = "Login endpoint not found or invalid tenant.";
            }
          } else if (error.request) {
            // Network error (no response received)
             this.error = 'Server is not responding. Check network or try again later.';
          } else {
            // Other errors (e.g., setting up the request)
            this.error = 'An unexpected error occurred during login setup.';
          }
        } else {
           // Non-Axios error
           this.error = 'An unexpected error occurred.';
        }
        console.error('❌ Login error →', error)
        alert(`❌ ${this.error}`)
      }
    }
  }
}
</script>



