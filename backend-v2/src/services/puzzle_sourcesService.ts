import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { PuzzleSourceResponse, CreatePuzzleSourceRequest, UpdatePuzzleSourceRequest } from '../models/PuzzleSource';

export class PuzzleSourceService {
  private db = Database.getInstance();

async listPuzzleSources(): Promise<PuzzleSourceResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzle_sources ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleSourceResponse(row));
  }

  async getActivePuzzleSources(...args: any[]): Promise<any> {
    // Generic implementation for getActivePuzzleSources
    const result = await this.db.query('SELECT * FROM puzzle_sources ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleSourceResponse(row));
  }

async updatePuzzleSource(id: string, data: UpdatePuzzleSourceRequest): Promise<PuzzleSourceResponse> {
    const result = await this.db.query(`
      UPDATE puzzle_sources 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('PuzzleSource not found');
    return this.formatPuzzleSourceResponse(result.rows[0]);
  }

async deletePuzzleSource(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM puzzle_sources WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('PuzzleSource not found');
  }

async createPuzzleSource(data: CreatePuzzleSourceRequest): Promise<PuzzleSourceResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO puzzle_sources (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatPuzzleSourceResponse(result.rows[0]);
  }

async getAllPuzzle_sources(): Promise<PuzzleSourceResponse[]> {
    const result = await this.db.query('SELECT * FROM puzzle_sources ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatPuzzleSourceResponse(row));
  }

async getPuzzleSourceById(id: string): Promise<PuzzleSourceResponse> {
    const result = await this.db.query('SELECT * FROM puzzle_sources WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('PuzzleSource not found');
    
    return this.formatPuzzleSourceResponse(result.rows[0]);
  }

private formatPuzzleSourceResponse(row: any): PuzzleSourceResponse {
    return {
      id: row.id,
      name: row.name,
      description: row.description,
      attribution: row.attribution,
      license: row.license,
      source_url: row.source_url,
      total_puzzles: row.total_puzzles,
      average_rating: row.average_rating,
      is_active: row.is_active,
      last_imported: row.last_imported,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}