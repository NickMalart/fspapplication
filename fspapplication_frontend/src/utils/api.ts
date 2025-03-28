import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Add case conversion utilities
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

  // Add response interceptor for case conversion
  axios.interceptors.response.use(response => {
    if (response.data) {
      response.data = convertKeys(response.data)
    }
    return response
  })
  
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

  // Add response interceptor for case conversion
  apiClient.interceptors.response.use(response => {
    if (response.data) {
      response.data = convertKeys(response.data)
    }
    return response
  })
  
  return apiClient
}

// Export default configured axios instance
export default axios 