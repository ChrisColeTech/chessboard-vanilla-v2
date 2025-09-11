import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * AiOpponents Domain API Client
 * Handles all ai-opponents-related API operations
 */
export class AiOpponentsAPIClient extends BaseAPIClient {
  async getAllOpponents(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/aiOpponents${queryString}`);
  }
  async getOpponentById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/aiOpponents/${id}`);
  }
  async getOpponentsByDifficulty(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/aiOpponents/difficulty/:level${queryString}`);
  }
}

export default AiOpponentsAPIClient;
