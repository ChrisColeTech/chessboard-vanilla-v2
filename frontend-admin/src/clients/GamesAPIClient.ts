import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * Games Domain API Client
 * Handles all games-related API operations
 */
export class GamesAPIClient extends BaseAPIClient {
  async getGames(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/games${queryString}`);
  }
  async getGameById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/games/${id}`);
  }
  async createGame(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/games/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async updateGame(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/games/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  async analyzeGame(id: string, data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/games/${id}/analyze`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getGameAnalysis(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/games/${id}`);
  }
  async getGameReviews(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/games/reviews${queryString}`);
  }
}

export default GamesAPIClient;
