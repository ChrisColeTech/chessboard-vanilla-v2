import React, { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

interface InstructionsContextType {
  instructions: string[]
  title: string
  setInstructions: (title: string, instructions: string[]) => void
  showInstructions: boolean
  openInstructions: () => void
  closeInstructions: () => void
}

const InstructionsContext = createContext<InstructionsContextType | undefined>(undefined)

export const useInstructions = () => {
  const context = useContext(InstructionsContext)
  if (!context) {
    throw new Error('useInstructions must be used within InstructionsProvider')
  }
  return context
}

interface InstructionsProviderProps {
  children: ReactNode
}

export const InstructionsProvider: React.FC<InstructionsProviderProps> = ({ children }) => {
  const [instructions, setInstructionsState] = useState<string[]>([])
  const [title, setTitle] = useState<string>('')
  const [showInstructions, setShowInstructions] = useState(false)

  const setInstructions = useCallback((newTitle: string, newInstructions: string[]) => {
    setTitle(newTitle)
    setInstructionsState(newInstructions)
  }, [])

  const openInstructions = useCallback(() => setShowInstructions(true), [])
  const closeInstructions = useCallback(() => setShowInstructions(false), [])

  return (
    <InstructionsContext.Provider
      value={{
        instructions,
        title,
        setInstructions,
        showInstructions,
        openInstructions,
        closeInstructions
      }}
    >
      {children}
    </InstructionsContext.Provider>
  )
}