// useChessBoardAudio.ts - Chess board specific audio hook wrapper

import { useChessAudio } from '../../services/audio/audioService';
import type { MoveAudioContext, ChessBoardAudioConfig } from '../../types/audio/chess-board-audio.types';

/**
 * Chess board specific audio hook
 * Wraps useChessAudio with board-specific enhancements and semantic naming
 */
export const useChessBoardAudio = (config?: Partial<ChessBoardAudioConfig>) => {
  const {
    playMove,
    playError,
    playUIClick,
    playCheck,
    playGameStart,
    playGameEnd,
    setVolume,
    toggleEnabled,
    setEnabled,
    getSettings,
    updateSettings,
    preloadSounds
  } = useChessAudio();

  /**
   * Play audio feedback for piece selection
   * Uses UI click sound for piece selection feedback
   */
  const playPieceSelection = () => {
    if (config?.events?.pieceSelection !== false) {
      playUIClick();
    }
  };

  /**
   * Play audio feedback for piece deselection
   * Uses UI click sound for piece deselection feedback
   */
  const playPieceDeselection = () => {
    if (config?.events?.pieceSelection !== false) {
      playUIClick();
    }
  };

  /**
   * Play audio feedback for piece movement
   * @param wasCapture - Whether the move was a capture
   */
  const playPieceMove = (wasCapture: boolean = false) => {
    if (config?.events?.pieceMovement !== false || config?.events?.capture !== false) {
      playMove(wasCapture);
    }
  };

  /**
   * Play audio feedback for invalid moves or actions
   */
  const playInvalidMove = () => {
    if (config?.events?.invalidMove !== false) {
      playError();
    }
  };

  /**
   * Play audio feedback for check situation
   */
  const playCheckSound = () => {
    if (config?.events?.check !== false) {
      playCheck();
    }
  };

  /**
   * Play audio feedback for game start
   */
  const playGameStartSound = () => {
    if (config?.events?.gameEvents !== false) {
      playGameStart();
    }
  };

  /**
   * Play audio feedback for game end
   */
  const playGameEndSound = () => {
    if (config?.events?.gameEvents !== false) {
      playGameEnd();
    }
  };

  /**
   * Play contextual move audio based on move details
   * @param context - Context information about the move
   */
  const playContextualMove = (context: MoveAudioContext) => {
    // Handle special move types
    switch (context.moveType) {
      case 'capture':
        if (config?.events?.capture !== false) {
          playMove(true);
        }
        break;
      case 'castle':
      case 'enPassant':
      case 'promotion':
        // Special moves use regular move sound for now
        // TODO: Add specific sounds for special moves in Phase 3A
        if (config?.events?.pieceMovement !== false) {
          playMove(context.wasCapture);
        }
        break;
      case 'normal':
      default:
        if (config?.events?.pieceMovement !== false) {
          playMove(context.wasCapture);
        }
        break;
    }

    // Play check sound if the move resulted in check
    if (context.wasCheck && config?.events?.check !== false) {
      // Small delay to let the move sound play first
      setTimeout(() => {
        playCheck();
      }, 150);
    }
  };

  return {
    // Chess board specific methods
    playPieceSelection,
    playPieceDeselection,
    playPieceMove,
    playInvalidMove,
    playCheckSound,
    playGameStartSound,
    playGameEndSound,
    playContextualMove,

    // Pass through original methods for advanced use cases
    playMove,
    playError,
    playUIClick,
    playCheck,
    playGameStart,
    playGameEnd,

    // Configuration methods
    setVolume,
    toggleEnabled,
    setEnabled,
    getSettings,
    updateSettings,
    preloadSounds
  };
};