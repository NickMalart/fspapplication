import axios from 'axios';
import type {
    User,
    UserListItem,
    UserProfile,
    UpdateUserRequest,
    UpdateUserProfileRequest,
    UserResponse,
    UserListResponse,
    PaginatedResponse
} from '@/types/userProfile';

export class UserProfileService {
    private baseUrl: string;

    constructor() {
        this.baseUrl = '/api';
    }

    // Current User Operations
    async getCurrentUser(): Promise<User> {
        const response = await axios.get<UserResponse>(`${this.baseUrl}/me/`);
        return response.data.user;
    }

    async updateCurrentUser(data: UpdateUserRequest): Promise<User> {
        // Handle multipart form data if there's a file upload
        let formData: FormData | UpdateUserRequest = data;
        
        if (data.avatar instanceof File) {
            formData = new FormData();
            (formData as FormData).append('avatar', data.avatar);
            
            // Append other fields
            if (data.first_name) (formData as FormData).append('first_name', data.first_name);
            if (data.last_name) (formData as FormData).append('last_name', data.last_name);
            if (data.email) (formData as FormData).append('email', data.email);
            
            // Handle nested profile data
            if (data.profile) {
                Object.entries(data.profile).forEach(([key, value]) => {
                    if (value !== undefined) {
                        (formData as FormData).append(`profile.${key}`, value.toString());
                    }
                });
            }
        }

        const response = await axios.patch<UserResponse>(
            `${this.baseUrl}/me/`,
            formData,
            {
                headers: data.avatar instanceof File
                    ? { 'Content-Type': 'multipart/form-data' }
                    : { 'Content-Type': 'application/json' }
            }
        );
        return response.data.user;
    }

    // User List Operations
    async getUsers(params: {
        page?: number;
        page_size?: number;
        search?: string;
        ordering?: string;
        user_type?: string;
        status?: 'active' | 'inactive';
    } = {}): Promise<PaginatedResponse<UserListItem>> {
        const response = await axios.get<UserListResponse>(`${this.baseUrl}/users/`, { params });
        return response.data;
    }

    async getUserById(id: string): Promise<User> {
        const response = await axios.get<User>(`${this.baseUrl}/users/${id}/`);
        return response.data;
    }

    async createUser(data: UpdateUserRequest): Promise<User> {
        const response = await axios.post<User>(`${this.baseUrl}/users/`, data);
        return response.data;
    }

    async updateUser(id: string, data: UpdateUserRequest): Promise<User> {
        // Handle multipart form data if there's a file upload
        let formData: FormData | UpdateUserRequest = data;
        
        if (data.avatar instanceof File) {
            formData = new FormData();
            (formData as FormData).append('avatar', data.avatar);
            
            // Append other fields
            if (data.first_name) (formData as FormData).append('first_name', data.first_name);
            if (data.last_name) (formData as FormData).append('last_name', data.last_name);
            if (data.email) (formData as FormData).append('email', data.email);
            
            // Handle nested profile data
            if (data.profile) {
                Object.entries(data.profile).forEach(([key, value]) => {
                    if (value !== undefined) {
                        (formData as FormData).append(`profile.${key}`, value.toString());
                    }
                });
            }
        }

        const response = await axios.patch<User>(
            `${this.baseUrl}/users/${id}/`,
            formData,
            {
                headers: data.avatar instanceof File
                    ? { 'Content-Type': 'multipart/form-data' }
                    : { 'Content-Type': 'application/json' }
            }
        );
        return response.data;
    }

    async deleteUser(id: string): Promise<void> {
        await axios.delete(`${this.baseUrl}/users/${id}/`);
    }

    // User Profile Operations
    async getUserProfile(userId: string): Promise<UserProfile> {
        const response = await axios.get<UserProfile>(`${this.baseUrl}/users/${userId}/profile/`);
        return response.data;
    }

    async updateUserProfile(userId: string, data: UpdateUserProfileRequest): Promise<UserProfile> {
        const response = await axios.patch<UserProfile>(
            `${this.baseUrl}/users/${userId}/profile/`,
            data
        );
        return response.data;
    }

    // User Status Operations
    async activateUser(userId: string): Promise<void> {
        await axios.post(`${this.baseUrl}/users/${userId}/activate/`);
    }

    async deactivateUser(userId: string): Promise<void> {
        await axios.post(`${this.baseUrl}/users/${userId}/deactivate/`);
    }

    // Profile Operations
    async getCurrentUserProfile(): Promise<UserProfile> {
        const response = await axios.get<UserProfile>(`${this.baseUrl}/profiles/my_profile/`);
        return response.data;
    }

    async updateCurrentUserProfile(data: UpdateUserProfileRequest): Promise<UserProfile> {
        const response = await axios.patch<UserProfile>(
            `${this.baseUrl}/profiles/my_profile/`,
            data
        );
        return response.data;
    }
} 