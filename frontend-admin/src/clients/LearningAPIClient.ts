import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Learning Domain API Client
 * Handles all learning-related API operations
 */
export class LearningAPIClient extends BaseAPIClient {
  async getLearningPaths(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/learningPaths/paths${queryString}`);
  }
  async getLearningPathById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/learningPaths/${id}`);
  }
  async enrollInPath(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/learningPaths/${id}/paths/enroll`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async updateProgress(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/learningPaths/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
}

export default LearningAPIClient;
