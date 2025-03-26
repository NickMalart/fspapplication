// src/composables/auth.ts
import { reactive } from 'vue'
import axios from 'axios'

const auth = reactive({
  isAuthenticated: false,
  accessToken: '',
  refreshToken: '',
  user: {
    id: null as string | null,
    name: '',
    email: '',
  },

  init() {
    // Initialize the auth state from localStorage
    const storedAccess = localStorage.getItem('auth.access')
    const storedRefresh = localStorage.getItem('auth.refresh')
    const storedId = localStorage.getItem('auth.user.id')
    const storedName = localStorage.getItem('auth.user.name')
    const storedEmail = localStorage.getItem('auth.user.email')

    if (storedAccess && storedRefresh) {
      this.accessToken = storedAccess
      this.refreshToken = storedRefresh
      this.isAuthenticated = true
      this.user.id = storedId
      this.user.name = storedName || ''
      this.user.email = storedEmail || ''
    }
  },

  setToken(data: { access: string; refresh: string }) {
    this.accessToken = data.access
    this.refreshToken = data.refresh
    this.isAuthenticated = true
    localStorage.setItem('auth.access', data.access)
    localStorage.setItem('auth.refresh', data.refresh)
  },

  removeToken() {
    this.accessToken = ''
    this.refreshToken = ''
    this.isAuthenticated = false
    this.user = { id: null, name: '', email: '' }
    localStorage.removeItem('auth.access')
    localStorage.removeItem('auth.refresh')
    localStorage.removeItem('auth.user.id')
    localStorage.removeItem('auth.user.name')
    localStorage.removeItem('auth.user.email')
  },

  setUser(user: { id: string | null; name: string; email: string }) {
    this.user = user
    localStorage.setItem('auth.user.id', user.id ? user.id : '')
    localStorage.setItem('auth.user.name', user.name)
    localStorage.setItem('auth.user.email', user.email)
  },

  refreshTokenAction() {
    axios
      .post('/api/refresh/', { refresh: this.refreshToken })
      .then((response) => {
        this.accessToken = response.data.access
        localStorage.setItem('auth.access', response.data.access)
        axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`
      })
      .catch((error) => {
        console.error(error)
        this.removeToken()
      })
  },
})

export default auth
