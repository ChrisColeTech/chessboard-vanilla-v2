import React, { useState } from 'react'
import { animated, useSpring } from '@react-spring/web'
import { Plus, Minus, DollarSign, Repeat, X } from 'lucide-react'
import { useAppStore } from '../../../stores/appStore'
import { useUIClickSound } from '../../../hooks/audio/useUIClickSound'

export const BettingControls: React.FC = () => {
  const { playUIClick } = useUIClickSound()
  const pokerGame = useAppStore((state) => state.pokerGame)
  const [betAmount, setBetAmount] = useState(pokerGame.playerBet || 10)

  // Animation for betting controls appearance
  const controlsSpring = useSpring({
    opacity: pokerGame.isPlayerTurn ? 1 : 0.5,
    transform: pokerGame.isPlayerTurn ? 'translateY(0px)' : 'translateY(10px)',
    config: { tension: 120, friction: 14 }
  })

  // Button hover animations
  const useButtonSpring = (isPressed: boolean) => useSpring({
    transform: isPressed ? 'scale(0.95)' : 'scale(1)',
    config: { tension: 300, friction: 10 }
  })

  const handleFold = () => {
    playUIClick('Fold')
    // TODO: Implement fold logic
    console.log('Player folds')
  }

  const handleCheck = () => {
    playUIClick('Check')
    // TODO: Implement check logic
    console.log('Player checks')
  }

  const handleCall = () => {
    playUIClick('Call')
    // TODO: Implement call logic
    console.log(`Player calls $${pokerGame.dealerBet}`)
  }

  const handleRaise = () => {
    playUIClick('Raise')
    // TODO: Implement raise logic
    console.log(`Player raises to $${betAmount}`)
  }

  const handleAllIn = () => {
    playUIClick('All In')
    // TODO: Implement all-in logic
    console.log(`Player goes all-in with $${pokerGame.playerChips}`)
  }

  const adjustBetAmount = (delta: number) => {
    const newAmount = Math.max(
      pokerGame.dealerBet + 10, // Minimum raise
      Math.min(pokerGame.playerChips, betAmount + delta)
    )
    setBetAmount(newAmount)
    playUIClick(delta > 0 ? 'Bet Up' : 'Bet Down')
  }

  const canCheck = pokerGame.dealerBet === 0
  const canCall = pokerGame.dealerBet > 0 && pokerGame.dealerBet < pokerGame.playerChips
  const canRaise = betAmount > pokerGame.dealerBet && betAmount <= pokerGame.playerChips

  return (
    <animated.div style={controlsSpring} className="w-full">
      
      {/* Betting Amount Slider */}
      {!canCheck && (
        <div className="mb-4 bg-card/95 backdrop-blur-sm rounded-xl p-4 shadow-lg border border-border">
          <div className="text-center mb-3">
            <div className="text-sm text-muted-foreground mb-1">Bet Amount</div>
            <div className="text-2xl font-bold">${betAmount}</div>
          </div>
          
          {/* Bet Amount Controls */}
          <div className="flex items-center justify-center gap-3">
            <button
              onClick={() => adjustBetAmount(-10)}
              className="w-10 h-10 bg-secondary hover:bg-secondary/80 rounded-full flex items-center justify-center transition-colors"
              disabled={betAmount <= pokerGame.dealerBet + 10}
            >
              <Minus className="w-4 h-4" />
            </button>
            
            <div className="flex-1 mx-4">
              <input
                type="range"
                min={pokerGame.dealerBet + 10}
                max={pokerGame.playerChips}
                step="10"
                value={betAmount}
                onChange={(e) => setBetAmount(Number(e.target.value))}
                className="w-full accent-primary"
              />
            </div>
            
            <button
              onClick={() => adjustBetAmount(10)}
              className="w-10 h-10 bg-secondary hover:bg-secondary/80 rounded-full flex items-center justify-center transition-colors"
              disabled={betAmount >= pokerGame.playerChips}
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          {/* Quick Bet Buttons */}
          <div className="flex gap-2 mt-3">
            <button
              onClick={() => setBetAmount(pokerGame.dealerBet * 2)}
              className="flex-1 py-2 px-3 bg-accent/20 hover:bg-accent/30 rounded-lg text-xs font-medium transition-colors"
            >
              2x Pot
            </button>
            <button
              onClick={() => setBetAmount(pokerGame.pot)}
              className="flex-1 py-2 px-3 bg-accent/20 hover:bg-accent/30 rounded-lg text-xs font-medium transition-colors"
            >
              Pot
            </button>
            <button
              onClick={() => setBetAmount(pokerGame.playerChips)}
              className="flex-1 py-2 px-3 bg-accent/20 hover:bg-accent/30 rounded-lg text-xs font-medium transition-colors"
            >
              All-In
            </button>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-3">
        
        {/* Fold Button */}
        <animated.button
          onClick={handleFold}
          className="col-span-1 bg-red-600 hover:bg-red-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
          style={useButtonSpring(false)}
        >
          <X className="w-5 h-5" />
          Fold
        </animated.button>

        {/* Check/Call Button */}
        {canCheck ? (
          <animated.button
            onClick={handleCheck}
            className="col-span-1 bg-blue-600 hover:bg-blue-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            style={useButtonSpring(false)}
          >
            <Repeat className="w-5 h-5" />
            Check
          </animated.button>
        ) : canCall ? (
          <animated.button
            onClick={handleCall}
            className="col-span-1 bg-green-600 hover:bg-green-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            style={useButtonSpring(false)}
          >
            <DollarSign className="w-5 h-5" />
            Call ${pokerGame.dealerBet}
          </animated.button>
        ) : (
          <animated.button
            onClick={handleAllIn}
            className="col-span-1 bg-purple-600 hover:bg-purple-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            style={useButtonSpring(false)}
          >
            <DollarSign className="w-5 h-5" />
            All-In ${pokerGame.playerChips}
          </animated.button>
        )}
        
        {/* Raise Button (spans full width when available) */}
        {canRaise && (
          <animated.button
            onClick={handleRaise}
            className="col-span-2 bg-orange-600 hover:bg-orange-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            style={useButtonSpring(false)}
          >
            <Plus className="w-5 h-5" />
            Raise to ${betAmount}
          </animated.button>
        )}
      </div>

      {/* Player Status */}
      <div className="mt-4 text-center">
        <div className="text-sm text-muted-foreground">
          Your chips: <span className="font-bold text-primary">${pokerGame.playerChips}</span>
          {pokerGame.dealerBet > 0 && (
            <span className="ml-4">
              To call: <span className="font-bold text-green-500">${pokerGame.dealerBet}</span>
            </span>
          )}
        </div>
      </div>
    </animated.div>
  )
}