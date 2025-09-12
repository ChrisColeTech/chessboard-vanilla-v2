import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Endgames Domain API Client
 * Handles all endgames-related API operations
 */
export class EndgamesAPIClient extends BaseAPIClient {
  async getAllEndgames(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/endgames${queryString}`);
  }
  async getEndgameById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/endgames/${id}`);
  }
  async getEndgamesByCategory(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/endgames/category/:category${queryString}`);
  }
}

export default EndgamesAPIClient;
