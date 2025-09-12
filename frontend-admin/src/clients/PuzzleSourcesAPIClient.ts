import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * PuzzleSources Domain API Client
 * Handles all puzzle-sources-related API operations
 */
export class PuzzleSourcesAPIClient extends BaseAPIClient {
  async getAllSources(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/puzzleSources${queryString}`);
  }
  async getSourceById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/puzzleSources/${id}`);
  }
}

export default PuzzleSourcesAPIClient;
