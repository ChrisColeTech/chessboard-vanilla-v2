export interface PageInstructions {
  readonly title: string
  readonly instructions: readonly string[]
}

/**
 * Centralized instructions service for all pages and sub-pages
 * Provides consistent instructions management across the application
 * Supports hierarchical page IDs like 'uitests.audio-demo'
 */
export class InstructionsService {
  private static instance: InstructionsService | null = null
  private instructionsMap: Map<string, PageInstructions> = new Map()

  private constructor() {
    this.initializeInstructions()
  }

  public static getInstance(): InstructionsService {
    if (!InstructionsService.instance) {
      InstructionsService.instance = new InstructionsService()
    }
    return InstructionsService.instance
  }

  private initializeInstructions(): void {
    // Main tab pages
    this.instructionsMap.set('layout', {
      title: 'Background & Theme Testing',
      instructions: [
        'View the animated background effects and floating chess pieces',
        'Test different themes using the settings panel',
        'Observe glassmorphism design and responsive layout',
        'This page demonstrates the visual foundation of the app'
      ]
    })

    this.instructionsMap.set('worker', {
      title: 'Chess Computer Testing Guide',
      instructions: [
        'Test if the chess computer is working and ready to play games',
        'Check how fast the computer can think and respond to moves',
        'Adjust the computer\'s skill level from beginner to expert',
        'Run quick tests to verify the chess engine is functioning properly'
      ]
    })

    this.instructionsMap.set('uitests', {
      title: 'UI Testing Hub Guide',
      instructions: [
        'Navigate to different UI testing environments',
        'Try interactive audio demos and drag testing',
        'Test Global UI Audio Service patterns',
        'Explore educational implementation examples'
      ]
    })

    this.instructionsMap.set('casino', {
      title: 'Chess Casino Games Hub',
      instructions: [
        'Welcome to the chess-themed casino! Choose from our exciting selection of games',
        'Navigate between different casino games using the action menu',
        'All games feature chess piece symbols and themes for a unique experience',
        'Start with slots for the full casino slot machine experience'
      ]
    })

    this.instructionsMap.set('slots', {
      title: 'Chess Slot Machine Experience',
      instructions: [
        'Experience the thrill of a chess-themed casino slot machine',
        'Use the +/- buttons to adjust your coin wager amount',
        'Click the SPIN button to start the slot machine animation',
        'Watch for winning chess piece combinations and enjoy the casino atmosphere'
      ]
    })

    this.instructionsMap.set('blackjack', {
      title: 'Chess Blackjack Coming Soon',
      instructions: [
        'Chess-themed blackjack game with traditional rules',
        'Play against the dealer with chess piece card designs',
        'Try to get as close to 21 without going over',
        'Use the action menu to navigate to other casino games'
      ]
    })

    this.instructionsMap.set('holdem', {
      title: 'Chess Texas Hold\'em Poker',
      instructions: [
        'Chess-themed Texas Hold\'em poker against AI opponents',
        'Features different AI difficulty levels and strategies',
        'Complete betting rounds: preflop, flop, turn, and river',
        'Master poker hand rankings with chess piece themes'
      ]
    })

    this.instructionsMap.set('roulette', {
      title: 'Chess Roulette Wheel',
      instructions: [
        'Chess-themed roulette with realistic physics simulation',
        'Place bets on numbers, colors, and special chess piece sections',
        'Watch the wheel spin with smooth animations',
        'Experience the excitement of European-style roulette'
      ]
    })

    this.instructionsMap.set('craps', {
      title: 'Chess Craps Dice Game',
      instructions: [
        'Chess-themed craps with simplified mobile-friendly rules',
        'Roll the dice with chess piece patterns',
        'Place bets on various dice outcomes and combinations',
        'Enjoy the fast-paced excitement of this classic casino game'
      ]
    })

    this.instructionsMap.set('play', {
      title: 'Chess Play Hub',
      instructions: [
        'Welcome to the Chess Play Hub - Your gateway to chess gameplay',
        'Choose between classical chess games or challenging puzzles',
        'Navigate using the action menu to select your preferred play mode',
        'Each mode offers unique features and learning opportunities'
      ]
    })

    this.instructionsMap.set('playchess', {
      title: 'Classical Chess Games',
      instructions: [
        'Play full chess games on a complete 8x8 board with all 32 pieces',
        'Experience professional drag & drop chess interactions',
        'Features include move history, game controls, and audio feedback',
        'Challenge yourself against the computer or practice openings and endgames',
        'Use action menu for game controls: New Game, Pause, Show Moves, Undo'
      ]
    })

    this.instructionsMap.set('playpuzzles', {
      title: 'Chess Puzzle Training',
      instructions: [
        'Sharpen your tactical skills with our comprehensive puzzle collection',
        'Solve mate-in-1, mate-in-2, tactical combinations, and endgame studies',
        'Learn from famous positions in chess history',
        'Get hints when you\'re stuck or reveal the full solution',
        'Use action menu for puzzle controls: New Puzzle, Hint, Solve Puzzle'
      ]
    })

    // UI Tests sub-pages
    this.instructionsMap.set('uitests.audio-demo', {
      title: 'UI Audio System Demo',
      instructions: [
        'Explore interactive examples of Global UI Audio Service patterns',
        'Test different UI elements with automatic sound detection',
        'Learn about proper audio exclusion patterns',
        'See educational implementation examples in action'
      ]
    })

    this.instructionsMap.set('uitests.drag-test', {
      title: 'Interactive Chess Board Guide',
      instructions: [
        'Test drag and drop functionality with visual feedback and capture mechanics',
        'Drag the bottom-right corner of the dashed container to test responsive scaling',
        'Click on squares to select them and see valid drop targets highlighted',
        'Experience professional chess drag interactions'
      ]
    })

    this.instructionsMap.set('uitests.mobile-drag-test', {
      title: 'Mobile Chess Board Guide',
      instructions: [
        'Test mobile-optimized chess board interactions',
        'Experience touch-friendly drag and drop functionality',
        'See how the board adapts to mobile screen constraints',
        'Test mobile-specific chess interaction patterns'
      ]
    })

    this.instructionsMap.set('mobiledragtest', {
      title: 'Mobile Chess Board Testing',
      instructions: [
        'Test the wrapper-based chess board animation system',
        'Use action sheet to reset the board to initial position',
        'Test move sounds and capture animations',
        'Experience smooth piece animations and shrinking capture effects'
      ]
    })

    // Splash Screen pages
    this.instructionsMap.set('minimalsplash', {
      title: 'Minimal Professional Splash',
      instructions: [
        '🎨 Clean single logo + brand colors with professional typography',
        '👑 Floating chess crown symbol with subtle animation',
        '⏱️ 1.5-2 second duration for quick professional impression',
        '🔄 Restart animation using action sheet controls',
        '🚀 Navigate to other splash screen examples'
      ]
    })

    this.instructionsMap.set('animatedsplash', {
      title: 'Progressive Piece Assembly',
      instructions: [
        '♗ Chess pieces appear in logical hierarchy sequence',
        '🎭 Staggered timing creates engaging assembly animation', 
        '📚 Educational value showing piece placement learning',
        '🔄 Restart animation to see full piece assembly sequence',
        '🎮 Test cross-navigation to other splash variants'
      ]
    })

    this.instructionsMap.set('loadingprogress', {
      title: 'Engine Loading Dashboard',
      instructions: [
        '🔧 Technical precision meets chess sophistication',
        '📊 Real progress feedback for engine initialization sequence',
        '🎯 Professional dashboard styling with readable timing',
        '⚙️ Shows current service being initialized',
        '🔄 Restart to see full loading sequence animation'
      ]
    })

    this.instructionsMap.set('brandedsplash', {
      title: 'Master Chess Training Branding',
      instructions: [
        '🏛️ Full brand identity with institutional excellence feel',
        '🎓 Premium educational institution presentation',
        '👑 Sophisticated typography with authority indicators',
        '✨ No progress bars - pure brand experience focus',
        '🎨 Dignified crown floating with elegant styling'
      ]
    })

    this.instructionsMap.set('functionalsplash', {
      title: 'Functional Asset Preloading',
      instructions: [
        '🎯 **Real Asset Preloading**: Performs actual app initialization, not fake animations',
        '📊 **Live Progress**: Shows real loading stages (store → pieces → audio → background)',
        '🎨 **User-Preference-Driven**: Loads your selected piece set first, others in background',
        '🔊 **Smart Audio Loading**: Only preloads audio if enabled in settings',
        '⚡ **Modern APIs**: Uses 2024 React preload API + custom Promise coordination',
        '🚫 **Error Handling**: Shows retry options and graceful degradation on failures',
        '⏭️ **Skip Option**: Power users can bypass loading for immediate access',
        '📱 **Network Aware**: Adapts to connection speed with timeout handling'
      ]
    })

    // Future sub-pages can be added easily
    // this.instructionsMap.set('uitests.audio-demo.advanced', { ... })
    // this.instructionsMap.set('play.vs-computer.difficulty', { ... })
  }

  /**
   * Get instructions for a specific page or sub-page
   */
  public getInstructions(pageId: string): PageInstructions | null {
    return this.instructionsMap.get(pageId) || null
  }

  /**
   * Get all available page instructions
   */
  public getAllInstructions(): ReadonlyMap<string, PageInstructions> {
    return new Map(this.instructionsMap)
  }

  /**
   * Update instructions for a specific page (for dynamic content)
   */
  public updateInstructions(pageId: string, instructions: PageInstructions): void {
    this.instructionsMap.set(pageId, instructions)
  }

  /**
   * Check if instructions exist for a page
   */
  public hasInstructions(pageId: string): boolean {
    return this.instructionsMap.has(pageId)
  }

  /**
   * Get all sub-page IDs for a parent page
   * e.g. getSubPages('uitests') returns ['uitests.audio-demo', 'uitests.drag-test']
   */
  public getSubPages(parentPageId: string): string[] {
    const prefix = `${parentPageId}.`
    return Array.from(this.instructionsMap.keys())
      .filter(key => key.startsWith(prefix))
      .sort()
  }
}

// Export singleton instance
export const instructionsService = InstructionsService.getInstance()