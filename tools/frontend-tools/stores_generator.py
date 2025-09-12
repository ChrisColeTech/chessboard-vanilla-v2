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
        
        # Generate app store
        app_store_content = self._generate_app_store()
        app_store_file = stores_path / "appStore.ts"
        self.write_file(app_store_file, app_store_content)
        
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
    
    def _generate_app_store(self) -> str:
        """Generate app store with Zustand"""
        return """import { create } from "zustand";
import { persist, subscribeWithSelector } from "zustand/middleware";

export type TabId = 'chess' | 'user' | 'learning' | 'progress' | 'support' | 'other';

interface AppState {
  selectedTab: TabId;
  currentChildPage: string | null;
  coinBalance: number;
  isSettingsOpen: boolean;
  isCoinsModalOpen: boolean;
  setSelectedTab: (tab: TabId) => void;
  setCurrentChildPage: (childPage: string | null) => void;
  setCoinBalance: (balance: number) => void;
  toggleSettings: () => void;
  closeSettings: () => void;
  openSettings: () => void;
  toggleCoinsModal: () => void;
  closeCoinsModal: () => void;
  openCoinsModal: () => void;
}

export const useAppStore = create<AppState>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        selectedTab: 'chess',
        currentChildPage: null,
        coinBalance: 1000,
        isSettingsOpen: false,
        isCoinsModalOpen: false,
        setSelectedTab: (tab) => set({ selectedTab: tab }),
        setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
        setCoinBalance: (balance) => set({ coinBalance: balance }),
        toggleSettings: () => set((state) => ({ isSettingsOpen: !state.isSettingsOpen })),
        closeSettings: () => set({ isSettingsOpen: false }),
        openSettings: () => set({ isSettingsOpen: true }),
        toggleCoinsModal: () => set((state) => ({ isCoinsModalOpen: !state.isCoinsModalOpen })),
        closeCoinsModal: () => set({ isCoinsModalOpen: false }),
        openCoinsModal: () => set({ isCoinsModalOpen: true }),
      }),
      {
        name: 'chess-app-store',
        partialize: (state) => ({
          selectedTab: state.selectedTab,
          currentChildPage: state.currentChildPage,
          coinBalance: state.coinBalance,
        }),
      }
    )
  )
);

export const useSelectedTab = () => useAppStore((state) => state.selectedTab);

// Settings hook
export const useSettings = () => {
  const isSettingsOpen = useAppStore((state) => state.isSettingsOpen);
  const toggleSettings = useAppStore((state) => state.toggleSettings);
  const closeSettings = useAppStore((state) => state.closeSettings);
  const openSettings = useAppStore((state) => state.openSettings);
  
  return {
    isOpen: isSettingsOpen,
    toggle: toggleSettings,
    close: closeSettings,
    open: openSettings,
    // Legacy aliases
    isSettingsOpen,
    toggleSettings,
    closeSettings,
    openSettings,
  };
};

// Coins modal hook
export const useCoinsModal = () => {
  const isCoinsModalOpen = useAppStore((state) => state.isCoinsModalOpen);
  const toggleCoinsModal = useAppStore((state) => state.toggleCoinsModal);
  const closeCoinsModal = useAppStore((state) => state.closeCoinsModal);
  const openCoinsModal = useAppStore((state) => state.openCoinsModal);
  const coinBalance = useAppStore((state) => state.coinBalance);
  const setCoinBalance = useAppStore((state) => state.setCoinBalance);
  
  return {
    isOpen: isCoinsModalOpen,
    toggle: toggleCoinsModal,
    close: closeCoinsModal,
    open: openCoinsModal,
    coinBalance,
    setCoinBalance,
    // Legacy aliases
    isCoinsModalOpen,
    toggleCoinsModal,
    closeCoinsModal,
    openCoinsModal,
  };
};
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
export { useAppStore, useSelectedTab, useSettings, useCoinsModal } from './appStore';
// Note: Chess store disabled since we now have separate domains
"""