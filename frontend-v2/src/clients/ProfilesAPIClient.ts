import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Profiles Domain API Client
 * Handles all profiles-related API operations
 */
export class ProfilesAPIClient extends BaseAPIClient {
  async getProfile(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/profiles/:userId${queryString}`);
  }
  async updateProfile(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/profiles/:userId`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
}

export default ProfilesAPIClient;
