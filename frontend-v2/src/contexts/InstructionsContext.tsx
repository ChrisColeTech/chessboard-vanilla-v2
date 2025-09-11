import React, { createContext, useContext } from 'react';
import type { ReactNode } from 'react';
import { useInstructions } from '../hooks/useInstructions';

interface InstructionsContextType {
  title: string;
  instructions: string[];
  setInstructions: (title: string, instructions: string[]) => void;
}

const InstructionsContext = createContext<InstructionsContextType | undefined>(undefined);

export const useInstructionsContext = () => {
  const context = useContext(InstructionsContext);
  if (!context) {
    throw new Error('useInstructionsContext must be used within an InstructionsProvider');
  }
  return context;
};

interface InstructionsProviderProps {
  children: ReactNode;
}

export const InstructionsProvider: React.FC<InstructionsProviderProps> = ({ children }) => {
  const { title, instructions, setInstructions } = useInstructions();

  return (
    <InstructionsContext.Provider value={{
      title,
      instructions,
      setInstructions
    }}>
      {children}
    </InstructionsContext.Provider>
  );
};
