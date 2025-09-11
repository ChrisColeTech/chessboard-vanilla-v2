import React from 'react'
import type { ActionButtonsProps } from '../../../types/casino/blackjack.types'

export const ActionButtons: React.FC<ActionButtonsProps> = ({
  canHit,
  canStand,
  canDouble,
  onHit,
  onStand,
  onDouble,
  currentBet,
  balance,
  disabled = false
}) => {
  const buttonBaseClass = `
    flex flex-col items-center justify-center space-y-1
    min-w-20 min-h-16 px-4 py-2
    rounded-xl font-bold text-sm
    transform transition-all duration-200
    border-2
    disabled:opacity-50 disabled:cursor-not-allowed
    active:scale-95
  `

  const enabledButtonClass = `
    ${buttonBaseClass}
    hover:scale-105 hover:shadow-lg
    active:animate-pulse
  `

  return (
    <div className="flex justify-center space-x-4 mt-6">
      {/* Hit Button */}
      <button
        className={`
          ${enabledButtonClass}
          ${canHit && !disabled
            ? 'bg-blue-600 hover:bg-blue-700 text-white border-blue-700'
            : 'bg-gray-400 text-gray-700 border-gray-500'
          }
        `}
        disabled={!canHit || disabled}
        onClick={onHit}
      >
        <span className="text-lg">👆</span>
        <span>HIT</span>
      </button>

      {/* Stand Button */}
      <button
        className={`
          ${enabledButtonClass}
          ${canStand && !disabled
            ? 'bg-red-600 hover:bg-red-700 text-white border-red-700'
            : 'bg-gray-400 text-gray-700 border-gray-500'
          }
        `}
        disabled={!canStand || disabled}
        onClick={onStand}
      >
        <span className="text-lg">✋</span>
        <span>STAND</span>
      </button>

      {/* Double Button */}
      {canDouble && (
        <button
          className={`
            ${enabledButtonClass}
            ${balance >= currentBet && !disabled
              ? 'bg-yellow-600 hover:bg-yellow-700 text-white border-yellow-700'
              : 'bg-gray-400 text-gray-700 border-gray-500'
            }
          `}
          disabled={balance < currentBet || disabled}
          onClick={onDouble}
        >
          <span className="text-lg">💰</span>
          <span>DOUBLE</span>
          <span className="text-xs opacity-80">({currentBet} coins)</span>
        </button>
      )}
    </div>
  )
}