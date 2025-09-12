import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * LearningModules Domain API Client
 * Handles all learning-modules-related API operations
 */
export class LearningModulesAPIClient extends BaseAPIClient {
  async getModulesByPath(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/learningModules/path/:pathId${queryString}`);
  }
  async getModuleById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/learningModules/${id}`);
  }
  async completeModule(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/learningModules/${id}/complete`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default LearningModulesAPIClient;
