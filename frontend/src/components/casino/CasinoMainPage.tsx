import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'

export const CasinoMainPage: React.FC = () => {
  usePageInstructions('casino')

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <p className="text-muted-foreground text-center">
          Casino Games Hub - Welcome to the chess-themed casino! 
          Choose from our exciting selection of games including slots, blackjack, 
          Texas Hold'em poker, roulette, and craps. All games feature chess piece 
          symbols and themes for a unique gaming experience.
        </p>
      </div>
    </section>
  )
}