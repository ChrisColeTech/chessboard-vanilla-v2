// API service for chess puzzles from backend
import type { Puzzle, PuzzleFilters, PuzzleStats } from '../../types/puzzle.types';
import { getRandomSamplePuzzle } from '../../data/samplePuzzles';

class PuzzleApiService {
  private baseUrl = 'http://localhost:3001/api/puzzles';

  /**
   * Generic API request handler
   */
  private async apiRequest<T>(url: string): Promise<T> {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    if (!data.success) {
      throw new Error(data.error || 'API request returned error');
    }
    
    return data.data;
  }

  /**
   * Build query string from filters
   */
  private buildQueryString(filters: PuzzleFilters = {}): string {
    const params = new URLSearchParams();
    
    if (filters.minRating !== undefined) {
      params.append('minRating', filters.minRating.toString());
    }
    if (filters.maxRating !== undefined) {
      params.append('maxRating', filters.maxRating.toString());
    }
    if (filters.themes && filters.themes.length > 0) {
      params.append('themes', filters.themes.join(','));
    }
    if (filters.limit !== undefined) {
      params.append('limit', filters.limit.toString());
    }
    if (filters.offset !== undefined) {
      params.append('offset', filters.offset.toString());
    }
    
    return params.toString();
  }

  /**
   * Get a random puzzle based on filters
   */
  async getRandomPuzzle(filters: PuzzleFilters = {}): Promise<Puzzle | null> {
    try {
      const queryString = this.buildQueryString(filters);
      const url = `${this.baseUrl}/random${queryString ? `?${queryString}` : ''}`;
      
      return await this.apiRequest<Puzzle>(url);
    } catch (error) {
      console.warn('Backend API not available, using sample puzzle:', error);
      // Fallback to sample puzzle when API is not available
      return getRandomSamplePuzzle();
    }
  }

  /**
   * Get puzzle by ID
   */
  async getPuzzleById(id: string): Promise<Puzzle | null> {
    try {
      return await this.apiRequest<Puzzle>(`${this.baseUrl}/${id}`);
    } catch (error) {
      console.error('Failed to get puzzle by ID:', error);
      return null;
    }
  }

  /**
   * Get multiple puzzles with pagination
   */
  async getPuzzles(filters: PuzzleFilters = {}): Promise<Puzzle[]> {
    try {
      const queryString = this.buildQueryString(filters);
      const url = `${this.baseUrl}${queryString ? `?${queryString}` : ''}`;
      
      return await this.apiRequest<Puzzle[]>(url);
    } catch (error) {
      console.error('Failed to get puzzles:', error);
      return [];
    }
  }

  /**
   * Get available themes
   */
  async getAvailableThemes(): Promise<string[]> {
    try {
      return await this.apiRequest<string[]>(`${this.baseUrl}/themes`);
    } catch (error) {
      console.error('Failed to get themes:', error);
      return [];
    }
  }

  /**
   * Get puzzle statistics
   */
  async getPuzzleStats(): Promise<PuzzleStats | null> {
    try {
      return await this.apiRequest<PuzzleStats>(`${this.baseUrl}/stats`);
    } catch (error) {
      console.error('Failed to get puzzle stats:', error);
      return null;
    }
  }

  /**
   * Search puzzles by description
   */
  async searchPuzzles(searchTerm: string, limit: number = 10): Promise<Puzzle[]> {
    try {
      const params = new URLSearchParams({
        q: searchTerm,
        limit: limit.toString()
      });
      
      return await this.apiRequest<Puzzle[]>(`${this.baseUrl}/search?${params}`);
    } catch (error) {
      console.error('Failed to search puzzles:', error);
      return [];
    }
  }
}

// Singleton instance
export const puzzleApiService = new PuzzleApiService();