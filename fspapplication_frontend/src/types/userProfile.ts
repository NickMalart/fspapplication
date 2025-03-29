// User Types
export type UserType = 'agent' | 'client' | 'employee';

// Functional Group Interface
export interface FunctionalGroup {
    id: number;
    name: string;
    code: string;
}

// Base Profile Interface
export interface UserProfile {
    id: string;
    phone_number: string | null;
    emergency_contact: string | null;
    emergency_contact_first_name: string | null;
    emergency_contact_last_name: string | null;
    street_number: string | null;
    street_name: string | null;
    suburb: string | null;
    city: string | null;
    state: string | null;
    postal_code: string | null;
    country: string | null;
    latitude: number | null;
    longitude: number | null;
    google_place_id: string | null;
    date_of_birth: string | null;
    created_at: string;
    updated_at: string;
    full_address: string;
}

// Company Interface for Employee Profile
export interface Company {
    name: string;
    logo?: string;
    unit?: string;
    number?: string;
    street?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
    latitude?: number;
    longitude?: number;
    phone?: string;
    email?: string;
    website?: string;
    tax_number?: string;
    abn_number?: string;
    primary_color?: string;
    secondary_color?: string;
    established_date?: string;
}

// Specific Profile Types
export interface EmployeeProfileType {
    type: 'employee';
    company: Company;
    department: string;
    employee_id: string | null;
    job_title: string | null;
    start_date: string;
}

export interface AgentProfileType {
    type: 'agent';
    company_name: string;
    license_number: string | null;
    years_of_experience: number;
}

export interface ClientProfileType {
    type: 'client';
    company_name: string;
    industry: string | null;
    client_since: string;
}

// Union type for all specific profiles
export type SpecificProfile = EmployeeProfileType | AgentProfileType | ClientProfileType;

// Main User Interface
export interface User {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    full_name: string;
    avatar: string | null;
    user_type: UserType;
    profile: UserProfile;
    functional_groups: FunctionalGroup[];
    specific_profile: SpecificProfile | null;
    is_active: boolean;
    date_joined: string;
    last_login: string | null;
}

// User List Item Interface (for list views)
export interface UserListItem {
    id: string;
    first_name: string;
    last_name: string;
    full_name: string;
    email: string;
    user_type: UserType;
    avatar: string | null;
    functional_groups: string[];
    employee_details: {
        company: string | null;
        department: string | null;
        job_title: string | null;
        start_date: string | null;
    } | null;
    is_active: boolean;
    date_joined: string;
}

// Response Interfaces
export interface PaginatedResponse<T> {
    count: number;
    total_pages: number;
    current_page: number;
    results: T[];
}

export interface UserResponse {
    user: User;
}

export interface UserListResponse extends PaginatedResponse<UserListItem> {}

// Request Interfaces
export interface UpdateUserProfileRequest {
    phone_number?: string;
    emergency_contact?: string;
    emergency_contact_first_name?: string;
    emergency_contact_last_name?: string;
    street_number?: string;
    street_name?: string;
    suburb?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
    latitude?: number;
    longitude?: number;
    google_place_id?: string;
    date_of_birth?: string;
}

export interface UpdateUserRequest {
    first_name?: string;
    last_name?: string;
    email?: string;
    avatar?: File;
    profile?: UpdateUserProfileRequest;
} 