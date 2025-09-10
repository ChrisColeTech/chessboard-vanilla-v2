import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { AiopponentResponse, CreateAiopponentRequest, UpdateAiopponentRequest } from '../models/Aiopponent';

export class AiopponentService {
  private db = Database.getInstance();

  async getAllOpponents(): Promise<AiopponentResponse[]> {
    const result = await this.db.query('SELECT * FROM ai_opponents ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAiopponentResponse(row));
  }

  async getOpponentById(id: string): Promise<AiopponentResponse> {
    const result = await this.db.query('SELECT * FROM ai_opponents WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Aiopponent not found');
    
    return this.formatAiopponentResponse(result.rows[0]);
  }

  async getOpponentsByDifficulty(): Promise<AiopponentResponse[]> {
    const result = await this.db.query('SELECT * FROM ai_opponents ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAiopponentResponse(row));
  }

  async createOpponent(data: CreateAiopponentRequest): Promise<AiopponentResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO ai_opponents (id, created_at, updated_at, ...data)
      VALUES ($1, NOW(), NOW(), ...)
      RETURNING *
    `, [id]);
    
    return this.formatAiopponentResponse(result.rows[0]);
  }

  async getAllAi_opponents(): Promise<AiopponentResponse[]> {
    const result = await this.db.query('SELECT * FROM ai_opponents ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatAiopponentResponse(row));
  }

  async getAiopponentById(id: string): Promise<AiopponentResponse> {
    const result = await this.db.query('SELECT * FROM ai_opponents WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Aiopponent not found');
    
    return this.formatAiopponentResponse(result.rows[0]);
  }

  async createAiopponent(data: CreateAiopponentRequest): Promise<AiopponentResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO ai_opponents (id, created_at, updated_at, ...data)
      VALUES ($1, NOW(), NOW(), ...)
      RETURNING *
    `, [id]);
    
    return this.formatAiopponentResponse(result.rows[0]);
  }

  async updateAiopponent(id: string, data: UpdateAiopponentRequest): Promise<AiopponentResponse> {
    const result = await this.db.query(`
      UPDATE ai_opponents 
      SET updated_at = NOW(), ...data
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Aiopponent not found');
    return this.formatAiopponentResponse(result.rows[0]);
  }

  async deleteAiopponent(id: string): Promise<void> {
    await this.db.query('DELETE FROM ai_opponents WHERE id = $1', [id]);
  }

  private formatAiopponentResponse(row: any): AiopponentResponse {
    return {
      id: row.id,
      name: row.name,
      difficulty: row.difficulty,
      elo_rating: row.elo_rating,
      personality: row.personality,
      description: row.description,
      created_at: row.created_at,
    };
  }
}