import { defineStore } from 'pinia'
import axios from 'axios'

interface UserProfile {
  phoneNumber: string
  country: string
  city: string
  state: string
  postalCode: string
  addressLine1: string
  addressLine2: string
  latitude: number | null
  longitude: number | null
  emergencyContact: string
  emergencyContactFirstName: string
  emergencyContactLastName: string
}

interface User {
  id: string | null
  firstName: string
  lastName: string
  email: string
  profile?: Partial<UserProfile>
}

// This function will still be useful for other API responses
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (g) => g[1].toUpperCase())
}

function convertKeys(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(v => convertKeys(v))
  } else if (obj !== null && obj.constructor === Object) {
    return Object.keys(obj).reduce(
      (result, key) => ({
        ...result,
        [toCamelCase(key)]: convertKeys(obj[key])
      }),
      {}
    )
  }
  return obj
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    accessToken: '',
    refreshToken: '',
    user: {
      id: null as string | null,
      firstName: '',
      lastName: '',
      email: '',
      profile: {
        phoneNumber: '',
        country: '',
        city: '',
        state: '',
        postalCode: '',
        addressLine1: '',
        addressLine2: '',
        latitude: null as number | null,
        longitude: null as number | null,
        emergencyContact: '',
        emergencyContactFirstName: '',
        emergencyContactLastName: '',
      } as UserProfile
    },
  }),

  actions: {
    init() {
      this.accessToken = localStorage.getItem('auth.access') || ''
      this.refreshToken = localStorage.getItem('auth.refresh') || ''
      this.user.id = localStorage.getItem('auth.user.id')
      this.user.firstName = localStorage.getItem('auth.user.firstName') || ''
      this.user.lastName = localStorage.getItem('auth.user.lastName') || ''
      this.user.email = localStorage.getItem('auth.user.email') || ''
      
      // Load profile from localStorage if available
      const savedProfile = localStorage.getItem('auth.user.profile')
      if (savedProfile) {
        try {
          this.user.profile = JSON.parse(savedProfile)
        } catch (e) {
          console.error('Failed to parse saved profile data', e)
        }
      }

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

    setUser(backendUser: Record<string, any>) {
      // The backend now returns camelCase, so we can directly use the data
      // However, we keep convertKeys for backward compatibility or other APIs
      const userData = backendUser as User
      
      this.user = {
        id: userData.id,
        firstName: userData.firstName,
        lastName: userData.lastName,
        email: userData.email,
        profile: {
          phoneNumber: userData.profile?.phoneNumber || '',
          country: userData.profile?.country || '',
          city: userData.profile?.city || '',
          state: userData.profile?.state || '',
          postalCode: userData.profile?.postalCode || '',
          addressLine1: userData.profile?.addressLine1 || '',
          addressLine2: userData.profile?.addressLine2 || '',
          latitude: userData.profile?.latitude || null,
          longitude: userData.profile?.longitude || null,
          emergencyContact: userData.profile?.emergencyContact || '',
          emergencyContactFirstName: userData.profile?.emergencyContactFirstName || '',
          emergencyContactLastName: userData.profile?.emergencyContactLastName || '',
        }
      }
      
      localStorage.setItem('auth.user.id', this.user.id || '')
      localStorage.setItem('auth.user.firstName', this.user.firstName)
      localStorage.setItem('auth.user.lastName', this.user.lastName)
      localStorage.setItem('auth.user.email', this.user.email)
      
      // Store profile data
      if (this.user.profile) {
        localStorage.setItem('auth.user.profile', JSON.stringify(this.user.profile))
      }
    },

    removeToken() {
      this.accessToken = ''
      this.refreshToken = ''
      this.isAuthenticated = false
      this.user = {
        id: null,
        firstName: '',
        lastName: '',
        email: '',
        profile: {
          phoneNumber: '',
          country: '',
          city: '',
          state: '',
          postalCode: '',
          addressLine1: '',
          addressLine2: '',
          latitude: null,
          longitude: null,
          emergencyContact: '',
          emergencyContactFirstName: '',
          emergencyContactLastName: '',
        }
      }

      localStorage.removeItem('auth.access')
      localStorage.removeItem('auth.refresh')
      localStorage.removeItem('auth.user.id')
      localStorage.removeItem('auth.user.firstName')
      localStorage.removeItem('auth.user.lastName')
      localStorage.removeItem('auth.user.email')
      localStorage.removeItem('auth.user.profile')
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
