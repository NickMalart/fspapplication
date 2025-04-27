import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/stores/auth'; // Import Pinia auth store

// --- Case Conversion Utilities ---
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
}

function convertKeys(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(v => convertKeys(v));
  } else if (obj !== null && obj.constructor === Object) {
    return Object.keys(obj).reduce(
      (result, key) => ({
        ...result,
        [toCamelCase(key)]: convertKeys(obj[key]),
      }),
      {}
    );
  }
  return obj;
}
// --- End Case Conversion Utilities ---
const API_BASE_URL = '/api';

// Create API client instance with default configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL, // Use the proxy path
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
});

// --- Request Interceptor ---
// Adds Authorization header and Tenant header if available in the store
apiClient.interceptors.request.use(
  (config) => {
    const auth = useAuthStore();
    if (auth.accessToken) {
      config.headers.Authorization = `Bearer ${auth.accessToken}`;
    }

    if (auth.tenant) {
      config.headers['X-DTS-TENANT'] = auth.tenant;
    }

    return config;
  },
  (error) => Promise.reject(error)
);


// --- Response Interceptor ---

// Variables for handling token refresh queueing
let isRefreshing = false;
let failedQueue: { resolve: (value?: any) => void; reject: (reason?: any) => void }[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => {
    // Convert response data keys to camelCase
    if (response.data) {
      response.data = convertKeys(response.data);
    }
    return response; // Pass through successful responses
  },
  async (error) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    const auth = useAuthStore();

    // --- Handle 403 Forbidden (Tenant Access Denied) ---
    if (error.response?.status === 403) {

      // Prevent infinite loops if the original request was already the logout attempt
      const logoutPath = 'auth/logout/'; // Define the correct relative path
      if (originalRequest.url !== logoutPath) {
        try {
          // 1. Attempt to hit the backend logout endpoint
          await apiClient.get(logoutPath);
        } catch (logoutError: any) {
          // Logged out on frontend even if backend call fails
        }
      }

      // 2. Clear frontend auth state for immediate UI update
      auth.removeToken();

      // 3. Redirect to a base login page (using the root path '/')
      const publicHostname = 'localhost'; // Consider moving to env vars or config
      const port = window.location.port ? `:${window.location.port}` : '';
      const publicLoginUrl = `${window.location.protocol}//${publicHostname}${port}/`; // Construct the public URL

      window.location.href = publicLoginUrl; // Redirect to the public root path

      // Reject the promise to stop further processing
      return Promise.reject(new Error('Access Denied to Tenant - Logged Out'));
    }
    // --- End 403 Handling ---

    // Existing 401 handling (potentially needs review/removal for session auth)
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/api/account/token/refresh/') {
       // TODO: Review JWT refresh logic if session auth is primary
       // If Kinde/session auth is primary, you might want to redirect on 401 too:
       // auth.removeToken();
       // window.location.href = '/'; // Or your login path
       // return Promise.reject(new Error('Authentication Required'));
    }

    // For errors other than 401/403 or retries, just pass them along
    return Promise.reject(error);
  }
);


// Add isAxiosError method to the apiClient for type safety
interface ExtendedAxiosInstance extends AxiosInstance {
  isAxiosError: typeof axios.isAxiosError;
}

// Add the method to our instance and cast it
(apiClient as ExtendedAxiosInstance).isAxiosError = axios.isAxiosError;

// Re-export with the extended type
export default apiClient as ExtendedAxiosInstance; 