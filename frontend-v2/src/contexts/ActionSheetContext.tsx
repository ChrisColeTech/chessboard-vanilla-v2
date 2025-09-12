import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface ActionSheetContextType {
  isOpen: boolean;
  currentPage: string | null;
  openActionSheet: (page: string) => void;
  closeActionSheet: () => void;
}

const ActionSheetContext = createContext<ActionSheetContextType | undefined>(undefined);

export const useActionSheet = () => {
  const context = useContext(ActionSheetContext);
  if (!context) {
    throw new Error('useActionSheet must be used within an ActionSheetProvider');
  }
  return context;
};

interface ActionSheetProviderProps {
  children: ReactNode;
}

export const ActionSheetProvider: React.FC<ActionSheetProviderProps> = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState<string | null>(null);

  const openActionSheet = (page: string) => {
    setCurrentPage(page);
    setIsOpen(true);
  };

  const closeActionSheet = () => {
    setIsOpen(false);
    setCurrentPage(null);
  };

  return (
    <ActionSheetContext.Provider value={{
      isOpen,
      currentPage,
      openActionSheet,
      closeActionSheet
    }}>
      {children}
    </ActionSheetContext.Provider>
  );
};