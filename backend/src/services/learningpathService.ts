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

  async enrollInPath(...args: any[]): Promise<any> {
    // TODO: Implement enrollInPath
    throw new Error('enrollInPath not implemented');
  }

  async updateProgress(...args: any[]): Promise<any> {
    // TODO: Implement updateProgress
    throw new Error('updateProgress not implemented');
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