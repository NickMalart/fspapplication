import { defineStore } from 'pinia'
import axios from 'axios'
import { configureApi } from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    accessToken: '',
    refreshToken: '',
    tenant: '',
    user: {
      id: null as string | null,
      email: '',
    },
  }),

  actions: {
    init() {
      this.accessToken = localStorage.getItem('auth.access') || ''
      this.refreshToken = localStorage.getItem('auth.refresh') || ''
      this.tenant = localStorage.getItem('auth.tenant') || ''
      this.user.id = localStorage.getItem('auth.user.id')
      this.user.email = localStorage.getItem('auth.user.email') || ''
      
      this.isAuthenticated = !!this.accessToken && !!this.refreshToken
      
      configureApi()
      
      if (this.tenant) {
        axios.defaults.headers.common['X-DTS-TENANT'] = this.tenant
      }
      
      if (this.accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
      }
    },

    setToken(data: { access: string; refresh: string }) {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.isAuthenticated = true
      localStorage.setItem('auth.access', data.access)
      localStorage.setItem('auth.refresh', data.refresh)
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    },

    setTenant(tenant: string) {
      this.tenant = tenant
      localStorage.setItem('auth.tenant', tenant)
      axios.defaults.headers.common['X-DTS-TENANT'] = tenant
    },

    setUser(backendUser: { id: string, email: string }) {
      console.log('Raw backend user data:', backendUser)
      
      this.user = {
        id: backendUser.id,
        email: backendUser.email,
      }
      
      console.log('Final user state:', this.user)
      
      localStorage.setItem('auth.user.id', this.user.id || '')
      localStorage.setItem('auth.user.email', this.user.email)
    },

    removeToken() {
      this.accessToken = ''
      this.refreshToken = ''
      this.tenant = ''
      this.isAuthenticated = false
      this.user = {
        id: null,
        email: '',
      }

      localStorage.removeItem('auth.access')
      localStorage.removeItem('auth.refresh')
      localStorage.removeItem('auth.tenant')
      localStorage.removeItem('auth.user.id')
      localStorage.removeItem('auth.user.email')
      localStorage.removeItem('auth.user.profile')
      
      // Clear headers
      delete axios.defaults.headers.common['Authorization']
      delete axios.defaults.headers.common['X-DTS-TENANT']
    },

    refreshTokenAction() {
      axios
        .post('/api/account/refresh/', { refresh: this.refreshToken })
        .then((res) => {
          this.accessToken = res.data.access
          localStorage.setItem('auth.access', res.data.access)
          axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
        })
        .catch((err) => {
          console.error(err)
          this.removeToken()
        })
    },
  },
})
