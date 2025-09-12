import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Achievements Domain API Client
 * Handles all achievements-related API operations
 */
export class AchievementsAPIClient extends BaseAPIClient {
  async getAllAchievements(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/achievements${queryString}`);
  }
  async getUserAchievements(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/achievements/user/:userId${queryString}`);
  }
  async unlockAchievement(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/achievements/unlock`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default AchievementsAPIClient;
