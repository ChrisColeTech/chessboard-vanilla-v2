// index.ts - Services exports barrel

// Core chess services
export { ChessGameService } from './chess/ChessGameService';
export { FenService } from './chess/FenService';
export { TestBoardGameService } from './chess/TestBoardGameService';

// Stockfish services
export { StockfishService } from './chess/StockfishService';
export * from './chess/stockfish-singleton';

// Audio services
export * from './audio/audioService';
export * from './audio/globalUIAudioService';
export * from './audio/globalUIAudio-singleton';

// Chess subdomain services
export * from './chess';

// Client services
export * from './clients';

// Phase 4: UI Tests services
export { UIDemoService } from './ui';

// Authentication services
export { AuthService, authService } from './auth.service';
export type { AuthService as AuthServiceClass } from './auth.service';