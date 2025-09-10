import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Analytics Domain API Client
 * Handles all analytics-related API operations
 */
export class AnalyticsAPIClient extends BaseAPIClient {
  async trackEvent(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/analytics/track`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getUserAnalytics(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/analytics/user/:userId${queryString}`);
  }
}

export default AnalyticsAPIClient;
