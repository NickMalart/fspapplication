import { defineStore } from 'pinia'
import axios from 'axios'

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
        const response = await axios.get<Company>('/api/organisation/company/')
        this.company = response.data
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Failed to fetch company information'
        console.error('Error fetching company:', error)
      } finally {
        this.loading = false
      }
    },
    
    async updateCompany(companyData: Partial<Company>): Promise<boolean> {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put<Company>('/api/organisation/company/', companyData)
        this.company = response.data
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Failed to update company information'
        console.error('Error updating company:', error)
        return false
      } finally {
        this.loading = false
      }
    }
  }
}) 