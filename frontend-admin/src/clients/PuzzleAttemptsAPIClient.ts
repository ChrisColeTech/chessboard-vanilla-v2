import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * PuzzleAttempts Domain API Client
 * Handles all puzzle-attempts-related API operations
 */
export class PuzzleAttemptsAPIClient extends BaseAPIClient {
  async recordAttempt(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/puzzleAttempts/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getUserAttempts(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzleAttempts/user/:userId${queryString}`);
  }
  async getPuzzleAttempts(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/puzzleAttempts/puzzle/:puzzleId${queryString}`);
  }
}

export default PuzzleAttemptsAPIClient;
