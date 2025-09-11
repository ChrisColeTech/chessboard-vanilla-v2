import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Auth Domain API Client
 * Handles all auth-related API operations
 */
export class AuthAPIClient extends BaseAPIClient {
  async register(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/register`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async login(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/login`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getCurrentUser(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/auth/me${queryString}`);
  }
  async updateProfile(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/profile`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  async changePassword(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/change-password`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async verifyToken(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/verify-token`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async forgotPassword(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/forgot-password`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async resetPassword(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/reset-password`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async logout(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/logout`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async checkEmailAvailability(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/check-email`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async checkUsernameAvailability(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/auth/check-username`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async deleteAccount(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/auth/${id}`, {
      method: 'DELETE',
    });
  }
  async healthCheck(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/auth/health${queryString}`);
  }
}

export default AuthAPIClient;
