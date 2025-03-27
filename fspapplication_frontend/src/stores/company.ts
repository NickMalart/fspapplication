import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import { configureApi } from '@/utils/api'

interface Company {
  name: string
  logo?: string
  unit?: string
  number?: string
  street?: string
  city?: string
  state?: string
  postal_code?: string
  country?: string
  latitude?: number
  longitude?: number
  phone?: string
  email?: string
  website?: string
  tax_number?: string
  abn_number?: string
  primary_color?: string
  secondary_color?: string
  established_date?: string
}

interface CompanyState {
  company: Company | null
  loading: boolean
  error: string | null
}

export const useCompanyStore = defineStore('company', {
  state: (): CompanyState => ({
    company: null,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchCompany(): Promise<void> {
      this.loading = true
      this.error = null
      
      try {
        console.log('Attempting to fetch company data...')
        
        // Make sure the API is configured with the correct base URL and tenant
        const baseUrl = configureApi()
        
        // Use full URL instead of relative path
        const fullUrl = `${baseUrl}/api/organisation/company/`
        console.log('Full request URL:', fullUrl)
        
        const response = await axios.get<Company>(fullUrl)
        console.log('Company fetch response:', response)
        this.company = response.data
      } catch (error) {
        const axiosError = error as AxiosError
        console.error('Detailed fetch error:', {
          status: axiosError.response?.status,
          statusText: axiosError.response?.statusText,
          data: axiosError.response?.data,
          headers: axiosError.response?.headers,
          url: axiosError.config?.url,
          method: axiosError.config?.method,
          baseURL: axiosError.config?.baseURL,
        })
        
        if (axiosError.response?.status === 404) {
          this.error = 'Company endpoint not found. Please check API configuration.'
        } else {
          this.error = (axiosError.response?.data as any)?.message || 'Failed to fetch company information'
        }
      } finally {
        this.loading = false
      }
    },
    
    async updateCompany(companyData: Partial<Company>): Promise<boolean> {
      this.loading = true
      this.error = null
      
      try {
        console.log('Attempting to update company with data:', companyData)
        
        // Make sure the API is configured with the correct base URL and tenant
        const baseUrl = configureApi()
        console.log('Using base URL:', baseUrl)
        
        // Log headers to debug tenant issue
        console.log('Request headers:', {
          'X-DTS-TENANT': axios.defaults.headers.common['X-DTS-TENANT'],
          'Authorization': axios.defaults.headers.common['Authorization']
        })
        
        // Use full URL instead of relative path
        const fullUrl = `${baseUrl}/api/organisation/company/`
        console.log('Full request URL:', fullUrl)
        
        const response = await axios.put<Company>(fullUrl, companyData)
        console.log('Company update response:', response)
        this.company = response.data
        return true
      } catch (error) {
        const axiosError = error as AxiosError
        console.error('Detailed update error:', {
          status: axiosError.response?.status,
          statusText: axiosError.response?.statusText,
          data: axiosError.response?.data,
          headers: axiosError.response?.headers,
          url: axiosError.config?.url,
          method: axiosError.config?.method,
          baseURL: axiosError.config?.baseURL,
          requestData: companyData
        })
        
        if (axiosError.response?.status === 404) {
          this.error = 'Company endpoint not found. Please verify API URL: /api/organisation/company/'
        } else {
          this.error = (axiosError.response?.data as any)?.message || 'Failed to update company information'
        }
        return false
      } finally {
        this.loading = false
      }
    },

    // Add a debug method to check configuration
    async checkApiConfiguration() {
      // Ensure API is configured
      const baseUrl = configureApi()
      
      console.log('API Configuration Check:', {
        baseUrl,
        axios: {
          defaults: {
            baseURL: axios.defaults.baseURL,
            headers: axios.defaults.headers
          }
        },
        store: {
          company: this.company,
          error: this.error,
          loading: this.loading
        }
      })
    }
  }
}) 