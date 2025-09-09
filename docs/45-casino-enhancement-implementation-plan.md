# Casino Enhancement Implementation Plan - Document 45

## Work Progress Tracking Table

| Phase | Status | Priority | Description |
|-------|--------|----------|-------------|
| Phase 1: Shared Casino Infrastructure | 🟡 Planned | 1 (Highest) | Core utilities, types, services, and hooks for ALL casino games |
| Phase 2: RNG & Game Logic Foundation | 🟡 Planned | 2 (Highest) | Random number generation, win detection, payout calculations |
| Phase 3: Shared Components & Animations | 🟡 Planned | 3 (Highest) | React Spring integration, shared UI components (BetControls, CoinDisplay, etc.) |
| Phase 4: Audio & Haptics System | 🟡 Planned | 4 (High) | Web Audio API, haptic feedback, sound management |
| Phase 5: Balance & State Management | 🟡 Planned | 5 (High) | Enhanced Zustand casino store, persistence, validation |
| Phase 6: Casino Index Page | 🟡 Planned | 6 (High) | Main casino page with game selection, stats, and navigation |
| Phase 7: Enhanced Slots Page | 🟡 Planned | 7 (High) | Complete slot machine implementation using shared infrastructure |
| Phase 8: Mobile Optimization | 🟡 Planned | 8 (Medium) | Touch gestures, performance, battery optimization |
| Phase 9: Blackjack Page | 🟡 Planned | 9 (Low) | Single-player blackjack page using shared casino services |
| Phase 10: Video Poker Page | 🟡 Planned | 10 (Low) | Jacks or Better video poker page using shared infrastructure |
| Phase 11: PWA Features | 🟡 Planned | 11 (Low) | Service workers, offline play, installation |

## Project Structure Overview

```
src/
├── components/
│   └── casino/              # Casino game components
│       ├── shared/          # Shared UI components (BetControls, CoinDisplay, etc.)
│       ├── slots/           # Slot machine specific components
│       ├── blackjack/       # Blackjack specific components
│       └── poker/           # Video poker specific components
├── hooks/
│   └── casino/              # Casino-specific React hooks (useCasinoAudio, useSlotMachine, etc.)
├── services/
│   └── casino/              # Casino game logic and external services (RNG, PayoutCalculation, etc.)
├── types/
│   └── casino/              # Casino TypeScript type definitions
├── utils/
│   └── casino/              # Casino pure utility functions (currency, validation, etc.)
├── constants/
│   └── casino/              # Casino game configuration constants (payouts, symbols, etc.)
├── animations/
│   └── casino/              # Casino React Spring animation configs
├── pages/
│   └── casino/              # Casino pages
│       ├── CasinoIndexPage.tsx  # Main casino page with game selection and overview
│       ├── SlotsPage.tsx        # Enhanced slots page using shared casino infrastructure
│       ├── BlackjackPage.tsx    # Blackjack page using shared casino services  
│       └── VideoPokerPage.tsx   # Video poker page using shared casino infrastructure
└── stores/
    └── casinoStore.ts       # Casino-specific Zustand store (shared across all games)
```

---

## Phase 1: Foundation (Priority 1 - Highest)

### Overview
Establish core infrastructure for casino games including types, utilities, services, and foundational hooks following SRP and DRY principles.

### Files to Create
- `src/types/casino/index.ts`
- `src/types/casino/slot-machine.types.ts`
- `src/types/casino/casino-game.types.ts`
- `src/types/casino/audio.types.ts`
- `src/utils/casino/index.ts`
- `src/utils/casino/random.utils.ts`
- `src/utils/casino/currency.utils.ts`
- `src/utils/casino/validation.utils.ts`
- `src/constants/casino/index.ts`
- `src/constants/casino/slot-symbols.constants.ts`
- `src/constants/casino/payout-tables.constants.ts`
- `src/services/casino/index.ts`
- `src/services/casino/CasinoRNGService.ts`
- `src/hooks/casino/index.ts`
- `src/hooks/casino/useCasinoAudio.ts`
- `src/hooks/casino/useHapticFeedback.ts`

### Files to Modify
- `src/types/index.ts` (add casino type exports)
- `src/components/layout/types.ts` (add casino tab types)

### Integration Points (Files Used But Not Modified)
- `src/stores/appStore.ts` (for coinBalance state)
- `src/services/audio/audioService.ts` (for base audio functionality)
- `src/components/layout/TabBar.tsx` (existing casino tab)

### Key Deliverables
1. **Type System**: Complete TypeScript definitions for all casino games
2. **Crypto RNG**: `crypto.getRandomValues()` implementation replacing `Math.random()` for provably fair gaming
3. **Currency Utils**: Chess-themed coin formatting with comma separators, balance validation (minimum 0)
4. **Audio Foundation**: Web Audio API setup with 64kbps MP3 compression, <50KB file sizes, audio pooling
5. **Haptic System**: Vibration API patterns - `[200]` for wins, `[100,50,100]` for big wins, with user toggle

### Research-Based Implementation Details

**CasinoRNGService.ts**:
```typescript
// Cryptographically secure RNG
const generateSecureRandom = (): number => {
  const array = new Uint32Array(1)
  crypto.getRandomValues(array)
  return array[0] / (0xFFFFFFFF + 1)
}

// Weighted symbol selection with chess pieces
const CHESS_SYMBOL_WEIGHTS = {
  '♔': 0.05, // King - 5% (rarest)
  '♕': 0.08, // Queen - 8%
  '♖': 0.12, // Rook - 12%
  '♗': 0.15, // Bishop - 15%
  '♘': 0.15, // Knight - 15%
  '♙': 0.20, // Pawn - 20% (most common)
  // Black pieces with same weights
}
```

**hooks/casino/useCasinoAudio.ts**:
```typescript
// Battery-efficient audio with preloading
const AUDIO_CONFIG = {
  spinSound: { duration: 1.5, volume: 0.8 },
  winSound: { duration: 0.5, volume: 1.0 },
  ambientVolume: 0.2, // 20% background, 80% effects
  maxConcurrentSounds: 3
}
```

**hooks/casino/useHapticFeedback.ts**:
```typescript
// Vibration patterns from research
const HAPTIC_PATTERNS = {
  spin: [100],
  smallWin: [200],
  bigWin: [100, 50, 100, 50, 200],
  maxDuration: 500 // Battery optimization
}
```

---

## Phase 2: RNG & Game Logic (Priority 2 - High)

### Overview
Implement core game logic systems including weighted randomization, win detection, and payout calculations.

### Files to Create
- `src/services/casino/SlotGameLogic.ts`
- `src/services/casino/WinDetectionService.ts`
- `src/services/casino/PayoutCalculationService.ts`
- `src/utils/casino/slot-game.utils.ts`
- `src/utils/casino/probability.utils.ts`
- `src/hooks/casino/useSlotMachine.ts`
- `src/constants/casino/slot-paylines.constants.ts`
- `src/constants/casino/win-combinations.constants.ts`

### Files to Modify
- `src/services/casino/index.ts` (add exports)
- `src/hooks/casino/index.ts` (add exports)

### Integration Points
- `src/services/casino/CasinoRNGService.ts` (from Phase 1)
- `src/constants/casino/payout-tables.constants.ts` (from Phase 1)
- `src/stores/appStore.ts` (for balance updates)

### Key Deliverables
1. **Weighted RNG**: Chess piece probability distribution with near-miss logic (15-20% of losing spins)
2. **Payline Evaluation**: Single center line `[1,1,1]` optimized for mobile screens
3. **Chess Payout System**: Pawn=2x, Rook=5x, Knight=8x, Bishop=10x, Queen=25x, King=100x
4. **Game Hook**: Complete slot machine cycle with balance validation and win celebration
5. **Mathematical Testing**: RTP verification and randomness validation with deterministic seeds

### Research-Based Implementation Details

**services/casino/SlotGameLogic.ts**:
```typescript
// Chess-themed payout table from research
const CHESS_PAYOUTS = {
  '♙♙♙': 2,   // Triple Pawn
  '♖♖♖': 5,   // Triple Rook 
  '♘♘♘': 8,   // Triple Knight
  '♗♗♗': 10,  // Triple Bishop
  '♕♕♕': 25,  // Triple Queen
  '♔♔♔': 100, // Triple King (jackpot)
}

// Near-miss implementation
const generateNearMiss = (symbols: string[]): boolean => {
  return Math.random() < 0.18 // 18% near-miss rate
}
```

**services/casino/WinDetectionService.ts**:
```typescript
// Single payline for mobile optimization
const MOBILE_PAYLINES = [
  [1, 1, 1] // Center line only for 3-reel mobile slot
]

// Win detection with visual feedback timing
const detectWin = (reels: string[]): WinResult => {
  const winAmount = CHESS_PAYOUTS[reels.join('')] || 0
  return {
    isWin: winAmount > 0,
    amount: winAmount,
    highlightDuration: 2000, // 2s win animation
    celebrationLevel: winAmount >= 25 ? 'big' : 'small'
  }
}
```

**hooks/casino/useSlotMachine.ts**:
```typescript
// Complete game cycle with research-based timing
const useSlotMachine = () => {
  const [isSpinning, setIsSpinning] = useState(false)
  const [reels, setReels] = useState(['♔', '♛', '♖'])
  
  const spin = useCallback(async () => {
    if (balance < wager) return // Balance validation
    
    setIsSpinning(true)
    setCoinBalance(prev => prev - wager) // Deduct immediately
    
    // 2-3 second spin with 200-300ms stagger
    await animateReels(2500, [0, 200, 400]) // Stagger delays
    
    const result = generateSpinResult()
    setReels(result.symbols)
    
    if (result.isWin) {
      setCoinBalance(prev => prev + result.winAmount)
      triggerWinCelebration(result.celebrationLevel)
    }
    
    setIsSpinning(false)
  }, [balance, wager])
}
```

---

## Phase 3: Animation System (Priority 3 - High)

### Overview
Implement React Spring-based animation system for smooth, performant mobile gaming experiences.

### Files to Create
- `src/animations/casino/index.ts`
- `src/animations/casino/slot-reel.animations.ts`
- `src/animations/casino/win-celebration.animations.ts`
- `src/animations/casino/ui-feedback.animations.ts`
- `src/hooks/casino/useSlotAnimations.ts`
- `src/hooks/casino/useSpringTransitions.ts`
- `src/components/casino/shared/AnimatedCounter.tsx`
- `src/components/casino/shared/SpringTransition.tsx`

### Files to Modify
- `src/hooks/casino/index.ts` (add animation hooks)
- `src/components/casino/shared/index.ts` (create and add exports)

### Integration Points
- `src/hooks/casino/useSlotMachine.ts` (from Phase 2)
- `src/hooks/casino/useHapticFeedback.ts` (from Phase 1)
- React Spring library (external dependency)

### Key Deliverables
1. **React Spring Reels**: Hardware-accelerated spinning with `transform: translateY()` and spring physics
2. **Win Celebrations**: Scale/rotate effects for winning symbols, glowing borders, 1-2 second animations
3. **Touch Feedback**: 16ms response time with visual feedback (scale animation on tap)
4. **60fps Performance**: `will-change: transform`, easing curves (`ease-out`), <16ms render times
5. **Mobile Optimized**: Reduced motion accessibility option, prevent motion sickness patterns

### Research-Based Implementation Details

**animations/casino/slot-reel.animations.ts**:
```typescript
// Hardware-accelerated spinning from research
const useReelSpring = (isSpinning: boolean, symbols: string[]) => {
  const springProps = useSpring({
    transform: isSpinning 
      ? 'translateY(-2000px)' // 2000px spin distance
      : 'translateY(0px)',
    config: {
      tension: 120,
      friction: 14,
      // Realistic deceleration curve
    },
    onRest: () => {
      // Reel stopped, trigger next reel with 200ms delay
    }
  })
  
  return {
    ...springProps,
    willChange: 'transform', // Hardware acceleration hint
  }
}

// Staggered reel stopping (authentic casino feel)
const REEL_STOP_DELAYS = [0, 200, 400] // ms between reel stops
```

**animations/casino/win-celebration.animations.ts**:
```typescript
// Win animation patterns from research
const useWinAnimation = (isWinning: boolean, winLevel: 'small' | 'big') => {
  const celebration = useSpring({
    scale: isWinning ? 1.1 : 1.0,
    rotateZ: isWinning ? 5 : 0,
    boxShadow: isWinning 
      ? '0 0 20px rgba(255, 215, 0, 0.8)' // Golden glow
      : '0 0 0px rgba(255, 215, 0, 0)',
    config: { duration: winLevel === 'big' ? 2000 : 1000 }
  })
  
  return celebration
}

// Near-miss "hesitation" effect
const useNearMissEffect = (isNearMiss: boolean) => {
  return useSpring({
    transform: isNearMiss 
      ? 'translateY(-10px) translateY(0px)' // Brief hesitation
      : 'translateY(0px)',
    config: { tension: 300, friction: 10 }
  })
}
```

**animations/casino/ui-feedback.animations.ts**:
```typescript
// Button feedback with 16ms response target
const useTouchFeedback = (isPressed: boolean) => {
  return useSpring({
    scale: isPressed ? 0.95 : 1.0,
    backgroundColor: isPressed ? '#4ade80' : '#22c55e',
    config: { duration: 150 }, // Sub-16ms response
    immediate: false
  })
}

// Accessibility: Reduced motion support
const useAccessibleAnimation = (normalConfig: any) => {
  const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)')
  
  return prefersReducedMotion 
    ? { ...normalConfig, config: { duration: 0 } } // Instant
    : normalConfig
}
```

---

## Phase 4: Audio & Haptics (Priority 4 - Medium)

### Overview
Enhanced audio system with haptic feedback integration for immersive mobile gaming experience.

### Files to Create
- `src/services/casino/CasinoAudioService.ts`
- `src/services/casino/HapticFeedbackService.ts`
- `src/constants/casino/audio-config.constants.ts`
- `src/constants/casino/haptic-patterns.constants.ts`
- `src/utils/casino/audio.utils.ts`

### Files to Modify
- `src/hooks/casino/useCasinoAudio.ts` (enhance from Phase 1)
- `src/hooks/casino/useHapticFeedback.ts` (enhance from Phase 1)
- `src/services/casino/index.ts` (add exports)

### Integration Points
- `src/services/audio/audioService.ts` (base audio system)
- `src/stores/appStore.ts` (audio settings)
- Web Audio API and Vibration API (browser APIs)

### Key Deliverables
1. **Web Audio Integration**: 64kbps MP3 files <50KB each, audio context state detection for silent mode
2. **Haptic Patterns**: Research-specific vibration sequences with 500ms maximum duration
3. **Battery Efficiency**: Audio pooling, preload essential sounds only, pause when page not visible
4. **Cross-Device Audio**: Headphones vs speakers detection, volume mixing (ambient 20%, effects 80%)
5. **Accessibility**: Visual waveform indicators, captions for audio cues, ARIA labels

### Research-Based Implementation Details

**services/casino/CasinoAudioService.ts**:
```typescript
// Battery-efficient audio from research findings
class CasinoAudioService {
  private audioPool = new Map<string, HTMLAudioElement[]>()
  private maxConcurrentSounds = 3
  
  // Preload only essential sounds (research: avoid background loops)
  async preloadEssentials() {
    const essentialSounds = [
      { id: 'spin', src: '/audio/spin.mp3', duration: 1500 },
      { id: 'win', src: '/audio/win.mp3', duration: 500 },
      { id: 'coin', src: '/audio/coin.mp3', duration: 300 }
    ]
    
    // Create audio pool for reuse
    for (const sound of essentialSounds) {
      this.audioPool.set(sound.id, [])
      for (let i = 0; i < 2; i++) { // Pool of 2 per sound
        const audio = new Audio(sound.src)
        audio.preload = 'auto'
        this.audioPool.get(sound.id)!.push(audio)
      }
    }
  }
  
  // Silent mode detection
  async playSafely(soundId: string, volume = 1.0) {
    if (document.visibilityState === 'hidden') return // Battery optimization
    
    try {
      await this.audioContext.resume() // Handle autoplay policy
      const audioPool = this.audioPool.get(soundId)
      if (!audioPool) return
      
      const availableAudio = audioPool.find(audio => audio.paused)
      if (availableAudio) {
        availableAudio.volume = volume * this.masterVolume
        availableAudio.currentTime = 0
        await availableAudio.play()
      }
    } catch (error) {
      // Graceful fallback - show visual feedback instead
      this.showVisualFeedback(soundId)
    }
  }
}
```

**services/casino/HapticFeedbackService.ts**:
```typescript
// Research-based haptic patterns
const HAPTIC_LIBRARY = {
  // From research: specific patterns for casino events
  spin: [100], // Short tap for spin start
  smallWin: [200], // Medium buzz for small wins
  bigWin: [100, 50, 100, 50, 200], // Complex pattern for big wins
  jackpot: [200, 100, 200, 100, 500], // Dramatic pattern
  error: [50, 50, 50], // Triple short for errors
}

class HapticService {
  private isEnabled = true
  private maxDuration = 500 // Battery optimization from research
  
  async vibrate(pattern: keyof typeof HAPTIC_LIBRARY) {
    if (!this.isEnabled || !navigator.vibrate) return
    
    const vibrationPattern = HAPTIC_LIBRARY[pattern]
    const totalDuration = vibrationPattern.reduce((sum, val) => sum + val, 0)
    
    // Respect battery optimization limit
    if (totalDuration <= this.maxDuration) {
      navigator.vibrate(vibrationPattern)
    }
  }
  
  // User preference toggle
  setEnabled(enabled: boolean) {
    this.isEnabled = enabled
    // Store in localStorage for persistence
    localStorage.setItem('hapticEnabled', enabled.toString())
  }
}
```

**constants/casino/audio-config.constants.ts**:
```typescript
// Research-based audio configuration
export const CASINO_AUDIO_CONFIG = {
  // File optimization from research
  compression: '64kbps', // Mobile data efficiency
  maxFileSize: 50000, // 50KB limit
  formats: ['mp3', 'ogg'], // MP3 primary, OGG fallback
  
  // Volume mixing ratios from research
  volumeMix: {
    ambient: 0.2,  // 20% background
    effects: 0.8,  // 80% sound effects
  },
  
  // Battery optimization settings
  pauseOnHidden: true, // Pause when tab not visible
  maxConcurrent: 3,    // Limit simultaneous sounds
  poolSize: 2,         // Audio instance reuse
  
  // Accessibility features
  visualIndicators: {
    spinSound: '🎰 Spinning...',
    winSound: '🎉 You won!', 
    coinSound: '🪙 Coins added',
    errorSound: '❌ Error occurred'
  }
} as const
```

---

## Phase 5: Enhanced Slot Components (Priority 5 - Medium)

### Overview
Build complete, functional slot machine components with full game integration.

### Files to Create
- `src/components/casino/slots/EnhancedSlotMachine.tsx`
- `src/components/casino/slots/SlotReel.tsx`
- `src/components/casino/slots/ReelSymbol.tsx`
- `src/components/casino/slots/WinLineIndicator.tsx`
- `src/components/casino/slots/BetControls.tsx`
- `src/components/casino/slots/SpinButton.tsx`
- `src/components/casino/slots/WinCelebration.tsx`
- `src/components/casino/shared/CoinDisplay.tsx`
- `src/components/casino/shared/GameLayout.tsx`

### Files to Modify
- `src/components/casino/slots/index.ts` (create and add exports)
- `src/components/SlotMachine.tsx` (deprecate or refactor)

### Integration Points
- `src/hooks/casino/useSlotMachine.ts` (from Phase 2)
- `src/hooks/casino/useSlotAnimations.ts` (from Phase 3)
- `src/hooks/casino/useCasinoAudio.ts` (from Phase 4)
- `src/stores/appStore.ts` (coin balance)

### Key Deliverables
1. **Touch-Optimized Components**: 44x44px minimum touch targets, 500ms hold-to-repeat betting
2. **Complete Game Integration**: All research findings implemented in working slot machine
3. **Mobile-First Design**: Portrait orientation, safe areas for notched devices, responsive 320px-1024px
4. **Chess Casino Aesthetic**: Professional gambling UI with chess theme integration
5. **Full Accessibility**: WCAG 2.1 AA compliance, screen readers, reduce motion support

### Research-Based Implementation Details

**components/casino/slots/EnhancedSlotMachine.tsx**:
```typescript
// Mobile-optimized slot machine from research
const EnhancedSlotMachine: React.FC<SlotMachineProps> = ({ coinBalance, setCoinBalance }) => {
  const { spin, isSpinning, reels, winResult } = useSlotMachine()
  const { playSound } = useCasinoAudio()
  const { vibrate } = useHapticFeedback()
  const springProps = useSlotAnimations(isSpinning, reels)
  
  // Touch-friendly bet controls from research
  const handleBetAdjust = useCallback((delta: number) => {
    const newWager = Math.max(1, Math.min(100, wager + delta))
    setWager(newWager)
    vibrate('spin') // Haptic feedback for adjustment
  }, [wager])
  
  // Research: 500ms hold-to-repeat functionality 
  const { isHolding, startHold, stopHold } = useHoldToRepeat(handleBetAdjust, 500)
  
  return (
    <div className="slot-machine" style={{
      // Safe area handling for notched devices
      paddingTop: 'env(safe-area-inset-top)',
      paddingBottom: 'env(safe-area-inset-bottom)',
    }}>
      {/* Reels with hardware acceleration */}
      <div className="reels-container">
        {reels.map((symbol, index) => (
          <SlotReel
            key={index}
            symbol={symbol}
            isSpinning={isSpinning}
            delay={REEL_STOP_DELAYS[index]} // 0, 200, 400ms stagger
            style={{
              willChange: 'transform', // GPU acceleration
              ...springProps[index]
            }}
          />
        ))}
      </div>
      
      {/* Touch-optimized controls */}
      <div className="bet-controls">
        <TouchButton
          size="large" // 60x60px from research
          onMouseDown={() => startHold(-1)}
          onMouseUp={stopHold}
          onTouchStart={() => startHold(-1)}
          onTouchEnd={stopHold}
          disabled={wager <= 1}
          hapticFeedback="spin"
        >
          <Minus className="w-6 h-6" />
        </TouchButton>
        
        <CoinDisplay amount={wager} />
        
        <TouchButton
          size="large"
          onMouseDown={() => startHold(1)}
          onMouseUp={stopHold}
          onTouchStart={() => startHold(1)}
          onTouchEnd={stopHold}
          disabled={wager >= 100}
          hapticFeedback="spin"
        >
          <Plus className="w-6 h-6" />
        </TouchButton>
      </div>
      
      {/* Accessible spin button */}
      <SpinButton
        onClick={spin}
        disabled={isSpinning || coinBalance < wager}
        isSpinning={isSpinning}
        aria-label={`Spin reels for ${wager} coins`}
        style={{
          minHeight: '60px', // Touch target size
          minWidth: '120px',
        }}
      />
    </div>
  )
}
```

**components/casino/slots/SlotReel.tsx**:
```typescript
// Individual reel with React Spring physics
const SlotReel: React.FC<SlotReelProps> = ({ symbol, isSpinning, delay }) => {
  const springProps = useSpring({
    transform: isSpinning 
      ? 'translateY(-2000px)' // Research: 2000px spin distance
      : 'translateY(0px)',
    config: {
      tension: 120, // Spring physics for realistic deceleration
      friction: 14,
    },
    delay: delay, // Staggered stopping
  })
  
  return (
    <animated.div 
      className="slot-reel"
      style={{
        ...springProps,
        willChange: 'transform', // Hardware acceleration hint
      }}
    >
      <div className="symbol" style={{
        fontSize: '3rem', // Large enough for mobile
        textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)', // Readability
      }}>
        {symbol}
      </div>
    </animated.div>
  )
}
```

**components/casino/slots/BetControls.tsx**:
```typescript
// Research-based betting interface
const BetControls: React.FC = () => {
  // Prevent accidental max bets (research finding)
  const handleMaxBet = () => {
    const maxBetThreshold = coinBalance * 0.5 // 50% of balance
    if (wager > maxBetThreshold) {
      // Confirmation modal for large bets
      setShowConfirmation(true)
    } else {
      setWager(Math.min(100, coinBalance))
    }
  }
  
  return (
    <div className="bet-controls-grid">
      {/* Research: Visual feedback on all touches */}
      <TouchButton 
        variant="decrease"
        disabled={wager <= 1}
        onPress={() => {
          vibrate('spin')
          handleBetAdjust(-1)
        }}
        style={{
          minWidth: '44px', // iOS HIG minimum
          minHeight: '44px',
        }}
      >
        <Minus />
      </TouchButton>
      
      {/* Research: Clear wager display with coin icon */}
      <div className="wager-display">
        <Coins className="w-5 h-5 text-accent" />
        <span className="text-2xl font-bold">{wager}</span>
      </div>
      
      <TouchButton 
        variant="increase"
        disabled={wager >= 100 || wager >= coinBalance}
        onPress={() => {
          vibrate('spin')
          handleBetAdjust(1)
        }}
      >
        <Plus />
      </TouchButton>
    </div>
  )
}
```

---

## Phase 6: Casino Index Page (Priority 6 - High)

### Overview
Enhanced state management with comprehensive balance tracking, transaction logging, and persistence.

### Files to Create
- `src/stores/casinoStore.ts`
- `src/services/casino/BalanceService.ts`
- `src/services/casino/TransactionLogger.ts`
- `src/utils/casino/storage.utils.ts`
- `src/hooks/casino/useCasinoBalance.ts`
- `src/hooks/casino/useGameSession.ts`
- `src/types/casino/transaction.types.ts`

### Files to Modify
- `src/stores/appStore.ts` (integrate casino store)
- `src/types/casino/index.ts` (add transaction types)
- `src/hooks/casino/index.ts` (add balance hooks)

### Integration Points
- Zustand persistence middleware
- IndexedDB/localStorage APIs
- All casino components (for balance updates)

### Key Deliverables
1. **Zustand Casino Store**: Persistent store with `partialize` for selective localStorage sync
2. **Atomic Balance Updates**: Functional updates `setBalance(prev => prev - wager)` preventing race conditions
3. **IndexedDB Transactions**: Structured logging with Dexie.js, schema: `{gameType, timestamp, bet, winAmount, balance}`
4. **Session Persistence**: `beforeunload` + `visibilitychange` handlers for state backup
5. **Balance Validation**: Prevent negative balances, insufficient funds graceful handling

### Research-Based Implementation Details

**stores/casinoStore.ts**:
```typescript
// Research-optimized Zustand store
interface CasinoState {
  // Game state
  coinBalance: number
  currentGame: 'slots' | 'blackjack' | 'poker' | null
  gameSession: GameSession
  
  // Transaction tracking
  transactionHistory: Transaction[]
  sessionStats: SessionStats
  
  // UI state
  isGameActive: boolean
  lastWinAmount: number
}

interface CasinoActions {
  // Atomic balance operations from research
  placeBet: (amount: number) => boolean // Returns false if insufficient funds
  addWinnings: (amount: number) => void
  resetBalance: () => void
  
  // Transaction logging
  logTransaction: (transaction: Transaction) => void
  getGameHistory: (gameType: string) => Transaction[]
  
  // Session management
  startGameSession: (gameType: string) => void
  endGameSession: () => void
}

export const useCasinoStore = create<CasinoState & CasinoActions>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        // Initial state
        coinBalance: 1000, // Starting balance
        currentGame: null,
        gameSession: null,
        transactionHistory: [],
        sessionStats: { totalWagered: 0, totalWon: 0, sessionsPlayed: 0 },
        isGameActive: false,
        lastWinAmount: 0,
        
        // Research: Atomic balance operations prevent race conditions
        placeBet: (amount: number) => {
          const { coinBalance } = get()
          if (coinBalance < amount) {
            // Research: Graceful insufficient funds handling
            return false
          }
          
          set((state) => ({ 
            coinBalance: state.coinBalance - amount,
            // Log transaction immediately
            transactionHistory: [
              ...state.transactionHistory,
              {
                id: crypto.randomUUID(),
                gameType: state.currentGame!,
                type: 'bet',
                amount: -amount,
                balance: state.coinBalance - amount,
                timestamp: Date.now()
              }
            ]
          }))
          
          return true
        },
        
        addWinnings: (amount: number) => {
          set((state) => ({
            coinBalance: state.coinBalance + amount,
            lastWinAmount: amount,
            transactionHistory: [
              ...state.transactionHistory,
              {
                id: crypto.randomUUID(), 
                gameType: state.currentGame!,
                type: 'win',
                amount: amount,
                balance: state.coinBalance + amount,
                timestamp: Date.now()
              }
            ]
          }))
        },
        
        // Research: Session tracking for analytics
        startGameSession: (gameType: string) => {
          set({
            currentGame: gameType as any,
            isGameActive: true,
            gameSession: {
              id: crypto.randomUUID(),
              gameType,
              startTime: Date.now(),
              startBalance: get().coinBalance
            }
          })
        },
        
        endGameSession: () => {
          const { gameSession, coinBalance } = get()
          if (gameSession) {
            // Log session completion
            set((state) => ({
              sessionStats: {
                ...state.sessionStats,
                sessionsPlayed: state.sessionStats.sessionsPlayed + 1
              },
              isGameActive: false,
              currentGame: null,
              gameSession: null
            }))
          }
        }
      }),
      {
        name: 'casino-store',
        // Research: Selective persistence to optimize localStorage
        partialize: (state) => ({
          coinBalance: state.coinBalance,
          transactionHistory: state.transactionHistory.slice(-100), // Keep last 100
          sessionStats: state.sessionStats,
        }),
        onRehydrateStorage: () => (state) => {
          // Restore game session on reload
          if (state?.gameSession) {
            state.isGameActive = true
          }
        }
      }
    )
  )
)
```

**services/casino/BalanceService.ts**:
```typescript
// Research-based balance validation service
class BalanceService {
  // Prevent race conditions with functional updates
  static validateBet(balance: number, wager: number): ValidationResult {
    if (balance < wager) {
      return {
        isValid: false,
        error: 'Insufficient balance',
        suggestedAction: 'reduce-bet',
        maxBet: balance
      }
    }
    
    // Research: Warn on large bets (>50% balance)
    if (wager > balance * 0.5) {
      return {
        isValid: true,
        warning: 'Large bet detected',
        requiresConfirmation: true
      }
    }
    
    return { isValid: true }
  }
  
  // Format currency with commas (research requirement)
  static formatCoins(amount: number): string {
    return new Intl.NumberFormat('en-US').format(amount)
  }
}
```

**hooks/casino/useCasinoBalance.ts**:
```typescript
// Research-optimized balance hook
const useCasinoBalance = () => {
  const balance = useCasinoStore(state => state.coinBalance)
  const placeBet = useCasinoStore(state => state.placeBet)
  const addWinnings = useCasinoStore(state => state.addWinnings)
  
  // Research: Debounced balance updates for rapid interactions
  const debouncedBalance = useDebounce(balance, 100)
  
  const handleBet = useCallback((amount: number) => {
    const success = placeBet(amount)
    if (!success) {
      // Research: User feedback for insufficient funds
      toast.error('Insufficient coins! Bet reduced to maximum available.')
      return false
    }
    return true
  }, [placeBet])
  
  return {
    balance: debouncedBalance,
    formattedBalance: BalanceService.formatCoins(balance),
    handleBet,
    addWinnings,
    canAfford: (amount: number) => balance >= amount
  }
}
```

---

## Phase 7: Mobile Optimization (Priority 7 - Medium)

### Overview
Mobile-specific optimizations for touch interactions, performance, and battery efficiency.

### Files to Create
- `src/hooks/casino/useTouchGestures.ts`
- `src/hooks/casino/usePerformanceMonitoring.ts`
- `src/utils/casino/mobile-detection.utils.ts`
- `src/utils/casino/performance.utils.ts`
- `src/services/casino/PerformanceService.ts`
- `src/components/casino/shared/TouchFeedback.tsx`

### Files to Modify
- All casino components (add mobile optimizations)
- `src/hooks/casino/index.ts` (add mobile hooks)
- `src/utils/casino/index.ts` (add mobile utils)

### Integration Points
- All existing casino components
- Performance Observer API
- Battery API (when available)
- Screen Wake Lock API

### Key Deliverables
1. **Touch Gestures**: Tap primary actions, long-press (500ms+) for rapid bet adjust, 44px minimum targets
2. **Performance Tracking**: `performance.now()` frame timing, FPS counter, <16ms React render target
3. **Battery Optimization**: Pause animations when `visibilityState === 'hidden'`, reduce complexity on low battery
4. **Responsive Design**: CSS Grid `minmax()`, 320px-1024px viewport support, orientation handling
5. **Mobile Accessibility**: Screen reader support, high contrast mode, reduce motion preferences

### Research-Based Implementation Details

**hooks/casino/useTouchGestures.ts**:
```typescript
// Research-based touch interaction patterns
const useTouchGestures = () => {
  const [isLongPressing, setIsLongPressing] = useState(false)
  const longPressTimer = useRef<number>()
  
  // Research: 500ms+ long press for rapid bet adjustment
  const handleTouchStart = useCallback((action: () => void) => {
    longPressTimer.current = window.setTimeout(() => {
      setIsLongPressing(true)
      // Start rapid repeat every 100ms
      const interval = setInterval(action, 100)
      
      const cleanup = () => {
        clearInterval(interval)
        setIsLongPressing(false)
      }
      
      // Research: Clean up on touch end
      const handleTouchEnd = () => {
        cleanup()
        document.removeEventListener('touchend', handleTouchEnd)
      }
      
      document.addEventListener('touchend', handleTouchEnd)
    }, 500) // Research: 500ms threshold
  }, [])
  
  const handleTouchEnd = useCallback(() => {
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current)
    }
  }, [])
  
  return { handleTouchStart, handleTouchEnd, isLongPressing }
}
```

**hooks/casino/usePerformanceMonitoring.ts**:
```typescript
// Research: Performance monitoring for 60fps target
const usePerformanceMonitoring = () => {
  const [performanceMetrics, setPerformanceMetrics] = useState({
    fps: 60,
    frameTime: 16.67,
    memoryUsage: 0,
    isLowPerformance: false
  })
  
  useEffect(() => {
    let lastTime = performance.now()
    let frameCount = 0
    
    const measurePerformance = () => {
      const now = performance.now()
      const frameTime = now - lastTime
      frameCount++
      
      // Calculate FPS every 60 frames
      if (frameCount >= 60) {
        const fps = 1000 / (frameTime / frameCount)
        
        setPerformanceMetrics(prev => ({
          ...prev,
          fps: Math.round(fps),
          frameTime: frameTime / frameCount,
          isLowPerformance: fps < 45 // Research: Below 45fps = low performance
        }))
        
        frameCount = 0
      }
      
      lastTime = now
      requestAnimationFrame(measurePerformance)
    }
    
    requestAnimationFrame(measurePerformance)
    
    // Memory monitoring
    if ('memory' in performance) {
      const updateMemory = () => {
        const memory = (performance as any).memory
        setPerformanceMetrics(prev => ({
          ...prev,
          memoryUsage: Math.round(memory.usedJSHeapSize / 1024 / 1024) // MB
        }))
      }
      
      const interval = setInterval(updateMemory, 5000) // Every 5s
      return () => clearInterval(interval)
    }
  }, [])
  
  return performanceMetrics
}
```

**utils/casino/mobile-detection.utils.ts**:
```typescript
// Research: Device capability detection
export const MobileDetection = {
  // Detect device performance tier
  getPerformanceTier(): 'low' | 'medium' | 'high' {
    const cores = navigator.hardwareConcurrency || 2
    const memory = (navigator as any).deviceMemory || 2
    
    // Research-based performance tiers
    if (cores >= 8 && memory >= 4) return 'high'
    if (cores >= 4 && memory >= 2) return 'medium'
    return 'low'
  },
  
  // Battery level detection for optimization
  async getBatteryInfo() {
    if ('getBattery' in navigator) {
      const battery = await (navigator as any).getBattery()
      return {
        level: battery.level,
        charging: battery.charging,
        isLowBattery: battery.level < 0.2 // Below 20%
      }
    }
    return null
  },
  
  // Network quality detection
  getNetworkQuality(): 'slow' | 'fast' | 'unknown' {
    const connection = (navigator as any).connection
    if (!connection) return 'unknown'
    
    // Research: Optimize for slow connections
    const slowTypes = ['slow-2g', '2g', '3g']
    return slowTypes.includes(connection.effectiveType) ? 'slow' : 'fast'
  }
}
```

**components/casino/shared/TouchFeedback.tsx**:
```typescript
// Research: 16ms touch response target
const TouchFeedback: React.FC<TouchFeedbackProps> = ({ 
  children, 
  onPress, 
  hapticType = 'spin',
  minSize = 44 // Research: 44px minimum for accessibility
}) => {
  const [isPressed, setIsPressed] = useState(false)
  const { vibrate } = useHapticFeedback()
  
  // Research: Sub-16ms visual feedback
  const pressStyle = useSpring({
    scale: isPressed ? 0.95 : 1.0,
    backgroundColor: isPressed ? 'rgba(34, 197, 94, 0.8)' : 'rgba(34, 197, 94, 1)',
    config: { tension: 300, friction: 10 }, // Fast response
  })
  
  const handlePressStart = useCallback(() => {
    setIsPressed(true)
    vibrate(hapticType) // Immediate haptic feedback
  }, [vibrate, hapticType])
  
  const handlePressEnd = useCallback(() => {
    setIsPressed(false)
    onPress?.()
  }, [onPress])
  
  return (
    <animated.button
      style={{
        ...pressStyle,
        minWidth: `${minSize}px`,
        minHeight: `${minSize}px`,
        touchAction: 'manipulation', // Prevent zoom
      }}
      onTouchStart={handlePressStart}
      onTouchEnd={handlePressEnd}
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
    >
      {children}
    </animated.button>
  )
}
```

---

## Phase 8: Blackjack Game (Priority 8 - Low)

### Overview
Complete single-player blackjack game implementation with mobile-optimized UI.

### Files to Create
- `src/pages/casino/BlackjackPage.tsx`
- `src/components/casino/blackjack/BlackjackGame.tsx`
- `src/components/casino/blackjack/Card.tsx`
- `src/components/casino/blackjack/Hand.tsx`
- `src/components/casino/blackjack/DealerArea.tsx`
- `src/components/casino/blackjack/PlayerArea.tsx`
- `src/components/casino/blackjack/ActionButtons.tsx`
- `src/services/casino/BlackjackLogic.ts`
- `src/services/casino/CardDeckService.ts`
- `src/hooks/casino/useBlackjack.ts`
- `src/types/casino/blackjack.types.ts`
- `src/constants/casino/blackjack-rules.constants.ts`
- `src/utils/casino/card-game.utils.ts`

### Files to Modify
- `src/pages/index.ts` (add BlackjackPage export)
- `src/App.tsx` (add blackjack routing)
- `src/types/casino/index.ts` (add blackjack types)

### Integration Points
- `src/stores/casinoStore.ts` (from Phase 6)
- `src/hooks/casino/useCasinoAudio.ts` (from Phase 4)
- `src/hooks/casino/useCasinoBalance.ts` (from Phase 6)

### Key Deliverables
1. **Simplified Blackjack**: Basic hit/stand/double rules, single deck, dealer stands soft 17, 3:2 blackjack payout
2. **Touch Card System**: Swipe up=hit, swipe down=stand, tap=select, 80x120px minimum card size
3. **Dealer AI**: Simple deterministic rules with 1-2s "thinking" delay, shuffle at 75% deck penetration
4. **Mobile Interface**: Bottom action bar with 60x60px buttons, card fan layout with 15° rotation
5. **Visual Design**: High contrast card indices, oversized numbers, vertical stack for portrait mode

### Research-Based Implementation Details

**components/casino/blackjack/BlackjackGame.tsx**:
```typescript
// Research: Simplified mobile blackjack
const BlackjackGame: React.FC = () => {
  const { balance, handleBet, addWinnings } = useCasinoBalance()
  const { 
    playerHand, 
    dealerHand, 
    gameState, 
    playerTotal, 
    dealerTotal,
    hit,
    stand,
    doubleDown,
    newGame
  } = useBlackjack()
  
  // Research: Touch gestures for card actions
  const swipeHandlers = useSwipeable({
    onSwipedUp: () => gameState === 'player-turn' && hit(),
    onSwipedDown: () => gameState === 'player-turn' && stand(),
    preventDefaultTouchmoveEvent: true,
    trackMouse: true
  })
  
  return (
    <div className="blackjack-game" {...swipeHandlers}>
      {/* Dealer area with hidden card initially */}
      <DealerArea 
        cards={dealerHand}
        total={dealerTotal}
        hideFirstCard={gameState !== 'game-over'}
        isDealing={gameState === 'dealer-turn'}
      />
      
      {/* Player area with card fan layout */}
      <PlayerArea 
        cards={playerHand}
        total={playerTotal}
        maxTotal={21}
        cardSpacing={15} // 15° rotation from research
      />
      
      {/* Research: Bottom action bar for mobile */}
      <div className="action-bar" style={{
        position: 'fixed',
        bottom: 'env(safe-area-inset-bottom)',
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        gap: '12px',
        padding: '16px'
      }}>
        <TouchButton
          size="large" // 60x60px from research
          variant="success"
          disabled={gameState !== 'player-turn'}
          onPress={hit}
          hapticFeedback="spin"
          aria-label="Hit - Take another card"
        >
          <Plus className="w-6 h-6" />
          <span className="text-sm">HIT</span>
        </TouchButton>
        
        <TouchButton
          size="large"
          variant="danger"
          disabled={gameState !== 'player-turn'}
          onPress={stand}
          hapticFeedback="spin"
          aria-label="Stand - Keep current hand"
        >
          <Hand className="w-6 h-6" />
          <span className="text-sm">STAND</span>
        </TouchButton>
        
        <TouchButton
          size="large"
          variant="secondary"
          disabled={gameState !== 'player-turn' || playerHand.length !== 2}
          onPress={doubleDown}
          hapticFeedback="spin"
          aria-label="Double - Double bet and take one card"
        >
          <ArrowUp className="w-6 h-6" />
          <span className="text-sm">DOUBLE</span>
        </TouchButton>
      </div>
      
      {/* Game status overlay */}
      {gameState === 'game-over' && (
        <GameResultOverlay 
          result={determineWinner(playerTotal, dealerTotal)}
          playerTotal={playerTotal}
          dealerTotal={dealerTotal}
          onNewGame={newGame}
        />
      )}
    </div>
  )
}
```

**components/casino/blackjack/Card.tsx**:
```typescript
// Research: Mobile-optimized card display
const Card: React.FC<CardProps> = ({ 
  suit, 
  rank, 
  isHidden = false, 
  size = 'normal',
  rotation = 0 
}) => {
  const cardSizes = {
    small: { width: 60, height: 90 },
    normal: { width: 80, height: 120 }, // Research: 80x120px minimum
    large: { width: 100, height: 150 }
  }
  
  const { width, height } = cardSizes[size]
  
  return (
    <div 
      className="playing-card"
      style={{
        width: `${width}px`,
        height: `${height}px`,
        transform: `rotate(${rotation}deg)`,
        // Research: High contrast design for mobile
        backgroundColor: isHidden ? '#1f2937' : '#ffffff',
        border: '2px solid #374151',
        borderRadius: '8px',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {!isHidden && (
        <>
          {/* Research: Oversized card indices for readability */}
          <div className="card-index" style={{
            position: 'absolute',
            top: '4px',
            left: '4px',
            fontSize: '18px', // Large for mobile visibility
            fontWeight: 'bold',
            color: ['♦', '♥'].includes(suit) ? '#dc2626' : '#000000',
            lineHeight: 1
          }}>
            {rank}
          </div>
          
          {/* Large suit symbol in center */}
          <div className="card-suit" style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            fontSize: '32px',
            color: ['♦', '♥'].includes(suit) ? '#dc2626' : '#000000'
          }}>
            {suit}
          </div>
        </>
      )}
      
      {/* Card back pattern when hidden */}
      {isHidden && (
        <div className="card-back" style={{
          width: '100%',
          height: '100%',
          background: 'linear-gradient(45deg, #3b82f6 25%, transparent 25%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#ffffff',
          fontSize: '24px'
        }}>
          ♠
        </div>
      )}
    </div>
  )
}
```

**hooks/casino/useBlackjack.ts**:
```typescript
// Research-based blackjack game logic
const useBlackjack = () => {
  const [deck, setDeck] = useState<PlayingCard[]>([])
  const [playerHand, setPlayerHand] = useState<PlayingCard[]>([])
  const [dealerHand, setDealerHand] = useState<PlayingCard[]>([])
  const [gameState, setGameState] = useState<'betting' | 'dealing' | 'player-turn' | 'dealer-turn' | 'game-over'>('betting')
  
  // Research: Simple dealer AI with thinking delay
  const dealerTurn = useCallback(async () => {
    setGameState('dealer-turn')
    let currentDealerHand = [...dealerHand]
    let dealerTotal = calculateHandValue(currentDealerHand)
    
    while (dealerTotal < 17) {
      // Research: 1-2s thinking delay for realism
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const newCard = drawCard(deck)
      currentDealerHand.push(newCard)
      setDealerHand([...currentDealerHand])
      
      dealerTotal = calculateHandValue(currentDealerHand)
      
      // Research: Shuffle at 75% penetration
      if (deck.length < 13) { // 25% of 52 cards remaining
        setDeck(createShuffledDeck())
      }
    }
    
    setGameState('game-over')
  }, [dealerHand, deck])
  
  // Research: Simplified rules - hit/stand/double only
  const hit = useCallback(() => {
    if (gameState !== 'player-turn') return
    
    const newCard = drawCard(deck)
    const newHand = [...playerHand, newCard]
    setPlayerHand(newHand)
    
    const total = calculateHandValue(newHand)
    if (total > 21) {
      setGameState('game-over') // Bust
    }
  }, [playerHand, deck, gameState])
  
  const stand = useCallback(() => {
    if (gameState === 'player-turn') {
      dealerTurn()
    }
  }, [gameState, dealerTurn])
  
  // Research: Double down - double bet and take exactly one card
  const doubleDown = useCallback(() => {
    if (gameState !== 'player-turn' || playerHand.length !== 2) return
    
    const newCard = drawCard(deck)
    const newHand = [...playerHand, newCard]
    setPlayerHand(newHand)
    
    const total = calculateHandValue(newHand)
    if (total <= 21) {
      dealerTurn() // Stand automatically after doubling
    } else {
      setGameState('game-over') // Bust
    }
  }, [playerHand, deck, gameState, dealerTurn])
  
  return {
    playerHand,
    dealerHand,
    gameState,
    playerTotal: calculateHandValue(playerHand),
    dealerTotal: calculateHandValue(dealerHand),
    hit,
    stand,
    doubleDown,
    newGame: initializeGame
  }
}
```

---

## Phase 9: Video Poker Game (Priority 9 - Low)

### Overview
Jacks or Better video poker implementation with strategy hints and mobile-optimized controls.

### Files to Create
- `src/pages/casino/VideoPokerPage.tsx`
- `src/components/casino/poker/VideoPokerGame.tsx`
- `src/components/casino/poker/PokerHand.tsx`
- `src/components/casino/poker/PokerCard.tsx`
- `src/components/casino/poker/HoldControls.tsx`
- `src/components/casino/poker/PayTable.tsx`
- `src/components/casino/poker/StrategyHints.tsx`
- `src/services/casino/VideoPokerLogic.ts`
- `src/services/casino/PokerHandEvaluator.ts`
- `src/hooks/casino/useVideoPoker.ts`
- `src/types/casino/poker.types.ts`
- `src/constants/casino/poker-hands.constants.ts`
- `src/constants/casino/poker-payouts.constants.ts`
- `src/utils/casino/poker-strategy.utils.ts`

### Files to Modify
- `src/pages/index.ts` (add VideoPokerPage export)
- `src/App.tsx` (add video poker routing)
- `src/types/casino/index.ts` (add poker types)

### Integration Points
- `src/services/casino/CardDeckService.ts` (from Phase 8)
- `src/utils/casino/card-game.utils.ts` (from Phase 8)
- `src/stores/casinoStore.ts` (from Phase 6)

### Key Deliverables
1. **Jacks or Better**: Optimal single-player variant with standard payouts (pair=1x, two pair=2x, royal flush=800x)
2. **Hand Evaluation**: Color-coded hand rankings with animated overlays and educational popups
3. **Strategy Hints**: Collapsible hint panel with optimal hold suggestions, beginner auto-play mode
4. **Touch Interface**: Tap to toggle HOLD state, swipe up for quick hold/release, "Hold All"/"Draw All" buttons
5. **Progressive Payouts**: Consecutive win multipliers, achievement system integration

### Research-Based Implementation Details

**components/casino/poker/VideoPokerGame.tsx**:
```typescript
// Research: Jacks or Better optimized for mobile
const VideoPokerGame: React.FC = () => {
  const { balance, handleBet, addWinnings } = useCasinoBalance()
  const {
    hand,
    heldCards,
    gameState,
    currentPayout,
    toggleHold,
    draw,
    newGame,
    getOptimalHolds
  } = useVideoPoker()
  
  const [showHints, setShowHints] = useState(false)
  const optimalHolds = getOptimalHolds()
  
  return (
    <div className="video-poker-game">
      {/* Research: Hand ranking display with color coding */}
      <div className="hand-rankings-header">
        <button 
          className="info-button"
          onClick={() => setShowHandRankings(true)}
          aria-label="View hand rankings"
        >
          <Info className="w-5 h-5" />
          Hand Rankings
        </button>
      </div>
      
      {/* Card display with hold indicators */}
      <div className="poker-hand" style={{
        display: 'flex',
        gap: '8px',
        justifyContent: 'center',
        flexWrap: 'wrap',
        padding: '20px'
      }}>
        {hand.map((card, index) => (
          <div key={index} className="card-container">
            <PokerCard
              {...card}
              isHeld={heldCards[index]}
              onClick={() => toggleHold(index)}
              size="large" // Research: larger cards for mobile
              showHoldIndicator={gameState === 'hold-phase'}
            />
            
            {/* Hold indicator */}
            {heldCards[index] && (
              <div className="hold-indicator" style={{
                position: 'absolute',
                top: '-8px',
                left: '50%',
                transform: 'translateX(-50%)',
                backgroundColor: '#22c55e',
                color: 'white',
                padding: '2px 8px',
                borderRadius: '4px',
                fontSize: '12px',
                fontWeight: 'bold'
              }}>
                HELD
              </div>
            )}
            
            {/* Strategy hint indicator */}
            {showHints && !optimalHolds.includes(index) && (
              <div className="hint-indicator" style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                width: '16px',
                height: '16px',
                backgroundColor: '#ef4444',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <span style={{ fontSize: '10px', color: 'white' }}>!</span>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Research: Collapsible strategy hints */}
      {gameState === 'hold-phase' && (
        <div className="strategy-panel">
          <button 
            className="hint-toggle"
            onClick={() => setShowHints(!showHints)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              margin: '0 auto 16px',
              padding: '8px 16px',
              backgroundColor: showHints ? '#3b82f6' : '#6b7280',
              color: 'white',
              border: 'none',
              borderRadius: '8px'
            }}
          >
            <Lightbulb className="w-4 h-4" />
            {showHints ? 'Hide Hints' : 'Show Strategy Hints'}
          </button>
          
          {showHints && (
            <div className="strategy-advice" style={{
              backgroundColor: '#f3f4f6',
              padding: '12px',
              borderRadius: '8px',
              marginBottom: '16px'
            }}>
              <p className="text-sm text-gray-700">
                {getStrategyAdvice(hand, optimalHolds)}
              </p>
            </div>
          )}
        </div>
      )}
      
      {/* Research: Quick action buttons */}
      <div className="quick-actions" style={{
        display: 'flex',
        gap: '12px',
        justifyContent: 'center',
        marginBottom: '20px'
      }}>
        <TouchButton
          variant="secondary"
          onPress={() => heldCards.forEach((_, index) => 
            !heldCards[index] && toggleHold(index)
          )}
          disabled={gameState !== 'hold-phase'}
        >
          Hold All
        </TouchButton>
        
        <TouchButton
          variant="secondary"
          onPress={() => heldCards.forEach((held, index) => 
            held && toggleHold(index)
          )}
          disabled={gameState !== 'hold-phase'}
        >
          Hold None
        </TouchButton>
      </div>
      
      {/* Main action button */}
      <div className="main-action" style={{ textAlign: 'center' }}>
        {gameState === 'betting' && (
          <TouchButton
            variant="primary"
            size="large"
            onPress={newGame}
            disabled={!balance || balance < 1}
          >
            Deal Cards (1 Coin)
          </TouchButton>
        )}
        
        {gameState === 'hold-phase' && (
          <TouchButton
            variant="primary"
            size="large"
            onPress={draw}
          >
            Draw Cards
          </TouchButton>
        )}
        
        {gameState === 'game-over' && (
          <TouchButton
            variant="primary"
            size="large"
            onPress={newGame}
          >
            {currentPayout > 0 
              ? `Play Again (+${currentPayout} coins!)` 
              : 'Play Again'
            }
          </TouchButton>
        )}
      </div>
    </div>
  )
}
```

**services/casino/PokerHandEvaluator.ts**:
```typescript
// Research: Jacks or Better hand evaluation
const JACKS_OR_BETTER_PAYOUTS = {
  'royal-flush': 800,    // Research: Standard 800x payout
  'straight-flush': 50,
  'four-of-a-kind': 25,
  'full-house': 9,
  'flush': 6,
  'straight': 4,
  'three-of-a-kind': 3,
  'two-pair': 2,
  'jacks-or-better': 1,  // Pair of Jacks, Queens, Kings, or Aces
  'nothing': 0
} as const

class PokerHandEvaluator {
  static evaluateHand(cards: PlayingCard[]): HandResult {
    const handType = this.getHandType(cards)
    const payout = JACKS_OR_BETTER_PAYOUTS[handType]
    
    return {
      handType,
      payout,
      description: this.getHandDescription(handType),
      winningCards: this.getWinningCards(cards, handType)
    }
  }
  
  // Research: Color-coded hand types for UI
  static getHandColor(handType: string): string {
    const colorMap = {
      'royal-flush': '#fbbf24',      // Gold
      'straight-flush': '#a855f7',   // Purple  
      'four-of-a-kind': '#ef4444',   // Red
      'full-house': '#3b82f6',       // Blue
      'flush': '#22c55e',            // Green
      'straight': '#f97316',         // Orange
      'three-of-a-kind': '#8b5cf6',  // Violet
      'two-pair': '#06b6d4',         // Cyan
      'jacks-or-better': '#10b981',  // Emerald
      'nothing': '#6b7280'           // Gray
    }
    return colorMap[handType] || '#6b7280'
  }
}
```

**utils/casino/poker-strategy.utils.ts**:
```typescript
// Research: Optimal video poker strategy
export const VideoPokerStrategy = {
  // Get optimal cards to hold for Jacks or Better
  getOptimalHolds(hand: PlayingCard[]): number[] {
    const analysis = this.analyzeHand(hand)
    
    // Research: Strategy priority order
    if (analysis.hasRoyalFlushDraw) return analysis.royalFlushCards
    if (analysis.hasStraightFlushDraw) return analysis.straightFlushCards
    if (analysis.hasFlushDraw) return analysis.flushCards
    if (analysis.hasStraightDraw) return analysis.straightCards
    if (analysis.hasHighPair) return analysis.highPairCards
    if (analysis.hasLowPair) return analysis.lowPairCards
    if (analysis.hasHighCards) return analysis.highCards
    
    return [] // Hold nothing
  },
  
  // Generate human-readable strategy advice
  getAdvice(hand: PlayingCard[], optimalHolds: number[]): string {
    if (optimalHolds.length === 0) {
      return "No good cards to hold. Draw 5 new cards."
    }
    
    const heldCards = optimalHolds.map(i => hand[i])
    const handType = this.identifyHeldPattern(heldCards)
    
    const adviceMap = {
      'royal-flush-draw': 'Hold for Royal Flush - huge payout potential!',
      'straight-flush-draw': 'Hold for Straight Flush - excellent odds!',
      'flush-draw': 'Hold flush cards - good chance for 6x payout',
      'straight-draw': 'Hold straight cards - 4x payout opportunity',
      'high-pair': 'Hold high pair (Jacks or better) - guaranteed payout',
      'low-pair': 'Hold low pair - might improve to two pair or better',
      'high-cards': 'Hold high cards (J, Q, K, A) - chance for pairs'
    }
    
    return adviceMap[handType] || `Hold ${optimalHolds.length} cards`
  }
}
```

---

## Phase 10: PWA Features (Priority 10 - Low)

### Overview
Progressive Web App features for enhanced mobile experience including offline play and installation.

### Files to Create
- `public/sw.js` (service worker)
- `src/services/casino/PWAService.ts`
- `src/services/casino/CacheService.ts`
- `src/services/casino/OfflineGameService.ts`
- `src/hooks/casino/usePWAFeatures.ts`
- `src/hooks/casino/useOfflineGame.ts`
- `src/components/casino/shared/InstallPrompt.tsx`
- `src/components/casino/shared/OfflineIndicator.tsx`
- `src/utils/casino/cache.utils.ts`

### Files to Modify
- `public/manifest.json` (enhance PWA manifest)
- `src/main.tsx` (register service worker)
- `src/components/casino/shared/index.ts` (add PWA components)

### Integration Points
- Service Worker API
- Cache API
- IndexedDB for offline storage
- All casino games (offline functionality)

### Key Deliverables
1. **Service Worker**: Cache-First for game assets, Network-First for balance updates, 50MB cache limit
2. **Install Experience**: Install prompts after 3+ gaming sessions, fullscreen gaming with custom nav
3. **Offline Gaming**: Cached game assets, offline balance tracking with sync when online
4. **Device Features**: Screen Wake Lock for extended play, orientation lock for landscape games
5. **PWA Manifest**: `"display": "standalone"`, proper theming, 192x192 and 512x512 icons

### Research-Based Implementation Details

**services/casino/PWAService.ts**:
```typescript
// Research: Casino PWA optimization
class PWAService {
  private installPrompt: BeforeInstallPromptEvent | null = null
  private gameSessionCount = 0
  
  async init() {
    // Research: Install prompt after 3+ sessions
    this.gameSessionCount = parseInt(localStorage.getItem('casinoSessions') || '0')
    
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault()
      this.installPrompt = e as BeforeInstallPromptEvent
      
      if (this.gameSessionCount >= 3) {
        this.showInstallPrompt()
      }
    })
    
    // Track game sessions
    this.trackSession()
  }
  
  // Research: Screen Wake Lock for extended gaming
  async keepScreenAwake() {
    if ('wakeLock' in navigator) {
      try {
        const wakeLock = await navigator.wakeLock.request('screen')
        
        // Release on visibility change
        document.addEventListener('visibilitychange', () => {
          if (document.visibilityState === 'visible') {
            navigator.wakeLock.request('screen')
          }
        })
        
        return wakeLock
      } catch (err) {
        console.log('Wake Lock not supported:', err)
      }
    }
  }
  
  // Research: Fullscreen gaming experience
  async enterFullscreen() {
    if (document.documentElement.requestFullscreen) {
      try {
        await document.documentElement.requestFullscreen()
        // Hide browser UI, show custom casino nav
        document.body.classList.add('fullscreen-gaming')
      } catch (err) {
        console.log('Fullscreen not available:', err)
      }
    }
  }
}
```

**sw.js (Service Worker)**:
```javascript
// Research: Casino game caching strategy
const CACHE_NAME = 'casino-v1'
const STATIC_CACHE = 'casino-static-v1'
const DYNAMIC_CACHE = 'casino-dynamic-v1'

// Cache-First for static game assets
const STATIC_ASSETS = [
  '/',
  '/casino',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/audio/spin.mp3',
  '/audio/win.mp3',
  '/audio/coin.mp3',
  '/images/chess-symbols.webp'
]

// Network-First for dynamic data
const NETWORK_FIRST_ROUTES = [
  '/api/balance',
  '/api/transactions',
  '/api/leaderboard'
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(STATIC_ASSETS))
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Research: Cache-First for game assets
  if (STATIC_ASSETS.some(asset => url.pathname.includes(asset))) {
    event.respondWith(
      caches.match(request)
        .then(response => response || fetch(request))
    )
  }
  
  // Research: Network-First for balance/data
  else if (NETWORK_FIRST_ROUTES.some(route => url.pathname.includes(route))) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cache successful responses
          if (response.ok) {
            const responseClone = response.clone()
            caches.open(DYNAMIC_CACHE)
              .then(cache => cache.put(request, responseClone))
          }
          return response
        })
        .catch(() => caches.match(request)) // Fallback to cache
    )
  }
})

// Background sync for offline transactions
self.addEventListener('sync', (event) => {
  if (event.tag === 'casino-transaction') {
    event.waitUntil(
      // Sync offline transactions when online
      syncOfflineTransactions()
    )
  }
})
```

**services/casino/CacheService.ts**:
```typescript
// Research: 50MB cache management
class CacheService {
  private maxCacheSize = 50 * 1024 * 1024 // 50MB from research
  
  async preloadGameAssets() {
    const essentialAssets = [
      // Audio files <50KB each
      '/audio/spin.mp3',
      '/audio/win.mp3', 
      '/audio/lose.mp3',
      '/audio/coin.mp3',
      
      // WebP images for symbols
      '/images/chess-pieces.webp',
      '/images/card-sprites.webp',
      
      // Critical game scripts
      '/js/slot-engine.js',
      '/js/card-logic.js'
    ]
    
    const cache = await caches.open('casino-assets-v1')
    await cache.addAll(essentialAssets)
    
    // Monitor cache size
    await this.manageCacheSize()
  }
  
  async manageCacheSize() {
    const cache = await caches.open('casino-assets-v1')
    const keys = await cache.keys()
    let totalSize = 0
    
    // Calculate total cache size
    for (const key of keys) {
      const response = await cache.match(key)
      if (response) {
        const blob = await response.blob()
        totalSize += blob.size
      }
    }
    
    // Research: Remove oldest entries if over limit
    if (totalSize > this.maxCacheSize) {
      const entriesToRemove = Math.ceil(keys.length * 0.1) // Remove 10%
      for (let i = 0; i < entriesToRemove; i++) {
        await cache.delete(keys[i])
      }
    }
  }
}
```

---

## Implementation Guidelines

### Code Quality Standards
1. **TypeScript**: Strict mode with comprehensive type coverage
2. **Testing**: Minimum 80% code coverage for game logic
3. **Performance**: <16ms React render times, 60fps animations
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Mobile**: Touch target minimum 44px, responsive design

### Architecture Principles
1. **Single Responsibility**: Each component/service has one clear purpose
2. **DRY**: Shared logic in utilities, hooks, and services
3. **Composition**: Favor composition over inheritance
4. **Immutability**: Immutable state updates throughout
5. **Error Boundaries**: Comprehensive error handling and recovery

### Development Workflow
1. **Phase Completion**: Each phase must pass all tests before next phase
2. **Code Reviews**: All casino game logic requires mathematical validation
3. **Device Testing**: Test on minimum 3 different mobile devices per phase
4. **Performance Validation**: Lighthouse CI scoring >90 for performance
5. **Accessibility Audit**: Screen reader testing for all new components

---

*This implementation plan provides a systematic approach to building a comprehensive casino gaming experience while maintaining code quality, performance, and accessibility standards throughout the development process.*