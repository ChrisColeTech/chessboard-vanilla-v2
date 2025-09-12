import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Tutorials Domain API Client
 * Handles all tutorials-related API operations
 */
export class TutorialsAPIClient extends BaseAPIClient {
  async getTutorials(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/tutorials${queryString}`);
  }
  async getTutorialById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/tutorials/${id}`);
  }
  async completeTutorial(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/tutorials/${id}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default TutorialsAPIClient;
