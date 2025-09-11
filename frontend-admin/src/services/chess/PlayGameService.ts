// PlayGameService.ts - Core play game business logic
// Phase 5: Business Logic Services - Play game service
import { ChessGameService } from './ChessGameService';
import type { 
  ChessGameState, 
  ChessMoveResult, 
  PieceType,
  PieceColor,
  PlayGameState,
  ComputerDifficulty,
  ComputerThinkingState
} from '../../types';

export class PlayGameService {
  private chessGameService: ChessGameService;
  private currentPlayer: PieceColor = 'white';
  private playerColor: PieceColor = 'white';
  private computerColor: PieceColor = 'black';
  private gameMode: 'human-vs-computer' | 'human-vs-human' = 'human-vs-computer';
  private difficulty: ComputerDifficulty = 5;
  private thinkingState: ComputerThinkingState = {
    isThinking: false
  };

  constructor(playerColor: PieceColor = 'white') {
    this.chessGameService = new ChessGameService();
    this.playerColor = playerColor;
    this.computerColor = playerColor === 'white' ? 'black' : 'white';
  }

  /**
   * Make a move as the human player with turn validation
   */
  public makePlayerMove(from: string, to: string, promotion?: PieceType): ChessMoveResult {
    if (!this.isPlayerTurn()) {
      return { 
        success: false, 
        error: 'Not your turn - wait for computer move',
        gameState: this.getCurrentState() 
      };
    }
    
    if (this.thinkingState.isThinking) {
      return {
        success: false,
        error: 'Computer is thinking - please wait',
        gameState: this.getCurrentState()
      };
    }
    
    const result = this.chessGameService.makeMove({ from, to, promotion });
    
    if (result.success) {
      // Switch turns only on successful moves
      this.switchTurn();
    }
    
    return result;
  }

  /**
   * Execute a computer move (used internally)
   */
  public makeComputerMove(from: string, to: string, promotion?: PieceType): ChessMoveResult {
    if (this.isPlayerTurn()) {
      return {
        success: false,
        error: 'Not computer turn',
        gameState: this.getCurrentState()
      };
    }

    const result = this.chessGameService.makeMove({ from, to, promotion });
    
    if (result.success) {
      this.switchTurn();
    }
    
    return result;
  }

  /**
   * Check if it's currently the human player's turn
   */
  public isPlayerTurn(): boolean {
    return this.currentPlayer === this.playerColor;
  }

  /**
   * Check if it's currently the computer's turn
   */
  public isComputerTurn(): boolean {
    return this.currentPlayer === this.computerColor && this.gameMode === 'human-vs-computer';
  }

  /**
   * Switch to the next player's turn
   */
  public switchTurn(): void {
    this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
  }

  /**
   * Get current chess game state
   */
  public getCurrentState(): ChessGameState {
    return this.chessGameService.getCurrentState();
  }

  /**
   * Get complete play game state including computer info
   */
  public getPlayGameState(): PlayGameState {
    const gameState = this.getCurrentState();
    
    return {
      gameState,
      currentPlayer: this.currentPlayer,
      playerColor: this.playerColor,
      computerColor: this.computerColor,
      gameMode: this.gameMode,
      difficulty: this.difficulty,
      isComputerTurn: this.isComputerTurn(),
      thinkingState: this.thinkingState,
      settings: {
        playerColor: this.playerColor,
        difficulty: this.difficulty,
        computerTimeLimit: 2000,
        audioEnabled: true,
        showMoveHints: true,
        highlightLastMove: true,
        boardOrientation: this.playerColor
      }
    };
  }

  /**
   * Get valid moves for a square or all valid moves
   */
  public getValidMoves(square?: string): string[] {
    return this.chessGameService.getValidMoves(square);
  }

  /**
   * Get valid target squares for a specific piece
   */
  public getValidTargetSquares(square: string): string[] {
    return this.chessGameService.getValidTargetSquares(square);
  }

  /**
   * Reset/restart the game
   */
  public resetGame(fen?: string): void {
    this.chessGameService.resetGame(fen);
    this.currentPlayer = 'white';
    this.thinkingState = { isThinking: false };
  }

  /**
   * Update computer difficulty level
   */
  public updateDifficulty(level: ComputerDifficulty): void {
    this.difficulty = level;
  }

  /**
   * Update computer thinking state
   */
  public setThinkingState(thinkingState: Partial<ComputerThinkingState>): void {
    this.thinkingState = { ...this.thinkingState, ...thinkingState };
  }

  /**
   * Flip player and computer colors
   */
  public flipColors(): void {
    const oldPlayerColor = this.playerColor;
    this.playerColor = this.computerColor;
    this.computerColor = oldPlayerColor;
    
    // Don't change the current turn - game continues with same side to move
  }

  /**
   * Get current FEN position
   */
  public getFen(): string {
    return this.chessGameService.getFen();
  }

  /**
   * Get current PGN
   */
  public getPgn(): string {
    return this.chessGameService.getPgn();
  }

  /**
   * Undo the last move (if supported)
   */
  public undoLastMove(): boolean {
    const success = this.chessGameService.undoLastMove();
    if (success) {
      // Switch back to previous turn
      this.switchTurn();
      // Clear thinking state
      this.thinkingState = { isThinking: false };
    }
    return success;
  }

  /**
   * Check if the player can currently make a move
   */
  public canPlayerMakeMove(): boolean {
    const gameState = this.getCurrentState();
    return !gameState.isGameOver && 
           this.isPlayerTurn() && 
           !this.thinkingState.isThinking;
  }

  /**
   * Check if the computer should make a move
   */
  public shouldComputerMove(): boolean {
    const gameState = this.getCurrentState();
    return !gameState.isGameOver &&
           this.isComputerTurn() &&
           !this.thinkingState.isThinking;
  }

  /**
   * Get game settings
   */
  public getDifficulty(): ComputerDifficulty {
    return this.difficulty;
  }

  /**
   * Get player colors
   */
  public getPlayerColor(): PieceColor {
    return this.playerColor;
  }

  public getComputerColor(): PieceColor {
    return this.computerColor;
  }

  /**
   * Get current thinking state
   */
  public getThinkingState(): ComputerThinkingState {
    return { ...this.thinkingState };
  }
}