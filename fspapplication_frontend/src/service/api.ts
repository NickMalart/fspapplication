import axios, { AxiosInstance } from 'axios';

// Get the API URL from environment variables or use a default
const API_URL = import.meta.env.VITE_API_URL || '/api';

// Create API client instance with default configuration
export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // Enable cookies and credentials
});

// Add request interceptor for auth token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage if available
    const token = localStorage.getItem('auth.access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add tenant header for Django Tenants
    const tenant = localStorage.getItem('auth.tenant');
    if (tenant) {
      config.headers['X-DTS-TENANT'] = tenant;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for common error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized responses
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login if needed
      localStorage.removeItem('auth.access');
      localStorage.removeItem('auth.refresh');
      // Optional: Redirect to login page
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Add isAxiosError method to the apiClient
// This is a type-safe way to extend the AxiosInstance
interface ExtendedAxiosInstance extends AxiosInstance {
  isAxiosError: typeof axios.isAxiosError;
}

// Add the method to our instance and cast it to the extended type
(apiClient as ExtendedAxiosInstance).isAxiosError = axios.isAxiosError;

// Re-export with the extended type
export default apiClient as ExtendedAxiosInstance; 