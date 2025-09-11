import React from 'react'
import type { BetControlsProps } from '../../../types/casino/blackjack.types'

export const BetControls: React.FC<BetControlsProps> = ({
  currentBet,
  balance,
  minBet,
  maxBet,
  onBetChange,
  disabled = false
}) => {
  const handleBetChange = (newBet: number) => {
    const clampedBet = Math.max(minBet, Math.min(maxBet, Math.min(balance, newBet)))
    onBetChange(clampedBet)
  }

  const predefinedBets = [5, 10, 25, 50]
  const availableBets = predefinedBets.filter(bet => bet <= balance && bet >= minBet && bet <= maxBet)

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Current Bet Display */}
      <div className="text-center">
        <div className="text-lg font-semibold text-muted-foreground">Your Bet</div>
        <div className="text-3xl font-bold">{currentBet} coins</div>
      </div>

      {/* Quick Bet Buttons */}
      <div className="flex flex-wrap justify-center gap-2">
        {availableBets.map(bet => (
          <button
            key={bet}
            className={`
              px-4 py-2 rounded-lg font-semibold text-sm
              transform transition-all duration-200
              ${currentBet === bet
                ? 'bg-blue-600 text-white scale-105 shadow-lg'
                : 'bg-gray-600 text-gray-200 hover:bg-gray-500 hover:scale-105'
              }
              disabled:opacity-50 disabled:cursor-not-allowed
              active:scale-95
            `}
            disabled={disabled || bet > balance}
            onClick={() => handleBetChange(bet)}
          >
            {bet}
          </button>
        ))}
      </div>

      {/* Custom Bet Input */}
      <div className="flex items-center space-x-2">
        <button
          className="w-8 h-8 rounded-full bg-red-600 text-white font-bold text-sm hover:bg-red-700 disabled:opacity-50"
          disabled={disabled || currentBet <= minBet}
          onClick={() => handleBetChange(currentBet - 5)}
        >
          -
        </button>
        
        <input
          type="number"
          min={minBet}
          max={Math.min(maxBet, balance)}
          value={currentBet}
          onChange={(e) => handleBetChange(parseInt(e.target.value) || minBet)}
          disabled={disabled}
          className="
            w-20 h-8 text-center rounded border border-gray-400
            bg-gray-800 text-white font-semibold
            focus:outline-none focus:border-blue-500
            disabled:opacity-50
          "
        />
        
        <button
          className="w-8 h-8 rounded-full bg-green-600 text-white font-bold text-sm hover:bg-green-700 disabled:opacity-50"
          disabled={disabled || currentBet >= Math.min(maxBet, balance)}
          onClick={() => handleBetChange(currentBet + 5)}
        >
          +
        </button>
      </div>

      {/* Balance Display */}
      <div className="text-sm text-muted-foreground text-center">
        Balance: <span className="font-semibold">{balance} coins</span>
        {balance < minBet && (
          <div className="text-red-500 text-xs mt-1">
            Insufficient balance for minimum bet
          </div>
        )}
      </div>
    </div>
  )
}