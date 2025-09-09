import React from 'react'
import { Target, X } from 'lucide-react'

interface InstructionsModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  instructions: string[]
}

export const InstructionsModal: React.FC<InstructionsModalProps> = ({
  isOpen,
  onClose,
  title = "How to Use",
  instructions
}) => {
  if (!isOpen) return null

  return (
    <div className="modal-backdrop modal-backdrop-padding">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 modal-backdrop-dark"
        onClick={onClose}
      />
      
      {/* Modal Content */}
      <div className="modal-content modal-content-md">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="modal-icon-container">
              <Target className="w-5 h-5 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-muted rounded-lg transition-colors"
            aria-label="Close instructions"
          >
            <X className="w-5 h-5 text-muted-foreground" />
          </button>
        </div>
        
        <div className="space-y-3 text-sm text-muted-foreground">
          {instructions.map((instruction, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
              <p>{instruction}</p>
            </div>
          ))}
        </div>
        
        <button
          onClick={onClose}
          className="mt-6 w-full px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          Got it!
        </button>
      </div>
    </div>
  )
}