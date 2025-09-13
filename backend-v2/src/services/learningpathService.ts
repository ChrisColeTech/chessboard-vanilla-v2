import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { LearningPathResponse, CreateLearningPathRequest, UpdateLearningPathRequest } from '../models/LearningPath';

export class LearningPathService {
  private db = Database.getInstance();

  async getLearningPaths(): Promise<LearningPathResponse[]> {
    const result = await this.db.query('SELECT * FROM learning_paths ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningPathResponse(row));
  }

  async getLearningPathById(id: string): Promise<LearningPathResponse> {
    const result = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Learning path not found');
    
    return this.formatLearningPathResponse(result.rows[0]);
  }

  async enrollInPath(pathId: string, userId: string): Promise<any> {
    // First, verify the learning path exists
    const pathResult = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [pathId]);
    if (!pathResult.rows.length) throw new Error('Learning path not found');
    
    // Check if user is already enrolled
    const enrollmentCheck = await this.db.query(
      'SELECT * FROM user_learning_paths WHERE user_id = $1 AND learning_path_id = $2', 
      [userId, pathId]
    );
    
    if (enrollmentCheck.rows.length > 0) {
      throw new Error('User already enrolled in this learning path');
    }
    
    // Create enrollment record
    const enrollmentId = require('uuid').v4();
    await this.db.query(`
      INSERT INTO user_learning_paths (id, user_id, learning_path_id, progress, enrolled_at, created_at, updated_at)
      VALUES ($1, $2, $3, 0, NOW(), NOW(), NOW())
    `, [enrollmentId, userId, pathId]);
    
    // Return the learning path with enrollment status
    const learningPath = this.formatLearningPathResponse(pathResult.rows[0]);
    return {
      ...learningPath,
      enrolled: true,
      progress: 0,
      enrolled_at: new Date().toISOString()
    };
  }

  async updateProgress(pathId: string, userId: string, progressData: any): Promise<any> {
    // Update user's progress in the learning path
    const result = await this.db.query(`
      UPDATE user_learning_paths 
      SET progress = $3, updated_at = NOW()
      WHERE user_id = $1 AND learning_path_id = $2
      RETURNING *
    `, [userId, pathId, progressData.progress || 0]);
    
    if (!result.rows.length) throw new Error('Enrollment not found - user must enroll first');
    
    // Get the learning path details
    const pathResult = await this.db.query('SELECT * FROM learning_paths WHERE id = $1', [pathId]);
    if (!pathResult.rows.length) throw new Error('Learning path not found');
    
    const learningPath = this.formatLearningPathResponse(pathResult.rows[0]);
    return {
      ...learningPath,
      progress: result.rows[0].progress,
      updated_at: result.rows[0].updated_at
    };
  }

  async getAllLearning_paths(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM learning_paths ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatLearningPathResponse(row));
  }

  async createLearningPath(data: CreateLearningPathRequest): Promise<LearningPathResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO learning_paths (id, title, description, difficulty, modules, progress, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
      RETURNING *
    `, [id, data.title, data.description, data.difficulty, JSON.stringify(data.modules || []), data.progress || 0]);
    
    return this.formatLearningPathResponse(result.rows[0]);
  }

  async updateLearningPath(id: string, data: UpdateLearningPathRequest): Promise<LearningPathResponse> {
    const updateFields = [];
    const updateValues = [];
    let paramIndex = 2;
    
    if (data.title) {
      updateFields.push(`title = ${paramIndex}`);
      updateValues.push(data.title);
      paramIndex++;
    }
    if (data.description) {
      updateFields.push(`description = ${paramIndex}`);
      updateValues.push(data.description);
      paramIndex++;
    }
    if (data.difficulty) {
      updateFields.push(`difficulty = ${paramIndex}`);
      updateValues.push(data.difficulty);
      paramIndex++;
    }
    if (data.modules) {
      updateFields.push(`modules = ${paramIndex}`);
      updateValues.push(JSON.stringify(data.modules));
      paramIndex++;
    }
    if (data.progress !== undefined) {
      updateFields.push(`progress = ${paramIndex}`);
      updateValues.push(data.progress);
      paramIndex++;
    }
    
    updateFields.push('updated_at = NOW()');
    
    const query = `UPDATE learning_paths SET ${updateFields.join(', ')} WHERE id = $1 RETURNING *`;
    const result = await this.db.query(query, [id, ...updateValues]);
    
    if (!result.rows.length) throw new Error('LearningPath not found');
    return this.formatLearningPathResponse(result.rows[0]);
  }

  async deleteLearningPath(id: string): Promise<void> {
    await this.db.query('DELETE FROM learning_paths WHERE id = $1', [id]);
  }

  private formatLearningPathResponse(row: any): LearningPathResponse {
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