import React, { createContext, useContext, useState, type ReactNode } from 'react';

interface InstructionsContextType {
  title: string;
  instructions: string[];
  isOpen: boolean;
  setInstructions: (title: string, instructions: string[]) => void;
  clearInstructions: () => void;
  showInstructions: (title: string, instructions: string[]) => void;
  openInstructions: () => void;
  closeInstructions: () => void;
}

const InstructionsContext = createContext<InstructionsContextType | undefined>(undefined);

export const useInstructions = () => {
  const context = useContext(InstructionsContext);
  if (!context) {
    throw new Error('useInstructions must be used within an InstructionsProvider');
  }
  return context;
};

interface InstructionsProviderProps {
  children: ReactNode;
}

export const InstructionsProvider: React.FC<InstructionsProviderProps> = ({ children }) => {
  const [title, setTitle] = useState<string>('');
  const [instructions, setInstructionsState] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const setInstructions = (newTitle: string, newInstructions: string[]) => {
    setTitle(newTitle);
    setInstructionsState(newInstructions);
  };

  const clearInstructions = () => {
    setTitle('');
    setInstructionsState([]);
    setIsOpen(false);
  };

  const showInstructions = (newTitle: string, newInstructions: string[]) => {
    setTitle(newTitle);
    setInstructionsState(newInstructions);
    setIsOpen(true);
  };

  const openInstructions = () => {
    setIsOpen(true);
  };

  const closeInstructions = () => {
    setIsOpen(false);
  };

  return (
    <InstructionsContext.Provider value={{
      title,
      instructions,
      isOpen,
      setInstructions,
      clearInstructions,
      showInstructions,
      openInstructions,
      closeInstructions
    }}>
      {children}
    </InstructionsContext.Provider>
  );
};