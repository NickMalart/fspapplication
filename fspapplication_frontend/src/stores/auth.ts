import { defineStore } from 'pinia'
// Remove direct axios import here, interceptors will handle headers
// import axios from 'axios' 
// Remove configureApi import if it's only setting axios defaults
// import { configureApi } from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Attempt to initialize state from localStorage on load, but don't rely on it elsewhere
    isAuthenticated: !!localStorage.getItem('auth.access'),
    accessToken: localStorage.getItem('auth.access') || '',
    refreshToken: localStorage.getItem('auth.refresh') || '',
    tenant: localStorage.getItem('auth.tenant') || '',
    user: {
      id: localStorage.getItem('auth.user.id') as string | null,
      email: localStorage.getItem('auth.user.email') || '',
    },
  }),

  actions: {
    // init() action is likely no longer needed as state is initialized above 
    // and interceptors handle headers. Remove it or simplify significantly.
    // init() {
    //   // ... removed logic ...
    // },

    setToken(data: { access: string; refresh: string }) {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.isAuthenticated = true
      // Persist to localStorage for re-hydration on page load
      localStorage.setItem('auth.access', data.access)
      localStorage.setItem('auth.refresh', data.refresh)
      // Remove direct header manipulation
      // axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    },

    setTenant(tenant: string) {
      this.tenant = tenant
      // Persist to localStorage for re-hydration
      localStorage.setItem('auth.tenant', tenant)
      // Remove direct header manipulation
      // axios.defaults.headers.common['X-DTS-TENANT'] = tenant
    },

    setUser(backendUser: { id: string, email: string }) {      
      this.user = {
        id: backendUser.id,
        email: backendUser.email,
      }
      
      
      // Persist to localStorage for re-hydration
      localStorage.setItem('auth.user.id', this.user.id || '')
      localStorage.setItem('auth.user.email', this.user.email)
    },

    removeToken() {
      // Clear state
      this.accessToken = ''
      this.refreshToken = ''
      this.tenant = ''
      this.isAuthenticated = false
      this.user = {
        id: null,
        email: '',
      }

      // Clear persisted data
      localStorage.removeItem('auth.access')
      localStorage.removeItem('auth.refresh')
      localStorage.removeItem('auth.tenant')
      localStorage.removeItem('auth.user.id')
      localStorage.removeItem('auth.user.email')
      // localStorage.removeItem('auth.user.profile') // Uncomment if used
      
      // Remove direct header manipulation (interceptors handle this)
      // delete axios.defaults.headers.common['Authorization']
      // delete axios.defaults.headers.common['X-DTS-TENANT']
      
      // Optional: Redirect to login page after clearing tokens
      // import router from '@/router'; // Import router if needed
      // router.push('/login');
    },

    // Remove the old refreshTokenAction, the interceptor handles this now
    // refreshTokenAction() {
    //   // ... removed logic ...
    // },
  },
})
