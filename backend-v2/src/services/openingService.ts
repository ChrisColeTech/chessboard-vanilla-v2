import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { OpeningResponse, CreateOpeningRequest, UpdateOpeningRequest } from '../models/Opening';

export class OpeningService {
  private db = Database.getInstance();

  async getAllOpenings(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

  async getOpeningByEco(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

  async getOpeningByName(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

  async getPopularOpenings(): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

  async searchOpenings(...args: any[]): Promise<OpeningResponse[]> {
    const result = await this.db.query('SELECT * FROM openings ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatOpeningResponse(row));
  }

  async getOpeningById(id: string): Promise<OpeningResponse> {
    const result = await this.db.query('SELECT * FROM openings WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Opening not found');
    
    return this.formatOpeningResponse(result.rows[0]);
  }

  async createOpening(data: CreateOpeningRequest): Promise<OpeningResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO openings (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatOpeningResponse(result.rows[0]);
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

  async deleteOpening(id: string): Promise<void> {
    await this.db.query('DELETE FROM openings WHERE id = $1', [id]);
  }

  private formatOpeningResponse(row: any): OpeningResponse {
    return {
      id: row.id,
      name: row.name,
      eco_code: row.eco_code,
      moves: row.moves,
      description: row.description,
      popularity: row.popularity,
      created_at: row.created_at,
    };
  }
}