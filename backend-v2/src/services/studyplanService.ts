import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { StudyplanResponse, CreateStudyplanRequest, UpdateStudyplanRequest } from '../models/Studyplan';

export class StudyplanService {
  private db = Database.getInstance();

  async getUserStudyPlans(...args: any[]): Promise<any> {
    // Generic implementation - queries entity table and returns formatted results
    const result = await this.db.query('SELECT * FROM user_study_plans ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStudyplanResponse(row));
  }

  async createStudyPlan(data: CreateStudyplanRequest): Promise<StudyplanResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO user_study_plans (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatStudyplanResponse(result.rows[0]);
  }

  async updatePlan(id: string, data: UpdateStudyplanRequest): Promise<StudyplanResponse> {
    const result = await this.db.query(`
      UPDATE user_study_plans 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Studyplan not found');
    return this.formatStudyplanResponse(result.rows[0]);
  }

  async deletePlan(id: string): Promise<void> {
    await this.db.query('DELETE FROM user_study_plans WHERE id = $1', [id]);
  }

  async getAllStudy_plans(): Promise<StudyplanResponse[]> {
    const result = await this.db.query('SELECT * FROM user_study_plans ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatStudyplanResponse(row));
  }

  async getStudyplanById(id: string): Promise<StudyplanResponse> {
    const result = await this.db.query('SELECT * FROM user_study_plans WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Studyplan not found');
    
    return this.formatStudyplanResponse(result.rows[0]);
  }

  async createStudyplan(data: CreateStudyplanRequest): Promise<StudyplanResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO user_study_plans (id, created_at, updated_at)
      VALUES ($1, NOW(), NOW())
      RETURNING *
    `, [id]);
    
    return this.formatStudyplanResponse(result.rows[0]);
  }

  async updateStudyplan(id: string, data: UpdateStudyplanRequest): Promise<StudyplanResponse> {
    const result = await this.db.query(`
      UPDATE user_study_plans 
      SET updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Studyplan not found');
    return this.formatStudyplanResponse(result.rows[0]);
  }

  async deleteStudyplan(id: string): Promise<void> {
    await this.db.query('DELETE FROM user_study_plans WHERE id = $1', [id]);
  }

  private formatStudyplanResponse(row: any): StudyplanResponse {
    return {
      id: row.id,
      user_id: row.user_id,
      title: row.title,
      goals: row.goals,
      schedule: row.schedule,
      progress: row.progress,
      created_at: row.created_at,
      updated_at: row.updated_at,
    };
  }
}