import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/api/auth/login/', credentials)
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('token', this.token)
      } catch (error) {
        throw error
      }
    },

    async logout() {
      try {
        await axios.post('/api/auth/logout/')
        this.token = null
        this.user = null
        localStorage.removeItem('token')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },

    async fetchUser() {
      try {
        const response = await axios.get('/api/auth/user/')
        this.user = response.data
      } catch (error) {
        throw error
      }
    },

    async updateProfile(profileData) {
      try {
        const response = await axios.patch('/api/auth/profile/', profileData)
        this.user = {
          ...this.user,
          firstName: profileData.firstName,
          lastName: profileData.lastName,
          profile: {
            ...this.user.profile,
            phoneNumber: profileData.phoneNumber
          }
        }
        return response.data
      } catch (error) {
        throw error
      }
    },

    initializeFromStorage() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        this.fetchUser()
      }
    }
  }
}) 