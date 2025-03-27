import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

/**
 * Configures axios with the correct base URL based on the environment
 * 
 * @returns The base API URL
 */
export function configureApi() {
  const protocol = window.location.protocol
  const host = window.location.host
  const backendHost = host.replace(':5173', ':8000')
  const baseUrl = `${protocol}//${backendHost}`
  
  console.log('API Configuration:', { 
    protocol, 
    host, 
    backendHost, 
    baseUrl 
  })
  
  // Set default base URL
  axios.defaults.baseURL = baseUrl
  
  // Get tenant from hostname
  const hostname = window.location.hostname
  const tenant = hostname.split('.')[0]
  
  console.log('Tenant detection:', { 
    hostname, 
    tenant,
    isValid: !!tenant && tenant !== 'localhost'
  })
  
  // Set tenant header if available and valid
  if (tenant && tenant !== 'localhost') {
    console.log('Setting tenant header:', tenant)
    axios.defaults.headers.common['X-DTS-TENANT'] = tenant
  } else {
    console.warn('No valid tenant found in hostname, using default "dev"')
    // Use default tenant for development
    axios.defaults.headers.common['X-DTS-TENANT'] = 'dev'
  }
  
  // Log current axios configuration
  console.log('Axios configuration:', {
    baseURL: axios.defaults.baseURL,
    headers: {
      'X-DTS-TENANT': axios.defaults.headers.common['X-DTS-TENANT'],
      'Authorization': axios.defaults.headers.common['Authorization']
    }
  })
  
  return baseUrl
}

/**
 * Creates a configured axios client with tenant headers
 * 
 * @returns Axios instance with tenant headers
 */
export function createApiClient() {
  const auth = useAuthStore()
  const baseURL = configureApi()
  
  // Create a new axios instance with base URL
  const apiClient = axios.create({
    baseURL
  })
  
  // Add request interceptor to include tenant header
  apiClient.interceptors.request.use(config => {
    // Add tenant header
    if (auth.tenant) {
      config.headers['X-DTS-TENANT'] = auth.tenant
    }
    
    // Add auth token if available
    if (auth.accessToken) {
      config.headers.Authorization = `Bearer ${auth.accessToken}`
    }
    
    return config
  })
  
  return apiClient
}

// Export default configured axios instance
export default axios 