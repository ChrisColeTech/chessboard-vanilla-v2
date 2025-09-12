import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Sessions Domain API Client
 * Handles all sessions-related API operations
 */
export class SessionsAPIClient extends BaseAPIClient {
  async createSession(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/sessions/create`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async validateSession(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/sessions/validate/:token${queryString}`);
  }
  async expireSession(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/sessions/${id}`, {
      method: 'DELETE',
    });
  }
}

export default SessionsAPIClient;
