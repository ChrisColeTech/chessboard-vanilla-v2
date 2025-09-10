#!/usr/bin/env python3
"""
Stores Generator Module
Handles generation of Zustand stores for state management
"""

from base_generator import BaseFrontendGenerator

class StoresGenerator(BaseFrontendGenerator):
    """Generates Zustand stores for state management"""
    
    def generate_domain_stores(self):
        """Generate Zustand stores for each domain"""
        src_path = self.get_src_path()
        stores_path = src_path / "stores"
        
        # Generate auth store
        auth_store_content = self._generate_auth_store()
        auth_store_file = stores_path / "authStore.ts"
        self.write_file(auth_store_file, auth_store_content)
        
        # Note: Chess store disabled since we now have separate domains for games, puzzles, etc.
        # chess_store_content = self._generate_chess_store()
        # chess_store_file = stores_path / "chessStore.ts"
        # self.write_file(chess_store_file, chess_store_content)
        
        # Generate main stores index
        stores_index_content = self._generate_stores_index()
        stores_index_file = stores_path / "index.ts"
        self.write_file(stores_index_file, stores_index_content)
    
    def _generate_auth_store(self) -> str:
        """Generate auth store with Zustand"""
        return """import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AuthState, LoginCredentials, UserInfo } from '../types/auth';
import { AuthAPIClient } from '../clients/AuthAPIClient';

interface AuthStore extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  updateUser: (user: Partial<UserInfo>) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      status: 'idle',
      user: null,
      token: null,
      error: null,
      
      login: async (credentials) => {
        set({ status: 'loading', error: null });
        
        try {
          const authClient = new AuthAPIClient();
          const response = await authClient.login(credentials);
          const { user, token } = response.data;
          
          localStorage.setItem('auth_token', token);
          set({ 
            status: 'authenticated', 
            user, 
            token, 
            error: null 
          });
        } catch (error: any) {
          set({ 
            status: 'error', 
            error: error.message 
          });
          throw error;
        }
      },
      
      logout: () => {
        localStorage.removeItem('auth_token');
        set({ 
          status: 'unauthenticated', 
          user: null, 
          token: null, 
          error: null 
        });
      },
      
      refreshToken: async () => {
        try {
          const token = get().token;
          if (!token) return false;
          
          const authClient = new AuthAPIClient();
          const response = await authClient.verifyToken({ token });
          const { user } = response.data;
          
          set({ user });
          return true;
        } catch {
          get().logout();
          return false;
        }
      },
      
      updateUser: (userData) => {
        const currentUser = get().user;
        if (currentUser) {
          set({ user: { ...currentUser, ...userData } });
        }
      },
      
      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        status: state.status 
      }),
    }
  )
);
"""
    
    def _generate_chess_store(self) -> str:
        """Generate chess store with Zustand"""
        return """import { create } from 'zustand';
import type { GameStatus, PuzzleFilters } from '../types/chess';

interface ChessStore {
  currentGameId: string | null;
  gameStatus: GameStatus;
  puzzleFilters: PuzzleFilters;
  selectedPuzzleId: string | null;
  
  setCurrentGame: (gameId: string | null) => void;
  setGameStatus: (status: GameStatus) => void;
  updatePuzzleFilters: (filters: Partial<PuzzleFilters>) => void;
  selectPuzzle: (puzzleId: string | null) => void;
}

export const useChessStore = create<ChessStore>((set) => ({
  currentGameId: null,
  gameStatus: 'idle',
  puzzleFilters: {
    minRating: 800,
    maxRating: 2000,
    limit: 10,
    offset: 0
  },
  selectedPuzzleId: null,
  
  setCurrentGame: (gameId) => set({ currentGameId: gameId }),
  
  setGameStatus: (status) => set({ gameStatus: status }),
  
  updatePuzzleFilters: (filters) => 
    set((state) => ({ 
      puzzleFilters: { ...state.puzzleFilters, ...filters } 
    })),
    
  selectPuzzle: (puzzleId) => set({ selectedPuzzleId: puzzleId }),
}));
"""
    
    def _generate_stores_index(self) -> str:
        """Generate main stores index"""
        return """export { useAuthStore } from './authStore';
// Note: Chess store disabled since we now have separate domains
"""