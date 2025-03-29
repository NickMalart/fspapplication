import { defineStore } from 'pinia'
import type { Router } from 'vue-router'

// Define interfaces for User and State
interface User {
  username?: string;
  email?: string;
  // Add other user properties as needed, e.g.:
  // id?: string | number;
  // first_name?: string;
  // last_name?: string;
  [key: string]: any; // Allows for additional properties
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    const storedState = localStorage.getItem('authState')
    return storedState
      ? JSON.parse(storedState)
      : {
          user: null,
          isAuthenticated: false,
        }
  },
  actions: {
    async setCsrfToken(): Promise<void> {
      await fetch('http://localhost:8000/api/set-csrf-token', {
        method: 'GET',
        credentials: 'include',
      })
    },

    async login(email: string, password: string, router: Router | null = null): Promise<void> {
      try {
        const response = await fetch('http://localhost:8000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          body: JSON.stringify({
            email,
            password,
          }),
          credentials: 'include',
        })
        const data = await response.json()
        if (data.success) {
          this.isAuthenticated = true
          await this.fetchUser()
          this.saveState()
          console.log('Login successful!')
          if (router) {
            await router.push({ name: 'home' })
          }
        } else {
          this.user = null
          this.isAuthenticated = false
          this.saveState()
          console.error('Login failed:', data.message || 'Unknown error')
          throw new Error(data.message || 'Login failed.')
        }
      } catch (error) {
        console.error('Login request failed:', error)
        this.user = null
        this.isAuthenticated = false
        this.saveState()
        throw error
      }
    },

    async logout(router: Router | null = null): Promise<void> {
      try {
        const response = await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken(),
          },
          credentials: 'include',
        })
        if (response.ok) {
          this.user = null
          this.isAuthenticated = false
          this.saveState()
          console.log('Logout successful!')
          if (router) {
            await router.push({ name: 'Signin' })
          }
        } else {
           console.error('Logout failed on server:', response.statusText)
        }
      } catch (error) {
        console.error('Logout request failed:', error)
        throw error
      }
    },

    async fetchUser(): Promise<void> {
      try {
        const response = await fetch('http://localhost:8000/api/user', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        })
        if (response.ok) {
          const data = await response.json()
          this.user = data as User
          this.isAuthenticated = true
        } else {
          this.user = null
          this.isAuthenticated = false
          console.error('Failed to fetch user:', response.status, response.statusText)
        }
      } catch (error) {
        console.error('Network error fetching user:', error)
        this.user = null
        this.isAuthenticated = false
      }
      this.saveState()
    },

    saveState(): void {
      localStorage.setItem(
        'authState',
        JSON.stringify({
          user: this.user,
          isAuthenticated: this.isAuthenticated,
        }),
      )
    },
  },
})

export function getCSRFToken(): string {
  const name = 'csrftoken'
  let cookieValue: string | null = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  if (cookieValue === null) {
    throw new Error('Missing CSRF cookie.')
  }
  return cookieValue
}