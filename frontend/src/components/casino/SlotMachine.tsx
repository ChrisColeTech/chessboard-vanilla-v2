import React, { useState } from 'react'
import { Play, Plus, Minus, Coins } from 'lucide-react'
import { useUIClickSound } from '../../hooks/audio/useUIClickSound'

interface SlotMachineProps {
  coinBalance: number
  setCoinBalance: (balance: number) => void
}

export const SlotMachine: React.FC<SlotMachineProps> = ({ coinBalance: _coinBalance, setCoinBalance: _setCoinBalance }) => {
  const [wager, setWager] = useState(10)
  const [isSpinning, setIsSpinning] = useState(false)
  const { playUIClick } = useUIClickSound()
  
  // Current displayed symbols (3 reels) - starting with a mix of pieces
  const [reels, _setReels] = useState(['♔', '♛', '♖'])

  const handleWagerChange = (delta: number) => {
    playUIClick(`Wager ${delta > 0 ? 'Up' : 'Down'}`)
    const newWager = Math.max(1, Math.min(100, wager + delta))
    setWager(newWager)
  }

  const handleSpin = () => {
    if (isSpinning) return
    
    playUIClick('Slot Spin')
    setIsSpinning(true)
    
    // TODO: Add actual spinning logic later
    setTimeout(() => {
      setIsSpinning(false)
    }, 2000)
  }

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Chess Slot Machine Body */}
      <div className="relative">
        {/* Machine Frame - Using app's card-gaming style */}
        <div className="card-gaming p-6 rounded-3xl shadow-2xl border border-border">
          {/* Gaming accent border */}
          <div className="absolute inset-2 rounded-2xl border border-primary/20 opacity-60"></div>
          
          {/* Screen */}
          <div className="bg-background/50 backdrop-blur-sm p-4 rounded-xl border border-border shadow-inner">
            {/* Reels Container */}
            <div className="flex space-x-3">
              {reels.map((symbol, index) => (
                <div
                  key={index}
                  className={`
                    w-20 h-24 card-gaming rounded-lg flex items-center justify-center text-4xl
                    border border-border shadow-lg transition-all duration-200
                    ${isSpinning ? 'animate-pulse scale-95' : 'hover:scale-105'}
                  `}
                >
                  <span 
                    className={`
                      text-foreground transition-all duration-300
                      ${isSpinning ? 'animate-bounce text-primary' : ''}
                    `}
                    style={{
                      textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
                    }}
                  >
                    {symbol}
                  </span>
                </div>
              ))}
            </div>
            
            {/* Payline Indicator */}
            <div className="mt-3 h-1 bg-primary rounded-full shadow-lg animate-pulse"></div>
          </div>
          
          {/* Decorative Gaming Elements */}
          <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-8 h-4 bg-primary/80 rounded-full shadow-lg animate-pulse"></div>
          <div className="absolute -top-1 left-1/4 w-2 h-2 bg-accent rounded-full animate-ping animation-delay-500"></div>
          <div className="absolute -top-1 right-1/4 w-2 h-2 bg-primary/60 rounded-full animate-ping animation-delay-1000"></div>
        </div>
      </div>

      {/* Wager Controls */}
      <div className="flex flex-col items-center space-y-4">
        <div className="flex items-center space-x-4 card-gaming px-6 py-3 rounded-xl border border-border">
          <button
            onClick={() => handleWagerChange(-1)}
            className="btn-destructive w-10 h-10 rounded-full flex items-center justify-center"
            disabled={wager <= 1}
          >
            <Minus className="w-5 h-5" />
          </button>
          
          <div className="flex items-center space-x-2 min-w-24 justify-center">
            <Coins className="w-5 h-5 text-accent" />
            <span className="text-2xl font-bold text-foreground">{wager}</span>
          </div>
          
          <button
            onClick={() => handleWagerChange(1)}
            className="btn-secondary w-10 h-10 rounded-full flex items-center justify-center"
            disabled={wager >= 100}
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>

        {/* Spin Button */}
        <button
          onClick={handleSpin}
          disabled={isSpinning}
          className={`
            relative px-8 py-4 rounded-xl font-bold text-xl transition-all duration-200 shadow-lg
            ${isSpinning 
              ? 'btn-muted cursor-not-allowed' 
              : 'btn-primary hover:scale-105 active:scale-95'
            }
          `}
        >
          <div className="flex items-center space-x-2">
            <Play className={`w-6 h-6 ${isSpinning ? 'animate-spin' : ''}`} />
            <span>{isSpinning ? 'SPINNING...' : 'SPIN'}</span>
          </div>
          
          {/* Glowing effect when not spinning */}
          {!isSpinning && (
            <div className="absolute inset-0 rounded-xl bg-primary/20 opacity-0 hover:opacity-100 transition-opacity duration-200"></div>
          )}
        </button>
      </div>

      {/* Status Display */}
      <div className="text-center space-y-2">
        <div className="text-sm text-muted-foreground font-medium">
          {isSpinning ? 'Good Luck!' : 'Ready to Spin'}
        </div>
        <div className="text-xs text-muted-foreground/60">
          Wager: {wager} coins • Max Bet: 100 coins
        </div>
      </div>
    </div>
  )
}