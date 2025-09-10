import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * StudyPlans Domain API Client
 * Handles all study-plans-related API operations
 */
export class StudyPlansAPIClient extends BaseAPIClient {
  async getUserStudyPlans(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/studyPlans/user/:userId${queryString}`);
  }
  async createStudyPlan(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/studyPlans/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async updatePlan(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/studyPlans/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
}

export default StudyPlansAPIClient;
