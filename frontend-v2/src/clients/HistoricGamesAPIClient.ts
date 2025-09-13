import type { ApiResponse } from '../types/common';
import { BaseAPIClient } from './BaseAPIClient';

/**
 * HistoricGames Domain API Client
 * Handles all historic-games-related API operations
 */
export class HistoricGamesAPIClient extends BaseAPIClient {
  async getAllHistoricGames(params?: any): Promise<ApiResponse<any[]>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any[]>(`/api/historicGames${queryString}`);
  }
  async getGameById(id: string): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/historicGames/${id}`);
  }
  async searchGames(data: any): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/historicGames/search`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  async getGamesByPlayer(params?: any): Promise<ApiResponse<any>> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request<any>(`/api/historicGames/player/:player${queryString}`);
  }
}

export default HistoricGamesAPIClient;
