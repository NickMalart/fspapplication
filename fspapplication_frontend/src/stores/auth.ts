import { defineStore } from 'pinia'
// Interceptors will handle headers
// Interface for tenant data
interface TenantInfo {
  name: string;
  schema_name: string;
  domain: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Attempt to initialize state from localStorage on load
    isAuthenticated: !!localStorage.getItem('auth.access'),
    accessToken: localStorage.getItem('auth.access') || '',
    refreshToken: localStorage.getItem('auth.refresh') || '',
    tenant: localStorage.getItem('auth.tenant') || '',
    user: {
      id: localStorage.getItem('auth.user.id') as string | null,
      email: localStorage.getItem('auth.user.email') || '',
    },
    // State for multi-tenant selection flow (not persisted)
    tenantListForSelection: null as TenantInfo[] | null,
    tempTokenForSelection: null as string | null,
    // State for authentication errors
    authError: null as string | null,
  }),

  actions: {
    setToken(data: { access: string; refresh: string }) {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.isAuthenticated = true
      this.authError = null // Clear any previous errors
      this.clearTenantSelectionInfo() // Clear temporary selection state

      // Persist to localStorage
      localStorage.setItem('auth.access', data.access)
      localStorage.setItem('auth.refresh', data.refresh)
    },

    setTenant(tenant: string) {
      this.tenant = tenant
      localStorage.setItem('auth.tenant', tenant)
    },

    setUser(backendUser: { id: string, email: string }) {
      this.user = {
        id: backendUser.id,
        email: backendUser.email,
      }
      localStorage.setItem('auth.user.id', this.user.id || '')
      localStorage.setItem('auth.user.email', this.user.email)
    },

    removeToken() {
      // Clear state
      this.accessToken = ''
      this.refreshToken = ''
      this.tenant = ''
      this.isAuthenticated = false
      this.user = { id: null, email: '' }
      this.authError = null
      this.clearTenantSelectionInfo()

      // Clear persisted data
      localStorage.removeItem('auth.access')
      localStorage.removeItem('auth.refresh')
      localStorage.removeItem('auth.tenant')
      localStorage.removeItem('auth.user.id')
      localStorage.removeItem('auth.user.email')
    },

    // --- Actions for Tenant Selection Flow ---
    setTenantSelectionInfo(tenants: TenantInfo[], tempToken: string) {
        this.tenantListForSelection = tenants;
        this.tempTokenForSelection = tempToken;
        this.authError = null; // Clear error on starting selection
    },

    clearTenantSelectionInfo() {
        this.tenantListForSelection = null;
        this.tempTokenForSelection = null;
    },

    // --- Action for Errors ---
    setError(message: string | null) {
        this.authError = message;
        // Potentially clear sensitive info on error?
    }
  },
})
