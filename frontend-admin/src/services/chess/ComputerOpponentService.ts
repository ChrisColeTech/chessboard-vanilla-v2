// ComputerOpponentService.ts - Computer opponent logic and behavior
// Phase 5: Business Logic Services - Computer opponent service
import type { 
  ComputerDifficulty, 
  ComputerOpponentConfig, 
  ComputerThinkingState
} from '../../types';
import { 
  getDifficultyConfig,
  getDifficultyDescription
} from '../../constants/chess/computer-difficulty.constants';
import { 
  calculateThinkingTime,
  addNaturalVariation,
  formatEvaluation
} from '../../utils/chess/computer-chess.utils';

export class ComputerOpponentService {
  private currentDifficulty: ComputerDifficulty = 5;
  private thinkingStats = {
    movesCalculated: 0,
    totalThinkingTime: 0,
    averageThinkingTime: 0
  };

  constructor(initialDifficulty: ComputerDifficulty = 5) {
    this.currentDifficulty = initialDifficulty;
  }

  /**
   * Get configuration for current difficulty level
   */
  public getDifficultyConfig(level?: ComputerDifficulty): ComputerOpponentConfig {
    const difficulty = level || this.currentDifficulty;
    return getDifficultyConfig(difficulty);
  }

  /**
   * Calculate search depth based on difficulty
   * Maps 1-10 user scale to appropriate engine search depth
   */
  public calculateSearchDepth(difficulty?: ComputerDifficulty): number {
    const level = difficulty || this.currentDifficulty;
    
    // Map difficulty 1-10 to search depth 1-8
    // Beginner: 1-2, Casual: 3-4, Club: 4-5, Strong: 6-7, Expert: 7-8
    if (level <= 2) return Math.min(1 + level - 1, 2);  // 1-2
    if (level <= 4) return Math.min(2 + level - 3, 4);  // 3-4
    if (level <= 6) return Math.min(4 + level - 5, 5);  // 4-5
    if (level <= 8) return Math.min(6 + level - 7, 7);  // 6-7
    return Math.min(7 + level - 9, 8);                  // 7-8
  }

  /**
   * Generate realistic thinking delay based on difficulty
   * Higher difficulties take longer to maintain realism
   */
  public generateThinkingDelay(difficulty?: ComputerDifficulty): number {
    const level = difficulty || this.currentDifficulty;
    const baseTime = calculateThinkingTime(level);
    
    // Add natural variation to make computer feel more human
    return addNaturalVariation(baseTime, 25); // ±25% variation
  }

  /**
   * Update current difficulty level
   */
  public setDifficulty(level: ComputerDifficulty): void {
    if (level >= 1 && level <= 10) {
      this.currentDifficulty = level;
    } else {
      throw new Error(`Invalid difficulty level: ${level}. Must be between 1 and 10.`);
    }
  }

  /**
   * Get current difficulty level
   */
  public getCurrentDifficulty(): ComputerDifficulty {
    return this.currentDifficulty;
  }

  /**
   * Format computer status message for UI
   */
  public formatComputerStatus(isThinking: boolean, level?: ComputerDifficulty): string {
    const difficulty = level || this.currentDifficulty;
    
    if (!isThinking) {
      return 'Ready to play';
    }
    
    const description = getDifficultyDescription(difficulty);
    return `Thinking... (${description})`;
  }

  /**
   * Create thinking state for UI feedback
   */
  public createThinkingState(isThinking: boolean, expectedDuration?: number): ComputerThinkingState {
    const now = Date.now();
    
    return {
      isThinking,
      startTime: isThinking ? now : undefined,
      expectedDuration: isThinking ? (expectedDuration || this.generateThinkingDelay()) : undefined,
      progress: undefined // Will be updated externally if progress tracking is available
    };
  }

  /**
   * Update thinking statistics
   */
  public updateThinkingStats(thinkingTime: number): void {
    this.thinkingStats.movesCalculated++;
    this.thinkingStats.totalThinkingTime += thinkingTime;
    this.thinkingStats.averageThinkingTime = 
      this.thinkingStats.totalThinkingTime / this.thinkingStats.movesCalculated;
  }

  /**
   * Get computer opponent statistics
   */
  public getStats() {
    return {
      ...this.thinkingStats,
      currentDifficulty: this.currentDifficulty,
      difficultyDescription: getDifficultyDescription(this.currentDifficulty),
      currentSearchDepth: this.calculateSearchDepth()
    };
  }

  /**
   * Reset statistics
   */
  public resetStats(): void {
    this.thinkingStats = {
      movesCalculated: 0,
      totalThinkingTime: 0,
      averageThinkingTime: 0
    };
  }

  /**
   * Validate difficulty level
   */
  public isValidDifficulty(level: number): level is ComputerDifficulty {
    return Number.isInteger(level) && level >= 1 && level <= 10;
  }

  /**
   * Get all available difficulty levels with descriptions
   */
  public getAllDifficultyLevels(): Array<{ level: ComputerDifficulty; description: string; config: ComputerOpponentConfig }> {
    const levels: ComputerDifficulty[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    return levels.map(level => ({
      level,
      description: getDifficultyDescription(level),
      config: getDifficultyConfig(level)
    }));
  }

  /**
   * Get recommended difficulty for different player types
   */
  public getRecommendedDifficulty(playerType: 'beginner' | 'casual' | 'intermediate' | 'advanced' | 'expert'): ComputerDifficulty {
    const recommendations: Record<string, ComputerDifficulty> = {
      'beginner': 1,
      'casual': 3,
      'intermediate': 5,
      'advanced': 7,
      'expert': 9
    };
    
    return recommendations[playerType] || 5;
  }

  /**
   * Calculate expected game duration based on difficulty
   * Higher difficulties generally lead to longer games
   */
  public estimateGameDuration(difficulty?: ComputerDifficulty): number {
    const level = difficulty || this.currentDifficulty;
    
    // Base game duration in minutes
    const baseDuration = 15; 
    
    // Higher difficulties think longer, leading to longer games
    const difficultyMultiplier = 1 + (level - 1) * 0.1;
    
    return Math.floor(baseDuration * difficultyMultiplier);
  }

  /**
   * Format evaluation score for display
   */
  public formatEvaluationScore(centipawns: number): string {
    return formatEvaluation(centipawns);
  }

  /**
   * Determine if computer should resign based on evaluation
   * Only applies to lower difficulty levels for realism
   */
  public shouldResign(evaluation: number, difficulty?: ComputerDifficulty): boolean {
    const level = difficulty || this.currentDifficulty;
    
    // Only lower difficulty levels resign
    if (level > 6) return false;
    
    // Resign threshold varies by difficulty
    // Beginners resign easier, experts never resign
    const resignThresholds: Record<number, number> = {
      1: -800,  // 8 points behind
      2: -900,  // 9 points behind  
      3: -1000, // 10 points behind
      4: -1100, // 11 points behind
      5: -1200, // 12 points behind
      6: -1300  // 13 points behind
    };
    
    const threshold = resignThresholds[level] || -1000;
    return evaluation < threshold;
  }

  /**
   * Get personality traits for different difficulty levels
   * Used for UI messaging and behavior customization
   */
  public getPersonalityTraits(difficulty?: ComputerDifficulty): {
    style: string;
    tendencies: string[];
    weaknesses: string[];
  } {
    const level = difficulty || this.currentDifficulty;
    
    if (level <= 2) {
      return {
        style: "Beginner",
        tendencies: ["Makes basic moves", "Focuses on piece development", "Sometimes misses tactics"],
        weaknesses: ["Tactical oversights", "Endgame knowledge", "Time management"]
      };
    }
    
    if (level <= 4) {
      return {
        style: "Casual Player",
        tendencies: ["Knows basic tactics", "Attempts simple strategies", "Reasonable opening play"],
        weaknesses: ["Complex positions", "Advanced tactics", "Positional understanding"]
      };
    }
    
    if (level <= 6) {
      return {
        style: "Club Player", 
        tendencies: ["Good tactical awareness", "Solid opening knowledge", "Decent endgame play"],
        weaknesses: ["Deep calculations", "Advanced strategy", "Time pressure"]
      };
    }
    
    if (level <= 8) {
      return {
        style: "Strong Player",
        tendencies: ["Strong tactical play", "Good positional sense", "Solid in all phases"],
        weaknesses: ["Rare miscalculations", "Very complex positions"]
      };
    }
    
    return {
      style: "Expert",
      tendencies: ["Excellent calculation", "Deep positional understanding", "Strong in all areas"],
      weaknesses: ["Nearly perfect play"]
    };
  }
}