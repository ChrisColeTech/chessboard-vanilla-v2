import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Stats Domain API Client
 * Handles all stats-related API operations
 */
export class StatsAPIClient extends BaseAPIClient {
  async getOverviewStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/overview${queryString}`);
  }
  async getPuzzleStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/puzzles${queryString}`);
  }
  async getGameStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/games${queryString}`);
  }
  async getProgressStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/progress${queryString}`);
  }
  async getPerformanceStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/performance${queryString}`);
  }
  async getRatingStats(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/stats/ratings${queryString}`);
  }
}

export default StatsAPIClient;
