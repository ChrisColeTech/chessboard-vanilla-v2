// MobileChessGameService.ts - Mobile-optimized chess game service
// Phase 2: Mobile Chess Game Service - 8x8 chess with mobile optimizations

import { Chess } from 'chess.js';
import type { 
  ChessGameState, 
  ChessMove, 
  ChessMoveInput, 
  ChessPiece, 
  ChessPosition,
  PieceColor,
  PieceType,
  MobileChessConfig,
  MobileChessGameState,
  MobileBoardState,
  MobileChessMoveResult,
  MobileChessInteraction
} from '../../types';

import { DEFAULT_MOBILE_CHESS_CONFIG } from '../../types';
import { squareToPosition } from '../../utils';

/**
 * Mobile-optimized chess game service
 * Extends standard chess with mobile-specific features and optimizations
 */
export class MobileChessGameService {
  private gameEngine: Chess;
  private moveHistory: ChessMove[] = [];
  private mobileConfig: MobileChessConfig;
  private mobileState: MobileBoardState;
  private interactionHistory: MobileChessInteraction[] = [];

  constructor(
    initialFen?: string, 
    mobileConfig: Partial<MobileChessConfig> = {}
  ) {
    this.gameEngine = new Chess(initialFen);
    this.mobileConfig = { ...DEFAULT_MOBILE_CHESS_CONFIG, ...mobileConfig };
    this.mobileState = this.createInitialMobileState();
  }

  /**
   * Create initial mobile board state
   */
  private createInitialMobileState(): MobileBoardState {
    return {
      selectedSquare: null,
      validMoves: [],
      lastMove: null,
      highlightedSquares: [],
      isPlayerTurn: true,
      isBoardFlipped: false,
      animatingMove: null
    };
  }

  /**
   * Get current mobile chess game state
   */
  public getMobileGameState(): MobileChessGameState {
    const baseState = this.getCurrentChessState();
    return {
      ...baseState,
      mobileState: { ...this.mobileState },
      mobileConfig: { ...this.mobileConfig },
      interactionHistory: [...this.interactionHistory]
    };
  }

  /**
   * Get current standard chess state
   */
  private getCurrentChessState(): ChessGameState {
    const position = new Map<string, ChessPiece>();
    const board: Record<string, ChessPiece | null> = {};

    // Convert chess.js board to our format
    const chessBoard = this.gameEngine.board();
    
    for (let rank = 0; rank < 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const square = String.fromCharCode(97 + file) + (8 - rank); // a8, b8, etc.
        const piece = chessBoard[rank][file];
        
        if (piece) {
          const chessPiece: ChessPiece = {
            id: `${piece.color}-${piece.type}-${square}`,
            type: piece.type as PieceType,
            color: piece.color as PieceColor,
            position: squareToPosition(square)
          };
          position.set(square, chessPiece);
          board[square] = chessPiece;
        } else {
          board[square] = null;
        }
      }
    }

    // Get castling rights
    const castlingRights = {
      white: {
        kingSide: this.gameEngine.getCastlingRights('w').k,
        queenSide: this.gameEngine.getCastlingRights('w').q
      },
      black: {
        kingSide: this.gameEngine.getCastlingRights('b').k,
        queenSide: this.gameEngine.getCastlingRights('b').q
      }
    };

    return {
      position,
      board,
      activeColor: this.gameEngine.turn() === 'w' ? 'white' : 'black',
      castlingRights,
      enPassantTarget: this.getEnPassantTarget(),
      halfmoveClock: this.getHalfmoveClock(),
      fullmoveNumber: this.getFullmoveNumber(),
      isCheck: this.gameEngine.inCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      isStalemate: this.gameEngine.isStalemate(),
      isDraw: this.gameEngine.isDraw(),
      isGameOver: this.gameEngine.isGameOver(),
      fen: this.gameEngine.fen(),
      history: [...this.moveHistory],
      lastMove: this.getLastMove()
    };
  }

  /**
   * Get last move in our format
   */
  private getLastMove(): { from: string; to: string } | undefined {
    const history = this.gameEngine.history({ verbose: true });
    if (history.length === 0) return undefined;
    
    const lastMove = history[history.length - 1];
    return {
      from: lastMove.from,
      to: lastMove.to
    };
  }

  /**
   * Make a move with mobile-specific validation and feedback
   */
  public makeMobileMove(moveInput: ChessMoveInput): MobileChessMoveResult {
    try {
      // Validate move using chess.js
      const move = this.gameEngine.move({
        from: moveInput.from,
        to: moveInput.to,
        promotion: moveInput.promotion ? moveInput.promotion[0] : undefined
      }) as any;

      if (!move) {
        return {
          isValid: false,
          move: null,
          gameState: this.getMobileGameState(),
          error: 'Invalid move',
          feedback: {
            playSuccessSound: false,
            playErrorSound: true,
            triggerHaptic: false,
            visualFeedback: 'error'
          }
        };
      }

      // Convert chess.js move to our format
      const chessMove = this.convertMove(move);
      this.moveHistory.push(chessMove);

      // Update mobile state
      this.updateMobileStateAfterMove(moveInput.from, moveInput.to, chessMove);

      // Determine feedback type
      const gameState = this.getMobileGameState();
      let visualFeedback: 'none' | 'success' | 'error' | 'check' | 'checkmate' = 'success';
      
      if (gameState.isCheckmate) {
        visualFeedback = 'checkmate';
      } else if (gameState.isCheck) {
        visualFeedback = 'check';
      }

      return {
        isValid: true,
        move: chessMove,
        gameState,
        error: null,
        feedback: {
          playSuccessSound: true,
          playErrorSound: false,
          triggerHaptic: this.mobileConfig.enableHapticFeedback,
          visualFeedback
        }
      };

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      return {
        isValid: false,
        move: null,
        gameState: this.getMobileGameState(),
        error: errorMessage,
        feedback: {
          playSuccessSound: false,
          playErrorSound: true,
          triggerHaptic: false,
          visualFeedback: 'error'
        }
      };
    }
  }

  /**
   * Get en passant target square from FEN
   */
  private getEnPassantTarget(): ChessPosition | undefined {
    const fen = this.gameEngine.fen();
    const enPassantSquare = fen.split(' ')[3];
    
    if (enPassantSquare === '-') {
      return undefined;
    }
    
    return enPassantSquare as ChessPosition;
  }

  /**
   * Get half move clock from FEN
   */
  private getHalfmoveClock(): number {
    const fen = this.gameEngine.fen();
    const parts = fen.split(' ');
    return parseInt(parts[4]) || 0;
  }

  /**
   * Get full move number from FEN
   */
  private getFullmoveNumber(): number {
    const fen = this.gameEngine.fen();
    const parts = fen.split(' ');
    return parseInt(parts[5]) || 1;
  }

  /**
   * Update mobile state after a successful move
   */
  private updateMobileStateAfterMove(from: ChessPosition, to: ChessPosition, _move: ChessMove): void {
    this.mobileState = {
      ...this.mobileState,
      selectedSquare: null,
      validMoves: [],
      lastMove: { from, to },
      highlightedSquares: this.gameEngine.inCheck() ? this.getCheckHighlights() : [],
      animatingMove: null // Animation will be handled by UI layer
    };
  }

  /**
   * Get squares to highlight when in check
   */
  private getCheckHighlights(): ChessPosition[] {
    if (!this.gameEngine.inCheck()) return [];

    // Find the king position
    const color = this.gameEngine.turn();
    const board = this.gameEngine.board();
    
    for (let rank = 0; rank < 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const piece = board[rank][file];
        if (piece && piece.type === 'k' && piece.color === color) {
          const square = String.fromCharCode(97 + file) + (8 - rank);
          return [square as ChessPosition];
        }
      }
    }
    return [];
  }

  /**
   * Convert chess.js move to our ChessMove format
   */
  private convertMove(chessJsMove: any): ChessMove {
    return {
      from: chessJsMove.from,
      to: chessJsMove.to,
      piece: {
        id: `${chessJsMove.color}-${chessJsMove.piece}-${chessJsMove.from}`,
        type: chessJsMove.piece as PieceType,
        color: chessJsMove.color === 'w' ? 'white' : 'black',
        position: squareToPosition(chessJsMove.from)
      },
      capturedPiece: chessJsMove.captured ? {
        id: `${chessJsMove.color === 'w' ? 'b' : 'w'}-${chessJsMove.captured}-${chessJsMove.to}`,
        type: chessJsMove.captured as PieceType,
        color: chessJsMove.color === 'w' ? 'black' : 'white',
        position: squareToPosition(chessJsMove.to)
      } : undefined,
      captured: chessJsMove.captured ? {
        id: `${chessJsMove.color === 'w' ? 'b' : 'w'}-${chessJsMove.captured}-${chessJsMove.to}`,
        type: chessJsMove.captured as PieceType,
        color: chessJsMove.color === 'w' ? 'black' : 'white',
        position: squareToPosition(chessJsMove.to)
      } : undefined,
      promotion: chessJsMove.promotion as PieceType | undefined,
      isCheck: this.gameEngine.inCheck(),
      isCheckmate: this.gameEngine.isCheckmate(),
      notation: chessJsMove.san,
      san: chessJsMove.san,
      uci: `${chessJsMove.from}${chessJsMove.to}${chessJsMove.promotion || ''}`
    };
  }

  /**
   * Get valid moves for a piece at a position (mobile-optimized)
   */
  public getValidMoves(position: ChessPosition): ChessPosition[] {
    try {
      const moves = this.gameEngine.moves({ 
        square: position as any, 
        verbose: true 
      }) as any[];
      
      return moves.map(move => move.to as ChessPosition);
    } catch (error) {
      console.warn('Error getting valid moves:', error);
      return [];
    }
  }

  /**
   * Handle mobile square selection
   */
  public selectSquare(position: ChessPosition): void {
    const piece = this.gameEngine.get(position as any);
    
    if (this.mobileState.selectedSquare === position) {
      // Deselect if same square clicked
      this.mobileState = {
        ...this.mobileState,
        selectedSquare: null,
        validMoves: []
      };
    } else if (piece && piece.color === this.gameEngine.turn()) {
      // Select piece and show valid moves
      const validMoves = this.getValidMoves(position);
      this.mobileState = {
        ...this.mobileState,
        selectedSquare: position,
        validMoves
      };
    } else if (this.mobileState.selectedSquare && 
               this.mobileState.validMoves.includes(position)) {
      // Attempt move to this square
      // This will be handled by the calling code using makeMobileMove
    }
  }

  /**
   * Record mobile interaction for gesture recognition
   */
  public recordInteraction(interaction: MobileChessInteraction): void {
    this.interactionHistory.push(interaction);
    
    // Keep only recent interactions (last 10 for gesture recognition)
    if (this.interactionHistory.length > 10) {
      this.interactionHistory = this.interactionHistory.slice(-10);
    }
  }

  /**
   * Update mobile configuration
   */
  public updateMobileConfig(config: Partial<MobileChessConfig>): void {
    this.mobileConfig = { ...this.mobileConfig, ...config };
  }

  /**
   * Reset game to initial state
   */
  public reset(initialFen?: string): void {
    this.gameEngine.reset();
    if (initialFen) {
      this.gameEngine.load(initialFen);
    }
    this.moveHistory = [];
    this.mobileState = this.createInitialMobileState();
    this.interactionHistory = [];
  }

  /**
   * Get current FEN string
   */
  public getFen(): string {
    return this.gameEngine.fen();
  }

  /**
   * Load game from FEN string
   */
  public loadFen(fen: string): boolean {
    try {
      this.gameEngine.load(fen);
      this.mobileState = this.createInitialMobileState();
      return true;
    } catch (error) {
      console.error('Failed to load FEN:', error);
      return false;
    }
  }

  /**
   * Get game PGN
   */
  public getPgn(): string {
    return this.gameEngine.pgn();
  }

  /**
   * Check if position is valid for mobile interaction
   */
  public isValidSquare(position: string): position is ChessPosition {
    try {
      // Check if it's a valid chess square
      return /^[a-h][1-8]$/.test(position);
    } catch (error) {
      return false;
    }
  }

  /**
   * Get piece at position
   */
  public getPieceAt(position: ChessPosition): ChessPiece | null {
    const piece = this.gameEngine.get(position as any);
    if (!piece) return null;

    return {
      id: `${piece.color}-${piece.type}-${position}`,
      type: piece.type as PieceType,
      color: piece.color === 'w' ? 'white' : 'black',
      position: squareToPosition(position)
    };
  }

  /**
   * Check if it's player's turn (for mobile UI state)
   */
  public isPlayerTurn(playerColor: PieceColor): boolean {
    const currentTurn = this.gameEngine.turn() === 'w' ? 'white' : 'black';
    return currentTurn === playerColor;
  }

  /**
   * Get mobile board state
   */
  public getMobileBoardState(): MobileBoardState {
    return { ...this.mobileState };
  }

  /**
   * Force board flip (for mobile rotation)
   */
  public flipBoard(): void {
    this.mobileState = {
      ...this.mobileState,
      isBoardFlipped: !this.mobileState.isBoardFlipped
    };
  }
}