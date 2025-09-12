import { create } from "zustand";
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
