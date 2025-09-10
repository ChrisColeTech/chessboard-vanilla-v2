import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { TutorialstepResponse, CreateTutorialstepRequest, UpdateTutorialstepRequest } from '../models/Tutorialstep';

export class TutorialstepService {
  private db = Database.getInstance();

  async getStepsByTutorial(): Promise<TutorialstepResponse[]> {
    const result = await this.db.query('SELECT * FROM tutorial_steps ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatTutorialstepResponse(row));
  }

  async getStepById(id: string): Promise<TutorialstepResponse> {
    const result = await this.db.query('SELECT * FROM tutorial_steps WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Tutorialstep not found');
    
    return this.formatTutorialstepResponse(result.rows[0]);
  }

  async completeStep(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM tutorial_steps ORDER BY step_number ASC');
    return result.rows.map(row => this.formatTutorialstepResponse(row));
  }

  async resetTutorial(...args: any[]): Promise<any> {
    const result = await this.db.query('SELECT * FROM tutorial_steps ORDER BY step_number ASC');
    return result.rows.map(row => this.formatTutorialstepResponse(row));
  }

  async getAllTutorial_steps(): Promise<TutorialstepResponse[]> {
    const result = await this.db.query('SELECT * FROM tutorial_steps ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatTutorialstepResponse(row));
  }

  async getTutorialstepById(id: string): Promise<TutorialstepResponse> {
    const result = await this.db.query('SELECT * FROM tutorial_steps WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Tutorialstep not found');
    
    return this.formatTutorialstepResponse(result.rows[0]);
  }

  async createTutorialstep(data: CreateTutorialstepRequest): Promise<TutorialstepResponse> {
    const id = require('uuid').v4();
    const result = await this.db.query(`
      INSERT INTO tutorial_steps (id, created_at, updated_at, ...data)
      VALUES ($1, NOW(), NOW(), ...)
      RETURNING *
    `, [id]);
    
    return this.formatTutorialstepResponse(result.rows[0]);
  }

  async updateTutorialstep(id: string, data: UpdateTutorialstepRequest): Promise<TutorialstepResponse> {
    const result = await this.db.query(`
      UPDATE tutorial_steps 
      SET updated_at = NOW(), ...data
      WHERE id = $1
      RETURNING *
    `, [id]);
    
    if (!result.rows.length) throw new Error('Tutorialstep not found');
    return this.formatTutorialstepResponse(result.rows[0]);
  }

  async deleteTutorialstep(id: string): Promise<void> {
    await this.db.query('DELETE FROM tutorial_steps WHERE id = $1', [id]);
  }

  private formatTutorialstepResponse(row: any): TutorialstepResponse {
    return {
      id: row.id,
      tutorial_id: row.tutorial_id,
      step_number: row.step_number,
      title: row.title,
      content: row.content,
      action_required: row.action_required,
      completed: row.completed,
    };
  }
}