import type { BackgroundEffectProps } from '../../../types/core/backgroundEffects'

/**
 * Gaming Effects Component
 * Renders the original gaming-style background effects including:
 * - Animated floating orbs with glassmorphism
 * - Floating chess pieces with various animations
 * - Sparkle effects with twinkle animations
 * - Theme gradient background
 */
export function GamingEffects({ className = '' }: BackgroundEffectProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Full-screen theme gradient background */}
      <div className="absolute inset-0 bg-gaming-gradient" />
      
      {/* Floating Orbs - Gaming Style */}
      <div className="absolute top-20 left-20 bg-orb-responsive-lg bg-orb-floating bg-orb-floating-primary blur-sm animate-pulse-glow animate-drift animation-delay-500" />
      <div className="absolute top-40 right-32 bg-orb-responsive-md bg-orb-floating bg-orb-floating-secondary blur-sm animate-pulse-glow animate-hover animation-delay-1000" />
      <div className="absolute bottom-32 left-40 bg-orb-responsive-sm-alt bg-orb-floating bg-orb-floating-primary blur-sm animate-pulse-glow animate-float animation-delay-2000" />
      <div className="absolute bottom-20 right-20 bg-orb-responsive-md-alt bg-orb-floating bg-orb-floating-secondary blur-sm animate-pulse-glow animate-drift" />
      
      {/* Floating Chess Pieces */}
      <div className="bg-chess-piece top-1/4 left-1/4 bg-chess-piece-lg chess-piece-color-foreground-15 animation-delay-100">♛</div>
      <div className="bg-chess-piece top-1/3 right-1/3 bg-chess-piece-md chess-piece-color-primary-30 animation-delay-500">♔</div>
      <div className="bg-chess-piece bottom-1/4 right-1/4 bg-chess-piece-md chess-piece-color-foreground-15 animation-delay-1000">♝</div>
      <div className="bg-chess-piece bottom-1/3 left-1/3 bg-chess-piece-md chess-piece-color-primary-20 animation-delay-1500">♞</div>
      <div className="bg-chess-piece top-2/3 left-1/5 bg-chess-piece-md chess-piece-color-foreground-15 animation-delay-2000">♜</div>
      <div className="bg-chess-piece bottom-2/3 right-1/5 bg-chess-piece-sm chess-piece-color-primary-20 animation-delay-800">♟</div>
      
      {/* Sparkle Effects */}
      <div className="bg-sparkle absolute top-1/4 right-1/4 bg-sparkle-lg bg-sparkle-primary animate-twinkle animation-delay-100" />
      <div className="bg-sparkle absolute top-1/3 left-1/3 bg-sparkle-md bg-sparkle-accent animate-twinkle animation-delay-500" />
      <div className="bg-sparkle absolute bottom-1/4 left-1/4 bg-sparkle-lg bg-sparkle-primary animate-twinkle animation-delay-1000" />
      <div className="bg-sparkle absolute bottom-1/3 right-1/3 bg-sparkle-md bg-sparkle-accent animate-twinkle animation-delay-200" />
      <div className="bg-sparkle absolute top-2/3 right-1/5 bg-sparkle-sm bg-sparkle-primary animate-twinkle animation-delay-2000" />
      <div className="bg-sparkle absolute bottom-2/3 left-1/5 bg-sparkle-sm bg-sparkle-accent animate-twinkle animation-delay-1500" />
      
      {/* Additional ambient orbs for depth */}
      <div className="absolute top-1/2 left-1/6 bg-orb-responsive-sm bg-orb-floating bg-orb-floating-primary blur-md animate-pulse-glow animate-hover animation-delay-1500" />
      <div className="absolute top-3/4 right-1/6 bg-orb-responsive-xs bg-orb-floating bg-orb-floating-secondary blur-md animate-pulse-glow animate-drift animation-delay-800" />
      
      {/* More chess pieces for richness */}
      <div className="bg-chess-piece top-1/5 right-1/5 bg-chess-piece-sm chess-piece-color-accent-20 animation-delay-300">♕</div>
      <div className="bg-chess-piece bottom-1/5 left-1/5 bg-chess-piece-sm chess-piece-color-accent-20 animation-delay-1800">♗</div>
    </div>
  )
}