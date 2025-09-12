import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Subscriptions Domain API Client
 * Handles all subscriptions-related API operations
 */
export class SubscriptionsAPIClient extends BaseAPIClient {
  async getUserSubscription(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/subscriptions/user/:userId${queryString}`);
  }
  async createSubscription(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/subscriptions/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async updateSubscription(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/subscriptions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
}

export default SubscriptionsAPIClient;
