import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { PuzzleResponse, CreatePuzzleRequest, UpdatePuzzleRequest } from '../models/Puzzle';

export class PuzzleService {
  private db = Database.getInstance();

  async getNextPuzzle(userId: string): Promise<PuzzleResponse> {
    // Get next puzzle for user based on rating and history
    const result = await this.db.query(`
      SELECT * FROM puzzles 
      WHERE rating BETWEEN $1 AND $2 
      ORDER BY RANDOM() 
      LIMIT 1
    `, [800, 2000]);
    
    if (!result.rows.length) {
      throw new Error('No puzzles available');
    }
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

  async solvePuzzle(puzzleId: string, solutionData: any): Promise<{correct: boolean, solution?: string[]}> {
    const puzzle = await this.db.query('SELECT * FROM puzzles WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('Puzzle not found');
    
    const puzzleData = puzzle.rows[0];
    const userMoves = solutionData.moves || [];
    const solutionMoves = JSON.parse(puzzleData.solution_moves || '[]');
    
    const isCorrect = JSON.stringify(userMoves) === JSON.stringify(solutionMoves);
    
    return {
      correct: isCorrect,
      solution: isCorrect ? undefined : solutionMoves
    };
  }

  async getPuzzleHint(puzzleId: string): Promise<{hint: string}> {
    const puzzle = await this.db.query('SELECT * FROM puzzles WHERE id = $1', [puzzleId]);
    if (!puzzle.rows.length) throw new Error('Puzzle not found');
    
    const themes = JSON.parse(puzzle.rows[0].themes || '[]');
    const hint = themes.length > 0 ? `Look for ${themes[0]} tactics` : 'Look for the best move';
    
    return { hint };
  }

  async getPuzzleCategories(): Promise<string[]> {
    const result = await this.db.query(`
      SELECT DISTINCT themes FROM puzzles 
      WHERE themes IS NOT NULL AND themes != ''
      LIMIT 50
    `);
    
    const allThemes = new Set<string>();
    result.rows.forEach(row => {
      try {
        const themes = JSON.parse(row.themes || '[]');
        themes.forEach((theme: string) => allThemes.add(theme));
      } catch (e) {
        // Skip invalid JSON
      }
    });
    
    return Array.from(allThemes).slice(0, 20);
  }

  async getPuzzleHistory(userId: string): Promise<any[]> {
    // Return empty array for now - would need puzzle_attempts table
    return [];
  }

  async createCustomPuzzle(puzzleData: any): Promise<PuzzleResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO puzzles (id, fen, solution_moves, themes, rating, description)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *
    `, [
      id,
      puzzleData.fen,
      JSON.stringify(puzzleData.solutionMoves || []),
      JSON.stringify(puzzleData.themes || []),
      puzzleData.rating || 1000,
      puzzleData.description || ''
    ]);
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

  async getCustomPuzzles(): Promise<PuzzleResponse[]> {
    const result = await this.db.query(`
      SELECT * FROM puzzles 
      WHERE description LIKE '%custom%' 
      ORDER BY created_at DESC 
      LIMIT 20
    `);
    
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

  // New methods to match frontend expectations
  async getRandomPuzzle(queryParams: any): Promise<PuzzleResponse> {
    const { minRating = 800, maxRating = 2000, themes, limit = 1 } = queryParams;
    
    let query = 'SELECT * FROM puzzles WHERE rating BETWEEN $1 AND $2';
    const params = [minRating, maxRating];
    
    if (themes) {
      const themeArray = Array.isArray(themes) ? themes : themes.split(',');
      query += ' AND themes ILIKE ANY($3)';
      params.push(themeArray.map((theme: string) => `%${theme}%`));
    }
    
    query += ' ORDER BY RANDOM() LIMIT $' + (params.length + 1);
    params.push(limit);
    
    const result = await this.db.query(query, params);
    
    if (!result.rows.length) {
      throw new Error('No puzzles available');
    }
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

  async getPuzzleById(id: string): Promise<PuzzleResponse> {
    const result = await this.db.query('SELECT * FROM puzzles WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Puzzle not found');
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

  async getPuzzles(queryParams: any): Promise<PuzzleResponse[]> {
    const { minRating = 0, maxRating = 3000, themes, limit = 10, offset = 0 } = queryParams;
    
    let query = 'SELECT * FROM puzzles WHERE rating BETWEEN $1 AND $2';
    const params = [minRating, maxRating];
    
    if (themes) {
      const themeArray = Array.isArray(themes) ? themes : themes.split(',');
      query += ' AND themes ILIKE ANY($3)';
      params.push(themeArray.map((theme: string) => `%${theme}%`));
    }
    
    query += ' ORDER BY rating DESC LIMIT $' + (params.length + 1) + ' OFFSET $' + (params.length + 2);
    params.push(limit, offset);
    
    const result = await this.db.query(query, params);
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

  async getPuzzleThemes(): Promise<string[]> {
    const result = await this.db.query(`
      SELECT DISTINCT themes FROM puzzles 
      WHERE themes IS NOT NULL AND themes != ''
      LIMIT 50
    `);
    
    const allThemes = new Set<string>();
    result.rows.forEach(row => {
      try {
        const themes = JSON.parse(row.themes || '[]');
        themes.forEach((theme: string) => allThemes.add(theme));
      } catch (e) {
        // Skip invalid JSON
      }
    });
    
    return Array.from(allThemes).slice(0, 20);
  }

  async getPuzzleStats(): Promise<any> {
    const totalResult = await this.db.query('SELECT COUNT(*) as total FROM puzzles');
    const avgRatingResult = await this.db.query('SELECT AVG(rating) as avg_rating FROM puzzles');
    const minRatingResult = await this.db.query('SELECT MIN(rating) as min_rating FROM puzzles');
    const maxRatingResult = await this.db.query('SELECT MAX(rating) as max_rating FROM puzzles');
    
    return {
      totalPuzzles: parseInt(totalResult.rows[0]?.total || '0'),
      averageRating: Math.round(avgRatingResult.rows[0]?.avg_rating || 0),
      minRating: parseInt(minRatingResult.rows[0]?.min_rating || '0'),
      maxRating: parseInt(maxRatingResult.rows[0]?.max_rating || '0')
    };
  }

  async searchPuzzles(queryParams: any): Promise<PuzzleResponse[]> {
    const { q, limit = 10 } = queryParams;
    
    if (!q) {
      return [];
    }
    
    const result = await this.db.query(`
      SELECT * FROM puzzles 
      WHERE description ILIKE $1 OR themes ILIKE $1
      ORDER BY rating DESC 
      LIMIT $2
    `, [`%${q}%`, limit]);
    
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

  private formatPuzzleResponse(row: any): PuzzleResponse {
    return {
      id: row.id,
      fen: row.fen,
      solution_moves: row.solution_moves ? JSON.parse(row.solution_moves) : [],
      themes: row.themes ? JSON.parse(row.themes) : [],
      rating: row.rating,
      description: row.description,
      created_at: row.created_at
    };
  }
}