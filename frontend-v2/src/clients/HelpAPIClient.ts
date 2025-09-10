import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Help Domain API Client
 * Handles all help-related API operations
 */
export class HelpAPIClient extends BaseAPIClient {
  async getAllHelp(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/help${queryString}`);
  }
  async getHelpByCategory(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/help/category/:category${queryString}`);
  }
  async searchHelp(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/help/search${queryString}`);
  }
}

export default HelpAPIClient;
