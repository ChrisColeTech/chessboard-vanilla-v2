import { v4 as uuidv4 } from 'uuid';
import { Database } from '../utils/database';
import { StatsResponse, CreateStatsRequest, UpdateStatsRequest } from '../models/Stats';

export class StatsService {
  private db = Database.getInstance();

  async getOverviewStats(userId: string): Promise<StatsResponse> {
    // Get user progress from user_progress table or create default stats
    let progressResult = await this.db.query(
      'SELECT * FROM user_progress WHERE user_id = $1', 
      [userId]
    );

    if (!progressResult.rows.length) {
      // Create default progress if it doesn't exist
      const progressId = uuidv4();
      await this.db.query(`
        INSERT INTO user_progress 
        (id, user_id, puzzles_solved, puzzles_correct, current_streak, best_streak, 
         total_time_spent, achievements_unlocked, created_at, updated_at)
        VALUES ($1, $2, 0, 0, 0, 0, 0, '[]', NOW(), NOW())
      `, [progressId, userId]);
      
      progressResult = await this.db.query(
        'SELECT * FROM user_progress WHERE user_id = $1',
        [userId]
      );
    }

    const progress = progressResult.rows[0];
    const accuracy = progress.puzzles_solved > 0 ? (progress.puzzles_correct / progress.puzzles_solved) * 100 : 0;
    const avgTime = progress.total_time_spent / Math.max(progress.puzzles_solved, 1);

    return this.formatStatsResponse({
      user_id: userId,
      total_puzzles: progress.puzzles_solved,
      correct_puzzles: progress.puzzles_correct,
      puzzle_accuracy: accuracy,
      avg_solve_time: avgTime,
      current_rating: 1000, // Default rating
      games_played: 0,
      games_won: 0,
      win_rate: 0
    });
  }

  async getPuzzleStats(userId: string): Promise<StatsResponse> {
    return this.getOverviewStats(userId);
  }

  async getGameStats(userId: string): Promise<StatsResponse> {
    return this.getOverviewStats(userId);
  }

  async getProgressStats(userId: string): Promise<StatsResponse> {
    return this.getOverviewStats(userId);
  }

  async getPerformanceStats(userId: string): Promise<StatsResponse> {
    return this.getOverviewStats(userId);
  }

  async getRatingStats(userId: string): Promise<StatsResponse> {
    return this.getOverviewStats(userId);
  }

  private formatStatsResponse(row: any): StatsResponse {
    return {
      user_id: row.user_id,
      total_puzzles: row.total_puzzles,
      correct_puzzles: row.correct_puzzles,
      puzzle_accuracy: row.puzzle_accuracy,
      avg_solve_time: row.avg_solve_time,
      current_rating: row.current_rating,
      games_played: row.games_played,
      games_won: row.games_won,
      win_rate: row.win_rate,
    };
  }
}