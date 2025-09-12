import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Progress Domain API Client
 * Handles all progress-related API operations
 */
export class ProgressAPIClient extends BaseAPIClient {
  async getUserProgress(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/progress/user/:userId${queryString}`);
  }
  async updateProgress(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/progress/update`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  async getProgressStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/progress/stats/:userId${queryString}`);
  }
}

export default ProgressAPIClient;
