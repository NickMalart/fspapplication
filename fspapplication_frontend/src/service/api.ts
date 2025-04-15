import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/stores/auth'; // Import Pinia auth store

// Get the API URL from environment variables or use a default
// Use '/api' to route requests through the Vite proxy during development
const API_BASE_URL = '/api'; // Changed from import.meta.env.VITE_API_URL

// Create API client instance with default configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL, // Use the proxy path
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // Enable cookies and credentials if needed for CSRF or session auth
});

// --- Request Interceptor ---
// Adds Auth token and Tenant header from Pinia store to every request
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
// Handles token expiry and refresh automatically

let isRefreshing = false; // Flag to prevent multiple refresh requests
let failedQueue: { resolve: (value?: any) => void; reject: (reason?: any) => void }[] = []; // Queue for requests that failed during refresh

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
  (response) => response, // Pass through successful responses
  async (error) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    const auth = useAuthStore();

    // Check if it's a 401 error, not a retry attempt, and not the refresh token endpoint itself
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/api/account/token/refresh/') {

      if (isRefreshing) {
        // If already refreshing, queue the original request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          // Retry the request with the new token from the successful refresh
          originalRequest.headers!['Authorization'] = `Bearer ${token}`;
          return apiClient(originalRequest);
        }).catch(err => {
          // Propagate error if the refresh failed
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true; // Mark as retry attempt
      isRefreshing = true;

      const refreshToken = auth.refreshToken;

      if (!refreshToken) {
        isRefreshing = false;
        auth.removeToken(); // Use removeToken instead of logout
        return Promise.reject(error);
      }

      try {
        const refreshResponse = await axios.post(`${API_BASE_URL}/api/account/token/refresh/`, {
          refresh: refreshToken,
        }, {
          headers: { // Ensure tenant header is sent for refresh request if needed by backend
             'X-DTS-TENANT': auth.tenant || undefined
          }
        });

        const newAccessToken = refreshResponse.data.access;
        // Note: If using ROTATE_REFRESH_TOKENS, backend might send a new refresh token too
        // const newRefreshToken = refreshResponse.data.refresh;
        auth.setToken({ access: newAccessToken, refresh: refreshToken /* Use newRefreshToken if provided */ });

        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`; // Update default header
        originalRequest.headers!['Authorization'] = `Bearer ${newAccessToken}`; // Update header for the original request

        processQueue(null, newAccessToken); // Process queue with new token
        isRefreshing = false;
        return apiClient(originalRequest); // Retry the original request

      } catch (refreshError: any) {
        processQueue(refreshError, null); // Process queue with error
        isRefreshing = false;
        auth.removeToken(); // Use removeToken instead of logout
        return Promise.reject(refreshError);
      }
    }

    // For errors other than 401 or retries, just pass them along
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