import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    accessToken: '',
    refreshToken: '',
    user: {
      id: null as string | null,
      first_name: '',
      last_name: '',
      email: '',
    },
  }),

  actions: {
    init() {
      this.accessToken = localStorage.getItem('auth.access') || ''
      this.refreshToken = localStorage.getItem('auth.refresh') || ''
      this.user.id = localStorage.getItem('auth.user.id')
      this.user.first_name = localStorage.getItem('auth.user.first_name') || ''
      this.user.last_name = localStorage.getItem('auth.user.last_name') || ''
      this.user.email = localStorage.getItem('auth.user.email') || ''

      this.isAuthenticated = !!this.accessToken && !!this.refreshToken
    },

    setToken(data: { access: string; refresh: string }) {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.isAuthenticated = true
      localStorage.setItem('auth.access', data.access)
      localStorage.setItem('auth.refresh', data.refresh)
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    },

    setUser(user: { id: string | null; first_name: string; last_name: string; email: string }) {
      this.user = user
      localStorage.setItem('auth.user.id', user.id || '')
      localStorage.setItem('auth.user.first_name', user.first_name)
      localStorage.setItem('auth.user.last_name', user.last_name)
      localStorage.setItem('auth.user.email', user.email)
    },

    removeToken() {
      this.accessToken = ''
      this.refreshToken = ''
      this.isAuthenticated = false
      this.user = {
        id: null,
        first_name: '',
        last_name: '',
        email: '',
      }

      localStorage.removeItem('auth.access')
      localStorage.removeItem('auth.refresh')
      localStorage.removeItem('auth.user.id')
      localStorage.removeItem('auth.user.first_name')
      localStorage.removeItem('auth.user.last_name')
      localStorage.removeItem('auth.user.email')
    },

    refreshTokenAction() {
      axios
        .post('/api/refresh/', { refresh: this.refreshToken })
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
