
interface AuthBackgroundEffectsProps {
  className?: string;
}

/**
 * Auth Background Effects Component
 * Specialized background effects for authentication pages
 * Auth-themed effects inspired by the app's elegant system
 * Features security/login themed elements with chess motifs
 */
export function AuthBackgroundEffects({ className = '' }: AuthBackgroundEffectsProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Auth-themed gradient - deeper, more secure feeling */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-background/98 to-primary/5" />
      
      {/* Random positioned security orbs */}
      <div className="absolute top-32 left-8 bg-orb-responsive-sm bg-orb-floating bg-orb-floating-accent opacity-20 animate-pulse-glow animate-drift animation-delay-800" />
      <div className="absolute top-12 right-1/3 bg-orb-responsive-xs bg-orb-floating bg-orb-floating-primary opacity-25 animate-pulse-glow animate-hover animation-delay-1800" />
      <div className="absolute bottom-16 left-1/4 bg-orb-responsive-md bg-orb-floating bg-orb-floating-secondary opacity-15 animate-pulse-glow animate-float animation-delay-2400" />
      <div className="absolute top-3/4 right-8 bg-orb-responsive-sm bg-orb-floating bg-orb-floating-accent opacity-30 animate-pulse-glow animate-drift animation-delay-600" />
      
      {/* Scattered chess pieces - different positions */}
      <div className="bg-chess-piece top-8 left-2/3 bg-chess-piece-md chess-piece-color-accent-10 animation-delay-1000">♔</div>
      <div className="bg-chess-piece top-1/2 left-8 bg-chess-piece-sm chess-piece-color-primary-15 animation-delay-1800">♛</div>
      <div className="bg-chess-piece bottom-8 right-1/2 bg-chess-piece-lg chess-piece-color-foreground-8 animation-delay-2200">♜</div>
      <div className="bg-chess-piece top-16 right-12 bg-chess-piece-sm chess-piece-color-muted animation-delay-400">♞</div>
      <div className="bg-chess-piece bottom-1/3 left-12 bg-chess-piece-xs chess-piece-color-accent-12 animation-delay-2800">♟</div>
      <div className="bg-chess-piece top-2/3 right-1/4 bg-chess-piece-sm chess-piece-color-primary-8 animation-delay-1400">♗</div>
      
      {/* Minimal sparkles in unique spots */}
      <div className="bg-sparkle absolute top-20 left-1/2 bg-sparkle-xs bg-sparkle-accent opacity-35 animate-twinkle animation-delay-2000" />
      <div className="bg-sparkle absolute bottom-20 right-1/6 bg-sparkle-sm bg-sparkle-primary opacity-25 animate-twinkle animation-delay-3200" />
      
      {/* Simple geometric elements */}
      <div className="absolute top-1/3 right-4 w-8 h-8 border border-accent/8 rounded-full animate-hover animation-delay-2600 opacity-20" />
      <div className="absolute bottom-1/4 left-4 w-6 h-6 border border-primary/6 rounded-lg animate-drift animation-delay-1200 opacity-25" />
      
      {/* Ambient depth layer */}
      <div className="absolute inset-0 bg-gradient-to-t from-background/10 via-transparent to-background/5" />
    </div>
  );
}