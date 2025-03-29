import './assets/main.css'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'jsvectormap/dist/jsvectormap.css'
import 'flatpickr/dist/flatpickr.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
import { configureApi } from './utils/api'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia) 
app.use(router)
app.use(VueApexCharts)

import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()

// Configure API with base URL and tenant headers
configureApi()

// Import axios after configuration
import axios from 'axios'

// Set up axios interceptors
axios.interceptors.request.use(
  (config) => {
    const token = auth.accessToken
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add tenant header to all requests
    const tenant = auth.tenant
    if (tenant) {
      config.headers['X-DTS-TENANT'] = tenant
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        await auth.refreshTokenAction()
        
        originalRequest.headers.Authorization = `Bearer ${auth.accessToken}`
        return axios(originalRequest)
      } catch (refreshError) {
        auth.removeToken()
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

app.mount('#app')
