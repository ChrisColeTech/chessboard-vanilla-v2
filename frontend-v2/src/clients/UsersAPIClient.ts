import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Users Domain API Client
 * Handles all users-related API operations
 */
export class UsersAPIClient extends BaseAPIClient {
  async getUserProfile(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/users/profile${queryString}`);
  }
  async updateUserProfile(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/users/profile`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  async getUserPreferences(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/users/preferences${queryString}`);
  }
  async updateUserPreferences(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/users/preferences`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  async getUserSettings(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/users/settings${queryString}`);
  }
  async updateUserSettings(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/users/settings`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
}

export default UsersAPIClient;
