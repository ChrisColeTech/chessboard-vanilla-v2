import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Puzzles Domain API Client
 * Handles all puzzles-related API operations
 */
export class PuzzlesAPIClient extends BaseAPIClient {
  async getNextPuzzle(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzles/next${queryString}`);
  }
  async solvePuzzle(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/puzzles/${id}/solve`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getPuzzleHint(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/puzzles/${id}`);
  }
  async getPuzzleCategories(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzles/categories${queryString}`);
  }
  async getPuzzleHistory(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzles/history${queryString}`);
  }
  async createCustomPuzzle(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/puzzles/custom`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getCustomPuzzles(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzles/custom${queryString}`);
  }
}

export default PuzzlesAPIClient;
