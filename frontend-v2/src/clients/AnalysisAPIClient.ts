import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Analysis Domain API Client
 * Handles all analysis-related API operations
 */
export class AnalysisAPIClient extends BaseAPIClient {
  async analyzePosition(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/analysis/position`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getPositionAnalysis(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/analysis/position/:fen${queryString}`);
  }
}

export default AnalysisAPIClient;
