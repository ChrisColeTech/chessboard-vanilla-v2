import React from 'react'
import { HelpCircle } from 'lucide-react'
interface InstructionsFABProps {
  onClick: () => void
}

export const InstructionsFAB: React.FC<InstructionsFABProps> = ({ onClick }) => {
  
  const handleClick = () => {
    // Note: UI click sound is handled automatically by Global UI Audio System
    onClick()
  }
  
  return (
    <button
      onClick={handleClick}
      className="absolute bottom-4 right-4 sm:right-8 lg:right-20 w-12 h-12 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center group z-30"
      aria-label="Show instructions"
    >
      <HelpCircle className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
    </button>
  )
}