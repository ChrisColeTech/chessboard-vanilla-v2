import type { ChessPiece, ChessPosition, ChessPositionObject, File, Rank } from '../../types';

export type PieceColor = 'white' | 'black';
export type GameStatus = 'playing' | 'check' | 'checkmate';

export interface GameState {
  pieces: Record<string, ChessPiece>;
  currentTurn: PieceColor;
  gameStatus: GameStatus;
  kingInCheck: PieceColor | null;
}

export interface MoveResult {
  success: boolean;
  capturedPiece?: ChessPiece;
  newGameState?: GameState;
  error?: string;
  needsPromotion?: boolean;
  promotionSquare?: ChessPosition;
}

export class TestBoardGameService {
  private gameState: GameState;

  constructor(initialPieces: Record<string, ChessPiece>) {
    this.gameState = {
      pieces: { ...initialPieces },
      currentTurn: 'white', // Doesn't matter for free play, but needed for interface
      gameStatus: 'playing',
      kingInCheck: null
    };
  }

  getGameState(): GameState {
    return { ...this.gameState };
  }

  // Get all valid moves for a piece at a position (FREE PLAY - no turn restrictions)
  getValidMoves(position: ChessPosition): ChessPosition[] {
    console.log(`🔍 [GAME SERVICE] getValidMoves called for position: ${position}`);
    const piece = this.gameState.pieces[position];
    if (!piece) {
      console.log(`🔍 [GAME SERVICE] No piece found at ${position}`);
      return [];
    }

    console.log(`🔍 [GAME SERVICE] Found piece: ${piece.color} ${piece.type} at ${position}`);
    const moves = this.getPieceBaseMoves(piece, position);
    
    console.log(`🔍 [GAME SERVICE] ${piece.color} ${piece.type} at ${position} base moves:`, moves);
    
    // Filter out moves that would put own king in check
    const validMoves = moves.filter(movePos => !this.wouldMoveLeaveKingInCheck(position, movePos));
    
    console.log(`🔍 [GAME SERVICE] Valid moves after check filtering:`, validMoves);
    
    return validMoves;
  }

  // Attempt to make a move (FREE PLAY - no turn restrictions)
  makeMove(from: ChessPosition, to: ChessPosition, promotionPiece?: 'queen' | 'rook' | 'bishop' | 'knight'): MoveResult {
    console.log(`🎯 [GAME SERVICE] makeMove called: ${from} → ${to}${promotionPiece ? ` (promote to ${promotionPiece})` : ''}`);
    
    const piece = this.gameState.pieces[from];
    console.log(`🎯 [GAME SERVICE] Piece at ${from}:`, piece);
    
    // Basic validation
    if (!piece) {
      console.log(`❌ [GAME SERVICE] No piece found at ${from}`);
      return { success: false, error: 'No piece at source position' };
    }

    console.log(`🎯 [GAME SERVICE] Current game state pieces:`, Object.keys(this.gameState.pieces));

    const validMoves = this.getValidMoves(from);
    if (!validMoves.includes(to)) {
      return { success: false, error: 'Invalid move' };
    }

    // Check for pawn promotion
    const isPromotion = piece.type === 'pawn' && 
      ((piece.color === 'white' && to[1] === '3') || // White pawn reaches rank 3
       (piece.color === 'black' && to[1] === '1'));   // Black pawn reaches rank 1

    if (isPromotion && !promotionPiece) {
      // Need promotion piece selection
      return {
        success: false,
        needsPromotion: true,
        promotionSquare: to,
        error: 'Pawn promotion requires piece selection'
      };
    }

    // Execute the move
    const capturedPiece = this.gameState.pieces[to];
    const newPieces = { ...this.gameState.pieces };
    
    // Move the piece
    delete newPieces[from];
    
    if (isPromotion && promotionPiece) {
      // Promote pawn to selected piece
      const promotedPiece: ChessPiece = {
        id: `promoted-${promotionPiece}-${to}`,
        type: promotionPiece,
        color: piece.color,
        position: this.parsePosition(to)
      };
      newPieces[to] = promotedPiece;
      console.log(`🎉 [GAME SERVICE] Pawn promoted to ${promotionPiece} at ${to}:`, promotedPiece);
    } else {
      // Normal move
      newPieces[to] = {
        ...piece,
        position: this.parsePosition(to)
      };
    }

    // Update game state (FREE PLAY - don't change turns)
    const newState: GameState = {
      pieces: newPieces,
      currentTurn: this.gameState.currentTurn, // Keep same turn for free play
      gameStatus: 'playing',
      kingInCheck: null
    };

    // Check for check/checkmate for both kings (FREE PLAY)
    const whiteKingPos = this.findKing('white', newPieces);
    const blackKingPos = this.findKing('black', newPieces);
    
    // Check if white king is in check
    if (whiteKingPos && this.isPositionUnderAttack(whiteKingPos, 'black', newPieces)) {
      newState.kingInCheck = 'white';
      if (this.isCheckmate('white', newPieces)) {
        newState.gameStatus = 'checkmate';
      } else {
        newState.gameStatus = 'check';
      }
    }
    // Check if black king is in check
    else if (blackKingPos && this.isPositionUnderAttack(blackKingPos, 'white', newPieces)) {
      newState.kingInCheck = 'black';
      if (this.isCheckmate('black', newPieces)) {
        newState.gameStatus = 'checkmate';
      } else {
        newState.gameStatus = 'check';
      }
    }

    this.gameState = newState;

    return {
      success: true,
      capturedPiece,
      newGameState: newState
    };
  }

  // Reset the game
  reset(initialPieces: Record<string, ChessPiece>): void {
    this.gameState = {
      pieces: { ...initialPieces },
      currentTurn: 'white',
      gameStatus: 'playing',
      kingInCheck: null
    };
  }

  // Helper: Get base moves for a piece (before check validation)
  private getPieceBaseMoves(piece: ChessPiece, position: ChessPosition): ChessPosition[] {
    const moves: ChessPosition[] = [];
    const { file, rank } = this.parsePosition(position);

    switch (piece.type) {
      case 'king':
        // King moves 1 square in any direction
        for (let df = -1; df <= 1; df++) {
          for (let dr = -1; dr <= 1; dr++) {
            if (df === 0 && dr === 0) continue; // Skip current position
            
            const newFile = String.fromCharCode(file.charCodeAt(0) + df);
            const newRank = rank + dr;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (this.isValidSquare(newPos) && this.canMoveTo(piece.color, newPos)) {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'pawn':
        const direction = piece.color === 'white' ? 1 : -1; // White moves up, black moves down
        
        // Forward move
        const forwardPos = `${file}${rank + direction}` as ChessPosition;
        if (this.isValidSquare(forwardPos) && !this.gameState.pieces[forwardPos]) {
          moves.push(forwardPos);
        }
        
        // Diagonal captures
        for (const df of [-1, 1]) {
          const newFile = String.fromCharCode(file.charCodeAt(0) + df);
          const capturePos = `${newFile}${rank + direction}` as ChessPosition;
          
          if (this.isValidSquare(capturePos)) {
            const targetPiece = this.gameState.pieces[capturePos];
            if (targetPiece && targetPiece.color !== piece.color) {
              moves.push(capturePos);
            }
          }
        }
        break;

      case 'queen':
        // Queen moves in all directions
        const directions = [
          [-1, -1], [-1, 0], [-1, 1],
          [0, -1],           [0, 1],
          [1, -1],  [1, 0],  [1, 1]
        ];
        
        for (const [df, dr] of directions) {
          for (let distance = 1; distance <= 3; distance++) { // Max distance on 3x3 board
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break; // Out of bounds
            
            const targetPiece = this.gameState.pieces[newPos];
            if (targetPiece) {
              if (targetPiece.color !== piece.color) {
                moves.push(newPos); // Can capture
              }
              break; // Can't move past any piece
            } else {
              moves.push(newPos); // Empty square
            }
          }
        }
        break;

      case 'rook':
        // Rook moves horizontally and vertically
        const rookDirections = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        
        for (const [df, dr] of rookDirections) {
          for (let distance = 1; distance <= 3; distance++) {
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break;
            
            const targetPiece = this.gameState.pieces[newPos];
            if (targetPiece) {
              if (targetPiece.color !== piece.color) {
                moves.push(newPos);
              }
              break;
            } else {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'bishop':
        // Bishop moves diagonally
        const bishopDirections = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
        
        for (const [df, dr] of bishopDirections) {
          for (let distance = 1; distance <= 3; distance++) {
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break;
            
            const targetPiece = this.gameState.pieces[newPos];
            if (targetPiece) {
              if (targetPiece.color !== piece.color) {
                moves.push(newPos);
              }
              break;
            } else {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'knight':
        // Knight moves in L-shapes
        const knightMoves = [
          [-2, -1], [-2, 1], [-1, -2], [-1, 2],
          [1, -2], [1, 2], [2, -1], [2, 1]
        ];
        
        for (const [df, dr] of knightMoves) {
          const newFile = String.fromCharCode(file.charCodeAt(0) + df);
          const newRank = rank + dr;
          const newPos = `${newFile}${newRank}` as ChessPosition;
          
          if (this.isValidSquare(newPos) && this.canMoveTo(piece.color, newPos)) {
            moves.push(newPos);
          }
        }
        break;
    }

    return moves;
  }

  // Helper: Check if a move would leave own king in check
  private wouldMoveLeaveKingInCheck(from: ChessPosition, to: ChessPosition): boolean {
    const piece = this.gameState.pieces[from];
    if (!piece) return true;

    // Simulate the move
    const simulatedPieces = { ...this.gameState.pieces };
    delete simulatedPieces[from];
    simulatedPieces[to] = piece;

    // Find our king position after the move
    const kingPos = piece.type === 'king' ? to : this.findKing(piece.color, simulatedPieces);
    if (!kingPos) {
      // No king found - in free play mode, allow move (no king to protect)
      return false;
    }

    // Check if king would be under attack
    const enemyColor: PieceColor = piece.color === 'white' ? 'black' : 'white';
    return this.isPositionUnderAttack(kingPos, enemyColor, simulatedPieces);
  }

  // Helper: Check if a position is under attack by a specific color
  private isPositionUnderAttack(position: ChessPosition, attackingColor: PieceColor, pieces: Record<string, ChessPiece>): boolean {
    for (const [pos, piece] of Object.entries(pieces)) {
      if (piece.color === attackingColor) {
        const attackMoves = this.getPieceAttackMoves(piece, pos as ChessPosition, pieces);
        if (attackMoves.includes(position)) {
          return true;
        }
      }
    }
    return false;
  }

  // Helper: Get squares a piece can attack (similar to moves but without check validation)
  private getPieceAttackMoves(piece: ChessPiece, position: ChessPosition, pieces: Record<string, ChessPiece>): ChessPosition[] {
    const moves: ChessPosition[] = [];
    const { file, rank } = this.parsePosition(position);

    switch (piece.type) {
      case 'king':
        for (let df = -1; df <= 1; df++) {
          for (let dr = -1; dr <= 1; dr++) {
            if (df === 0 && dr === 0) continue;
            
            const newFile = String.fromCharCode(file.charCodeAt(0) + df);
            const newRank = rank + dr;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (this.isValidSquare(newPos)) {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'pawn':
        const direction = piece.color === 'white' ? 1 : -1;
        // Pawns only attack diagonally
        for (const df of [-1, 1]) {
          const newFile = String.fromCharCode(file.charCodeAt(0) + df);
          const attackPos = `${newFile}${rank + direction}` as ChessPosition;
          
          if (this.isValidSquare(attackPos)) {
            moves.push(attackPos);
          }
        }
        break;

      case 'queen':
        const directions = [
          [-1, -1], [-1, 0], [-1, 1],
          [0, -1],           [0, 1],
          [1, -1],  [1, 0],  [1, 1]
        ];
        
        for (const [df, dr] of directions) {
          for (let distance = 1; distance <= 3; distance++) {
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break;
            
            moves.push(newPos);
            
            if (pieces[newPos]) break; // Stop at first piece encountered
          }
        }
        break;

      case 'rook':
        const rookDirections = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        
        for (const [df, dr] of rookDirections) {
          for (let distance = 1; distance <= 3; distance++) {
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break;
            
            moves.push(newPos);
            
            if (pieces[newPos]) break;
          }
        }
        break;

      case 'bishop':
        const bishopDirections = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
        
        for (const [df, dr] of bishopDirections) {
          for (let distance = 1; distance <= 3; distance++) {
            const newFile = String.fromCharCode(file.charCodeAt(0) + df * distance);
            const newRank = rank + dr * distance;
            const newPos = `${newFile}${newRank}` as ChessPosition;
            
            if (!this.isValidSquare(newPos)) break;
            
            moves.push(newPos);
            
            if (pieces[newPos]) break;
          }
        }
        break;

      case 'knight':
        const knightMoves = [
          [-2, -1], [-2, 1], [-1, -2], [-1, 2],
          [1, -2], [1, 2], [2, -1], [2, 1]
        ];
        
        for (const [df, dr] of knightMoves) {
          const newFile = String.fromCharCode(file.charCodeAt(0) + df);
          const newRank = rank + dr;
          const newPos = `${newFile}${newRank}` as ChessPosition;
          
          if (this.isValidSquare(newPos)) {
            moves.push(newPos);
          }
        }
        break;
    }

    return moves;
  }

  // Helper: Check for checkmate
  private isCheckmate(color: PieceColor, pieces: Record<string, ChessPiece>): boolean {
    // Find all pieces of the given color
    for (const [pos, piece] of Object.entries(pieces)) {
      if (piece.color === color) {
        // Get all possible moves for this piece
        const baseMoves = this.getPieceBaseMoves(piece, pos as ChessPosition);
        
        // Check if any move would get the king out of check
        for (const movePos of baseMoves) {
          if (!this.wouldMoveLeaveKingInCheckSimulated(pos as ChessPosition, movePos, pieces)) {
            return false; // Found a valid move, not checkmate
          }
        }
      }
    }
    
    return true; // No valid moves found, it's checkmate
  }

  // Helper for checkmate detection: simulate move without changing game state
  private wouldMoveLeaveKingInCheckSimulated(from: ChessPosition, to: ChessPosition, pieces: Record<string, ChessPiece>): boolean {
    const piece = pieces[from];
    if (!piece) return true;

    // Simulate the move
    const simulatedPieces = { ...pieces };
    delete simulatedPieces[from];
    simulatedPieces[to] = piece;

    // Find king position after move
    const kingPos = piece.type === 'king' ? to : this.findKing(piece.color, simulatedPieces);
    if (!kingPos) return true;

    // Check if king would still be under attack
    const enemyColor: PieceColor = piece.color === 'white' ? 'black' : 'white';
    return this.isPositionUnderAttack(kingPos, enemyColor, simulatedPieces);
  }

  // Helper: Find king of given color
  private findKing(color: PieceColor, pieces: Record<string, ChessPiece>): ChessPosition | null {
    for (const [pos, piece] of Object.entries(pieces)) {
      if (piece.type === 'king' && piece.color === color) {
        return pos as ChessPosition;
      }
    }
    return null;
  }

  // Helper: Check if position is valid on 3x3 board
  private isValidSquare(position: ChessPosition): boolean {
    const file = position[0];
    const rank = parseInt(position[1]);
    return file >= 'a' && file <= 'c' && rank >= 1 && rank <= 3;
  }

  // Helper: Check if piece can move to position (not occupied by same color)
  private canMoveTo(pieceColor: PieceColor, position: ChessPosition): boolean {
    const targetPiece = this.gameState.pieces[position];
    const canMove = !targetPiece || targetPiece.color !== pieceColor;
    console.log(`🔍 [GAME SERVICE] canMoveTo ${position}: target=${targetPiece?.color || 'empty'}, pieceColor=${pieceColor}, result=${canMove}`);
    return canMove;
  }

  // Helper: Parse position string to file/rank
  private parsePosition(position: ChessPosition): ChessPositionObject {
    return {
      file: position[0] as File,
      rank: parseInt(position[1]) as Rank
    };
  }
}