import { create } from "zustand";
import { persist, subscribeWithSelector } from "zustand/middleware";

export type TabId = 'chess' | 'user' | 'learning' | 'progress' | 'support' | 'other';

interface AppState {
  selectedTab: TabId;
  currentChildPage: string | null;
  coinBalance: number;
  setSelectedTab: (tab: TabId) => void;
  setCurrentChildPage: (childPage: string | null) => void;
  setCoinBalance: (balance: number) => void;
}

export const useAppStore = create<AppState>()(
  subscribeWithSelector(
    persist(
      (set) => ({
        selectedTab: 'chess',
        currentChildPage: null,
        coinBalance: 1000,
        setSelectedTab: (tab) => set({ selectedTab: tab }),
        setCurrentChildPage: (childPage) => set({ currentChildPage: childPage }),
        setCoinBalance: (balance) => set({ coinBalance: balance }),
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
