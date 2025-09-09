import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { TutorialResponse, CreateTutorialRequest, UpdateTutorialRequest } from '../models/Tutorial';

export class TutorialService {
  private db = Database.getInstance();

  async getTutorials(): Promise<TutorialResponse[]> {
    const result = await this.db.query('SELECT * FROM tutorials ORDER BY created_at DESC LIMIT 50');
    return result.rows.map(row => this.formatTutorialResponse(row));
  }

  async getTutorialById(id: string): Promise<TutorialResponse> {
    const result = await this.db.query('SELECT * FROM tutorials WHERE id = $1', [id]);
    if (!result.rows.length) throw new Error('Tutorial not found');
    
    return this.formatTutorialResponse(result.rows[0]);
  }

  async completeTutorial(...args: any[]): Promise<any> {
    // TODO: Implement completeTutorial
    throw new Error('completeTutorial not implemented');
  }

  private formatTutorialResponse(row: any): TutorialResponse {
    return {
      id: row.id,
      title: row.title,
      description: row.description,
      content: row.content,
      difficulty: row.difficulty,
      duration: row.duration,
      completed: row.completed,
      created_at: row.created_at,
    };
  }
}