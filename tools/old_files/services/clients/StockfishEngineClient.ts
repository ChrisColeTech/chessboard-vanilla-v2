// StockfishEngineClient.ts - Stockfish engine communication layer  
// Phase 6: External Communication - Clean interface for computer opponent
import { StockfishService } from '../chess/StockfishService';
import { getStockfishService } from '../chess/stockfish-singleton';
import type { 
  ComputerMoveRequest, 
  ComputerMoveResult,
  ComputerDifficulty,
  ComputerOpponentConfig
} from '../../types';
import { getDifficultyConfig } from '../../constants/chess/computer-difficulty.constants';
import { parseEngineMove, validateMoveFormat } from '../../utils/chess/computer-chess.utils';

export class StockfishEngineClient {
  private stockfishService: StockfishService;
  private currentSkillLevel: number = 8;
  private isInitialized: boolean = false;

  constructor() {
    // Use singleton pattern for HMR safety
    this.stockfishService = getStockfishService();
    this.initializeClient();
  }

  /**
   * Initialize the client and wait for engine to be ready
   */
  private async initializeClient(): Promise<void> {
    try {
      console.log('🤖 [STOCKFISH CLIENT] Initializing Stockfish engine client...');
      
      // Wait for engine to be ready
      await this.stockfishService.waitForReady();
      
      this.isInitialized = true;
      console.log('✅ [STOCKFISH CLIENT] Engine client ready');
    } catch (error) {
      console.error('❌ [STOCKFISH CLIENT] Failed to initialize:', error);
      this.isInitialized = false;
    }
  }

  /**
   * Check if the engine is ready for requests
   */
  public async isReady(): Promise<boolean> {
    if (!this.isInitialized) {
      await this.initializeClient();
    }
    
    return this.stockfishService.isEngineReady();
  }

  /**
   * Request a computer move with difficulty-based configuration
   */
  public async requestMove(request: ComputerMoveRequest): Promise<ComputerMoveResult> {
    try {
      if (!await this.isReady()) {
        return {
          move: '',
          success: false,
          error: 'Engine not ready'
        };
      }

      console.log('🎯 [STOCKFISH CLIENT] Requesting computer move:', request);
      
      // Get difficulty configuration
      const config = getDifficultyConfig(request.difficulty);
      
      // Map user difficulty (1-10) to Stockfish skill level (0-20)
      const skillLevel = config.skillLevel;
      const timeLimit = request.timeLimit || config.timeLimit;
      
      // Set skill level if changed
      if (skillLevel !== this.currentSkillLevel) {
        await this.setSkillLevel(skillLevel);
      }
      
      // Request move from engine
      const moveString = await this.stockfishService.getBestMoveWithPosition(
        request.fen, 
        skillLevel, 
        timeLimit
      );

      if (!moveString) {
        return {
          move: '',
          success: false,
          error: 'Failed to get move from engine'
        };
      }

      // Validate move format
      if (!validateMoveFormat(moveString)) {
        return {
          move: '',
          success: false,
          error: `Invalid move format returned: ${moveString}`
        };
      }

      console.log('✅ [STOCKFISH CLIENT] Computer move calculated:', moveString);
      
      return {
        move: moveString,
        success: true
      };

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('❌ [STOCKFISH CLIENT] Error requesting move:', errorMessage);
      
      return {
        move: '',
        success: false,
        error: errorMessage
      };
    }
  }

  /**
   * Simplified move request with just FEN and difficulty
   */
  public async getBestMove(fen: string, difficulty: ComputerDifficulty, timeLimit?: number): Promise<string | null> {
    const request: ComputerMoveRequest = {
      fen,
      difficulty,
      timeLimit
    };

    const result = await this.requestMove(request);
    return result.success ? result.move : null;
  }

  /**
   * Set engine skill level (0-20 Stockfish scale)
   */
  public async setSkillLevel(skillLevel: number): Promise<void> {
    try {
      if (!await this.isReady()) {
        throw new Error('Engine not ready');
      }

      // Clamp skill level to valid range
      const clampedLevel = Math.max(0, Math.min(20, skillLevel));
      
      if (clampedLevel !== this.currentSkillLevel) {
        console.log(`🔧 [STOCKFISH CLIENT] Setting skill level: ${clampedLevel}`);
        
        // Update skill level through the service's public method
        await this.stockfishService.setSkillLevel(clampedLevel);
        
        this.currentSkillLevel = clampedLevel;
        console.log('✅ [STOCKFISH CLIENT] Skill level updated');
      }
    } catch (error) {
      console.error('❌ [STOCKFISH CLIENT] Failed to set skill level:', error);
      throw error;
    }
  }

  /**
   * Set user-friendly difficulty level (1-10)
   */
  public async setDifficulty(difficulty: ComputerDifficulty): Promise<void> {
    const config = getDifficultyConfig(difficulty);
    await this.setSkillLevel(config.skillLevel);
  }

  /**
   * Evaluate current position
   */
  public async evaluatePosition(fen: string, depth: number = 15): Promise<number> {
    try {
      if (!await this.isReady()) {
        console.warn('⚠️ [STOCKFISH CLIENT] Engine not ready for evaluation');
        return 0;
      }

      return await this.stockfishService.evaluatePosition(fen, depth);
    } catch (error) {
      console.error('❌ [STOCKFISH CLIENT] Error evaluating position:', error);
      return 0;
    }
  }

  /**
   * Get current engine statistics  
   */
  public getStats() {
    return {
      isReady: this.stockfishService.isEngineReady(),
      currentSkillLevel: this.currentSkillLevel,
      isInitialized: this.isInitialized
    };
  }

  /**
   * Parse a UCI move string into components
   */
  public parseMove(moveString: string) {
    try {
      return parseEngineMove(moveString);
    } catch (error) {
      console.error('❌ [STOCKFISH CLIENT] Error parsing move:', error);
      return null;
    }
  }

  /**
   * Validate move format
   */
  public isValidMoveFormat(moveString: string): boolean {
    return validateMoveFormat(moveString);
  }

  /**
   * Get difficulty configuration for a level
   */
  public getDifficultyConfig(difficulty: ComputerDifficulty): ComputerOpponentConfig {
    return getDifficultyConfig(difficulty);
  }

  /**
   * Wait for engine to be ready with timeout
   */
  public async waitForReady(timeoutMs: number = 10000): Promise<void> {
    const startTime = Date.now();
    
    while (!await this.isReady() && (Date.now() - startTime) < timeoutMs) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    if (!await this.isReady()) {
      throw new Error(`Engine failed to become ready within ${timeoutMs}ms`);
    }
  }

  /**
   * Get current skill level
   */
  public getCurrentSkillLevel(): number {
    return this.currentSkillLevel;
  }

  /**
   * Get user-friendly difficulty level from current skill level
   */
  public getCurrentDifficulty(): ComputerDifficulty {
    // Convert Stockfish skill level back to user difficulty level
    // This is an approximation since multiple user levels may map to same skill level
    const skillToUserLevel: Record<number, ComputerDifficulty> = {
      0: 1, 2: 2, 4: 3, 6: 4, 8: 5, 
      10: 6, 12: 7, 14: 8, 16: 9, 18: 10
    };
    
    return skillToUserLevel[this.currentSkillLevel] || 5;
  }

  /**
   * Restart the engine (for debugging or error recovery)
   */
  public async restart(): Promise<void> {
    console.log('🔄 [STOCKFISH CLIENT] Restarting engine...');
    
    // Reinitialize the client
    this.isInitialized = false;
    await this.initializeClient();
  }

  /**
   * Cleanup method
   */
  public destroy(): void {
    console.log('🧹 [STOCKFISH CLIENT] Cleaning up client...');
    // The singleton service handles its own lifecycle
    this.isInitialized = false;
  }
}