import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { LearningmoduleResponse, CreateLearningmoduleRequest, UpdateLearningmoduleRequest } from '../models/Learningmodule';

export class LearningmoduleService {
  private db = Database.getInstance();

  async getModulesByPath(): Promise<LearningmoduleResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_modules ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningmoduleResponse(row));
  }

  async getModuleById(id: string): Promise<LearningmoduleResponse> {
    const result = await this.db.query('SELECT * FROM learning_modules WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learningmodule not found');
    
    return this.formatLearningmoduleResponse(result.rows[0]);
  }

  async completeModule(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM learning_modules ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningmoduleResponse(row));
  }

  async getAllLearning_modules(): Promise<LearningmoduleResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_modules ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningmoduleResponse(row));
  }

  async getLearningmoduleById(id: string): Promise<LearningmoduleResponse> {
    const result = await this.db.query('SELECT * FROM learning_modules WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learningmodule not found');
    
    return this.formatLearningmoduleResponse(result.rows[0]);
  }

  async createLearningmodule(data: CreateLearningmoduleRequest): Promise<LearningmoduleResponse> {
    const id = uuidv4();
    const result = await this.db.query(`
      INSERT INTO learning_modules (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatLearningmoduleResponse(result.rows[0]);
  }

  async updateLearningmodule(id: string, data: UpdateLearningmoduleRequest): Promise<LearningmoduleResponse> {
    const result = await this.db.query(`
      UPDATE learning_modules 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Learningmodule not found');
    return this.formatLearningmoduleResponse(result.rows[0]);
  }

  async deleteLearningmodule(id: string): Promise<void> {
    const result = await this.db.query('DELETE FROM learning_modules WHERE id = $1', [id]);
    if (result.rowCount === 0) throw new Error('Learningmodule not found');
  }

  private formatLearningmoduleResponse(row: any): LearningmoduleResponse {
    return {
      id: row.id,
      title: row.title,
      description: row.description,
      content: row.content,
      difficulty: row.difficulty,
      order: row.order,
      learning_path_id: row.learning_path_id,
      created_at: row.created_at,
    };
  }
}