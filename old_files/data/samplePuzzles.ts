// Sample chess puzzles for testing when API is not available
import type { Puzzle } from '../types/puzzle.types';

export const SAMPLE_PUZZLES: Puzzle[] = [
  {
    id: 'sample_1',
    fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2',
    solution_moves: ['Nf3'],
    themes: ['opening', 'development'],
    rating: 1000,
    description: 'Develop the knight to control the center',
    created_at: new Date().toISOString()
  },
  {
    id: 'sample_2', 
    fen: 'r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4',
    solution_moves: ['Qxf7#'],
    themes: ['checkmate', 'back_rank'],
    rating: 1200,
    description: "Scholar's Mate pattern - checkmate in one",
    created_at: new Date().toISOString()
  },
  {
    id: 'sample_3',
    fen: '8/8/8/8/8/3K4/4R3/4k3 w - - 0 1',
    solution_moves: ['Re1+', 'Kf2', 'Re2+', 'Kf3', 'Re3+'],
    themes: ['endgame', 'rook_vs_king'],
    rating: 1300,
    description: 'White to move and deliver checkmate with rook',
    created_at: new Date().toISOString()
  },
  {
    id: 'sample_4',
    fen: '6k1/5ppp/8/8/8/8/5PPP/R3K2r b - - 0 1',
    solution_moves: ['Rxh2', 'Ra8+', 'Kh7'],
    themes: ['tactics', 'fork'],
    rating: 1500,
    description: 'Black to play and win material',
    created_at: new Date().toISOString()
  },
  {
    id: 'sample_5',
    fen: '2rqkb1r/pp2nppp/3p4/2pP4/4P3/2N2N2/PPP2PPP/R1BQKB1R w KQk c6 0 8',
    solution_moves: ['dxc6', 'Nxc6', 'Nb5'],
    themes: ['opening', 'tactics', 'discovered_attack'],
    rating: 1600,
    description: 'White to play and gain advantage in the center',
    created_at: new Date().toISOString()
  }
];

// Utility to get a random sample puzzle
export const getRandomSamplePuzzle = (): Puzzle => {
  const randomIndex = Math.floor(Math.random() * SAMPLE_PUZZLES.length);
  return SAMPLE_PUZZLES[randomIndex];
};