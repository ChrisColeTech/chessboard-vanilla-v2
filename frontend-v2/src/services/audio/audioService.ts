import { useCallback } from 'react';

export const useChessAudio = () => {
  const preloadSounds = useCallback(() => {
    console.log('Chess Audio: Preloading sounds');
  }, []);

  const playGameStart = useCallback(() => {
    console.log('Chess Audio: Game start sound');
  }, []);

  const playMove = useCallback((isCapture: boolean = false) => {
    console.log(`Chess Audio: ${isCapture ? 'Capture' : 'Move'} sound`);
  }, []);

  const playCheck = useCallback(() => {
    console.log('Chess Audio: Check sound');
  }, []);

  const playCheckmate = useCallback(() => {
    console.log('Chess Audio: Checkmate sound');
  }, []);

  return {
    preloadSounds,
    playGameStart,
    playMove,
    playCheck,
    playCheckmate
  };
};
