import React from 'react'
import { usePageInstructions } from '../../hooks/core/usePageInstructions'

export const PlayMainPage: React.FC = () => {
  usePageInstructions('play')

  return (
    <section className="space-y-4">
      <div className="card-gaming p-8">
        <h2 className="text-2xl font-bold text-center mb-4">♕ Chess Play Hub ♕</h2>
        <p className="text-muted-foreground text-center">
          Welcome to the Chess Play Hub! Choose your chess experience from the action menu below.
          Play classical chess games or solve challenging puzzles to improve your skills.
        </p>
        <div className="text-center mt-6">
          <div className="text-6xl mb-4">♟️</div>
          <p className="text-sm text-muted-foreground">
            Use the action menu to start playing chess or solving puzzles
          </p>
        </div>
      </div>
    </section>
  )
}