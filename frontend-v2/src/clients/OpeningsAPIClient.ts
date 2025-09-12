import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Openings Domain API Client
 * Handles all openings-related API operations
 */
export class OpeningsAPIClient extends BaseAPIClient {
  async getAllOpenings(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/openings${queryString}`);
  }
  async getOpeningByEco(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/openings/eco/:code${queryString}`);
  }
  async searchOpenings(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/openings/search${queryString}`);
  }
}

export default OpeningsAPIClient;
