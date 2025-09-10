import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { HelpResponse, CreateHelpRequest, UpdateHelpRequest } from '../models/Help';

export class HelpService {
  private db = Database.getInstance();

  async getAllHelp(): Promise<HelpResponse[]> {
    const result = await this.db.query('SELECT * FROM help_content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHelpResponse(row));
  }

  async getHelpByCategory(): Promise<HelpResponse[]> {
    const result = await this.db.query('SELECT * FROM help_content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHelpResponse(row));
  }

  async searchHelp(...args: any[]): Promise<HelpResponse[]> {
    const result = await this.db.query('SELECT * FROM help_content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatHelpResponse(row));
  }

  async getHelpById(id: string): Promise<HelpResponse> {
    const result = await this.db.query('SELECT * FROM help_content WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Help not found');
    
    return this.formatHelpResponse(result.rows[0]);
  }

  async createHelp(data: CreateHelpRequest): Promise<HelpResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO help_content (id, created_at, updated_at, ...data)
      VALUES ($1, NOW(), NOW(), ...)
      RETURNING *
    `, [id]);
    
    return this.formatHelpResponse(result.rows[0]);
  }

  async updateHelp(id: string, data: UpdateHelpRequest): Promise<HelpResponse> {
    const result = await this.db.query(`
      UPDATE help_content 
      SET updated_at = NOW(), ...data
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Help not found');
    return this.formatHelpResponse(result.rows[0]);
  }

  async deleteHelp(id: string): Promise<void> {
    await this.db.query('DELETE FROM help_content WHERE id = $1', [id]);
  }

  private formatHelpResponse(row: any): HelpResponse {
    return {
      id: row.id,
      category: row.category,
      title: row.title,
      content: row.content,
      tags: row.tags,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}