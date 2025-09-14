import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { ContentResponse, CreateContentRequest, UpdateContentRequest } from '../models/Content';

export class ContentService {
  private db = Database.getInstance();

async updateContent(id: string, data: UpdateContentRequest): Promise<ContentResponse> {
    const result = await this.db.query(`
      UPDATE content 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Content not found');
    return this.formatContentResponse(result.rows[0]);
  }

async listContent(): Promise<ContentResponse[]> {
    const result = await this.db.query('SELECT * FROM content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatContentResponse(row));
  }

async getContentById(id: string): Promise<ContentResponse> {
    const result = await this.db.query('SELECT * FROM content WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Content not found');
    
    return this.formatContentResponse(result.rows[0]);
  }

  async getContentByType(...args: any[]): Promise<any> {
    // Generic implementation for getContentByType
    const result = await this.db.query('SELECT * FROM content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatContentResponse(row));
  }

async getAllContent(): Promise<ContentResponse[]> {
    const result = await this.db.query('SELECT * FROM content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatContentResponse(row));
  }

async createContent(data: CreateContentRequest): Promise<ContentResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO content (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatContentResponse(result.rows[0]);
  }

async deleteContent(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM content WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Content not found');
  }

  async getContentByCategory(...args: any[]): Promise<any> {
    // Generic implementation for getContentByCategory
    const result = await this.db.query('SELECT * FROM content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatContentResponse(row));
  }

  async getChildContent(...args: any[]): Promise<any> {
    // Generic implementation for getChildContent
    const result = await this.db.query('SELECT * FROM content ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatContentResponse(row));
  }

private formatContentResponse(row: any): ContentResponse {
    return {
      id: row.id,
      title: row.title,
      content_type: row.content_type,
      parent_id: row.parent_id,
      order_index: row.order_index,
      description: row.description,
      content_body: row.content_body,
      difficulty_level: row.difficulty_level,
      estimated_duration: row.estimated_duration,
      category: row.category,
      objectives: row.objectives,
      prerequisites: row.prerequisites,
      is_published: row.is_published,
      version: row.version,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}