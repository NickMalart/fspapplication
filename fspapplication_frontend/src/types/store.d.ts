declare module '@/stores/company' {
  import { Store } from 'pinia'
  
  export interface Company {
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
  
  export interface CompanyState {
    company: Company | null
    loading: boolean
    error: string | null
  }
  
  export interface CompanyStoreActions {
    fetchCompany(): Promise<void>
    updateCompany(companyData: Partial<Company>): Promise<boolean>
  }
  
  export type CompanyStore = Store<'company', CompanyState> & CompanyStoreActions
  
  export function useCompanyStore(): CompanyStore
} 