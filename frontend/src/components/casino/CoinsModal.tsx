import React from 'react'
import { Coins, X, Plus, Minus } from 'lucide-react'

interface CoinsModalProps {
  isOpen: boolean
  onClose: () => void
  coinBalance?: number
}

export const CoinsModal: React.FC<CoinsModalProps> = ({
  isOpen,
  onClose,
  coinBalance = 0
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
              <Coins className="w-5 h-5 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">Coin Balance</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-muted rounded-lg transition-colors"
            aria-label="Close coins modal"
          >
            <X className="w-5 h-5 text-muted-foreground" />
          </button>
        </div>
        
        {/* Current Balance Display */}
        <div className="text-center mb-6">
          <div className="text-3xl font-bold text-foreground mb-2">
            {coinBalance.toLocaleString()}
          </div>
          <div className="text-sm text-muted-foreground">
            Total Coins Available
          </div>
        </div>

        {/* Coin Actions */}
        <div className="space-y-3 mb-6">
          <div className="flex items-center justify-between p-3 border border-border rounded-lg">
            <div className="flex items-center gap-3">
              <Plus className="w-4 h-4 text-green-500" />
              <span className="text-sm text-foreground">Earned from games</span>
            </div>
            <span className="text-sm text-muted-foreground">+{Math.floor(coinBalance * 0.1)} today</span>
          </div>
          
          <div className="flex items-center justify-between p-3 border border-border rounded-lg">
            <div className="flex items-center gap-3">
              <Minus className="w-4 h-4 text-red-500" />
              <span className="text-sm text-foreground">Spent on features</span>
            </div>
            <span className="text-sm text-muted-foreground">-{Math.floor(coinBalance * 0.05)} today</span>
          </div>
        </div>

        {/* Info Text */}
        <div className="text-xs text-muted-foreground text-center mb-4">
          Earn coins by playing games and completing challenges. Use coins to unlock premium features and content.
        </div>
        
        <button
          onClick={onClose}
          className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          Close
        </button>
      </div>
    </div>
  )
}