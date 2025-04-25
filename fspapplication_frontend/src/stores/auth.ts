import { defineStore } from 'pinia'
// Remove direct axios import here, interceptors will handle headers
// import axios from 'axios' 
// Remove configureApi import if it's only setting axios defaults
// import { configureApi } from '@/utils/api'

// Interface for tenant data (can be moved to a types file if preferred)
interface TenantInfo {
  name: string;
  schema_name: string;
  domain: string | null; 
}

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
    // State for multi-tenant selection flow (not persisted)
    tenantListForSelection: null as TenantInfo[] | null,
    tempTokenForSelection: null as string | null,
    // State for authentication errors
    authError: null as string | null,
  }),

  actions: {
    // init() action is likely no longer needed as state is initialized above 
    // and interceptors handle headers. Remove it or simplify significantly.
    // init() {
    //   // ... removed logic ...
    // },

    setToken(data: { access: string; refresh: string }) {
      console.log("AuthStore: Setting tokens");
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
      console.log("AuthStore: Setting tenant", tenant);
      this.tenant = tenant
      localStorage.setItem('auth.tenant', tenant)
    },

    setUser(backendUser: { id: string, email: string }) {      
      console.log("AuthStore: Setting user", backendUser);
      this.user = {
        id: backendUser.id,
        email: backendUser.email,
      }
      localStorage.setItem('auth.user.id', this.user.id || '')
      localStorage.setItem('auth.user.email', this.user.email)
    },

    removeToken() {
      console.log("AuthStore: Removing tokens and session info");
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

    // Remove the old refreshTokenAction, the interceptor handles this now
    // refreshTokenAction() {
    //   // ... removed logic ...
    // },

    // --- Actions for Tenant Selection Flow ---
    setTenantSelectionInfo(tenants: TenantInfo[], tempToken: string) {
        console.log("AuthStore: Setting tenant selection info", { tenants, tempToken });
        this.tenantListForSelection = tenants;
        this.tempTokenForSelection = tempToken;
        this.authError = null; // Clear error on starting selection
    },
    
    clearTenantSelectionInfo() {
        console.log("AuthStore: Clearing tenant selection info");
        this.tenantListForSelection = null;
        this.tempTokenForSelection = null;
    },
    
    // --- Action for Errors ---
    setError(message: string | null) {
        console.log("AuthStore: Setting error", message);
        this.authError = message;
        // Clear sensitive info on error if appropriate?
        // For now, just set the message.
    }
  },
})
