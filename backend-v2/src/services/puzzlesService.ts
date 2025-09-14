import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { PuzzleResponse, CreatePuzzleRequest, UpdatePuzzleRequest } from '../models/Puzzle';

export class PuzzleService {
  private db = Database.getInstance();

  async getPuzzlesByTheme(...args: any[]): Promise<any> {
    // Generic implementation for getPuzzlesByTheme
    const result = await this.db.query('SELECT * FROM puzzles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

async updatePuzzle(id: string, data: UpdatePuzzleRequest): Promise<PuzzleResponse> {
    const result = await this.db.query(`
      UPDATE puzzles 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Puzzle not found');
    return this.formatPuzzleResponse(result.rows[0]);
  }

async getAllPuzzles(): Promise<PuzzleResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

async deletePuzzle(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM puzzles WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Puzzle not found');
  }

async getPuzzleById(id: string): Promise<PuzzleResponse> {
    const result = await this.db.query('SELECT * FROM puzzles WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Puzzle not found');
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

async listPuzzles(): Promise<PuzzleResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

async createPuzzle(data: CreatePuzzleRequest): Promise<PuzzleResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO puzzles (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatPuzzleResponse(result.rows[0]);
  }

  async getRandomPuzzle(...args: any[]): Promise<any> {
    // Generic implementation for getRandomPuzzle
    const result = await this.db.query('SELECT * FROM puzzles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

  async getPuzzlesByRating(...args: any[]): Promise<any> {
    // Generic implementation for getPuzzlesByRating
    const result = await this.db.query('SELECT * FROM puzzles ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleResponse(row));
  }

private formatPuzzleResponse(row: any): PuzzleResponse {
    return {
      id: row.id,
      source_id: row.source_id,
      fen: row.fen,
      moves: row.moves,
      rating: row.rating,
      themes: row.themes ? JSON.parse(row.themes) : [],
      opening_family: row.opening_family,
      game_phase: row.game_phase,
      popularity: row.popularity,
      play_count: row.play_count,
      success_rate: row.success_rate,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}