import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { LearningpathResponse, CreateLearningpathRequest, UpdateLearningpathRequest } from '../models/Learningpath';

export class LearningpathService {
  private db = Database.getInstance();

  async getLearningPaths(): Promise<LearningpathResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_paths ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningpathResponse(row));
  }

  async getLearningPathById(id: string): Promise<LearningpathResponse> {
    const result = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learningpath not found');
    
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async enrollInPath(userId: string, data: any): Promise<LearningpathResponse> {
    const result = await this.db.query(`
      UPDATE learning_paths 
      SET updated_at = NOW()
      WHERE user_id = $1
      RETURNING *
    `, [userId]);
    
    if (!result.rows.length) throw new Error('Learningpath not found');
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async updateProgress(id: string, data: UpdateLearningpathRequest): Promise<LearningpathResponse> {
    const result = await this.db.query(`
      UPDATE learning_paths 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Learningpath not found');
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async getAllLearning_paths(): Promise<LearningpathResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_paths ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningpathResponse(row));
  }

  async getLearningpathById(id: string): Promise<LearningpathResponse> {
    const result = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learningpath not found');
    
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async createLearningpath(data: CreateLearningpathRequest): Promise<LearningpathResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO learning_paths (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async updateLearningpath(id: string, data: UpdateLearningpathRequest): Promise<LearningpathResponse> {
    const result = await this.db.query(`
      UPDATE learning_paths 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Learningpath not found');
    return this.formatLearningpathResponse(result.rows[0]);
  }

  async deleteLearningpath(id: string): Promise<void> {
    await this.db.query('DELETE FROM learning_paths WHERE id = $1', [id]);
  }

  private formatLearningpathResponse(row: any): LearningpathResponse {
    return {
      id: row.id,
      title: row.title,
      description: row.description,
      difficulty: row.difficulty,
      modules: row.modules,
      progress: row.progress,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}