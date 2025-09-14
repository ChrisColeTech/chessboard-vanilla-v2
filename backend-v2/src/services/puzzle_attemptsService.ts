import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { PuzzleAttemptResponse, CreatePuzzleAttemptRequest, UpdatePuzzleAttemptRequest } from '../models/PuzzleAttempt';

export class PuzzleAttemptService {
  private db = Database.getInstance();

async getPuzzleAttemptById(id: string): Promise<PuzzleAttemptResponse> {
    const result = await this.db.query('SELECT * FROM puzzle_attempts WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('PuzzleAttempt not found');
    
    return this.formatPuzzleAttemptResponse(result.rows[0]);
  }

  async getPuzzleAttemptsByUser(...args: any[]): Promise<any> {
    // Generic implementation for getPuzzleAttemptsByUser
    const result = await this.db.query('SELECT * FROM puzzle_attempts ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleAttemptResponse(row));
  }

async getAllPuzzle_attempts(): Promise<PuzzleAttemptResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzle_attempts ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleAttemptResponse(row));
  }

  async getPuzzleAttemptsByPuzzle(...args: any[]): Promise<any> {
    // Generic implementation for getPuzzleAttemptsByPuzzle
    const result = await this.db.query('SELECT * FROM puzzle_attempts ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleAttemptResponse(row));
  }

async updatePuzzleAttempt(id: string, data: UpdatePuzzleAttemptRequest): Promise<PuzzleAttemptResponse> {
    const result = await this.db.query(`
      UPDATE puzzle_attempts 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('PuzzleAttempt not found');
    return this.formatPuzzleAttemptResponse(result.rows[0]);
  }

async createPuzzleAttempt(data: CreatePuzzleAttemptRequest): Promise<PuzzleAttemptResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO puzzle_attempts (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatPuzzleAttemptResponse(result.rows[0]);
  }

async listPuzzleAttempts(): Promise<PuzzleAttemptResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzle_attempts ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleAttemptResponse(row));
  }

async deletePuzzleAttempt(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM puzzle_attempts WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('PuzzleAttempt not found');
  }

private formatPuzzleAttemptResponse(row: any): PuzzleAttemptResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      puzzle_id: row.puzzle_id,
      solved: row.solved,
      user_moves: row.user_moves,
      time_taken: row.time_taken,
      hints_used: row.hints_used,
      attempt_number: row.attempt_number,
      rating_before: row.rating_before,
      rating_after: row.rating_after,
      rating_change: row.rating_change,
      attempted_at: row.attempted_at,
    };
  }
}