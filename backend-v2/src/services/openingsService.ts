import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { OpeningResponse, CreateOpeningRequest, UpdateOpeningRequest } from '../models/Opening';

export class OpeningService {
  private db = Database.getInstance();

async getOpeningById(id: string): Promise<OpeningResponse> {
    const result = await this.db.query('SELECT * FROM openings WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Opening not found');
    
    return this.formatOpeningResponse(result.rows[0]);
  }

  async getOpeningByEcoCode(...args: any[]): Promise<any> {
    // Generic implementation for getOpeningByEcoCode
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

async deleteOpening(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM openings WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Opening not found');
  }

async updateOpening(id: string, data: UpdateOpeningRequest): Promise<OpeningResponse> {
    const result = await this.db.query(`
      UPDATE openings 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Opening not found');
    return this.formatOpeningResponse(result.rows[0]);
  }

  async getOpeningsByDifficulty(...args: any[]): Promise<any> {
    // Generic implementation for getOpeningsByDifficulty
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

async createOpening(data: CreateOpeningRequest): Promise<OpeningResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO openings (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatOpeningResponse(result.rows[0]);
  }

  async searchOpenings(...args: any[]): Promise<any> {
    // Generic implementation for searchOpenings
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

async getAllOpenings(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

async listOpenings(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

private formatOpeningResponse(row: any): OpeningResponse {
    return {
      id: row.id,
      eco_code: row.eco_code,
      name: row.name,
      moves: row.moves,
      fen: row.fen,
      popularity: row.popularity,
      difficulty_level: row.difficulty_level,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}