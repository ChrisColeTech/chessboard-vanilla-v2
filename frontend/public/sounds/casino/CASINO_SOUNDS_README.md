# Casino Sounds Library

This directory contains free casino-themed sound effects for use in the responsive chessboard casino games implementation.

## Sound Sources & Licensing

### Mixkit Sounds (Mixkit License - Free for Commercial Use)
- `slot-machine-wheel.mp3` - Slot machine spinning sound (6 seconds)
- `slot-machine-win.mp3` - Basic win sound (5 seconds) 
- `coins-handling.mp3` - Coin handling/dropping sound (1 second)
- `magical-coin-win.mp3` - Enhanced coin win sound (2 seconds)
- `slot-machine-win-siren.mp3` - Jackpot siren sound (7 seconds)
- `payout-award.mp3` - Payout award sound (4 seconds)
- `arcade-slot-machine-wheel.mp3` - Arcade-style reel sound (3 seconds)
- `bonus-collect-award.mp3` - Bonus collection sound (1 second)

### Kenney Casino Audio Pack (CC0 Public Domain)
**Attribution**: Optional - can credit "Kenney.nl" or "www.kenney.nl"
**License File**: `KENNEY_LICENSE.txt`

#### Card Sounds (23 files)
- `card-fan-1.ogg`, `card-fan-2.ogg` - Card fanning sounds
- `card-place-1.ogg` to `card-place-4.ogg` - Card placement sounds
- `card-shove-1.ogg` to `card-shove-4.ogg` - Card shoving sounds
- `card-shuffle.ogg` - Main card shuffling sound
- `card-slide-1.ogg` to `card-slide-8.ogg` - Card sliding sounds
- `cards-pack-open-1.ogg`, `cards-pack-open-2.ogg` - Opening card pack
- `cards-pack-take-out-1.ogg`, `cards-pack-take-out-2.ogg` - Taking cards from pack

#### Chip Sounds (19 files)
- `chip-lay-1.ogg` to `chip-lay-3.ogg` - Placing chips
- `chips-collide-1.ogg` to `chips-collide-4.ogg` - Chips colliding
- `chips-handle-1.ogg` to `chips-handle-6.ogg` - Handling chips
- `chips-stack-1.ogg` to `chips-stack-6.ogg` - Stacking chips

#### Dice Sounds (12 files)
- `dice-grab-1.ogg`, `dice-grab-2.ogg` - Grabbing dice
- `dice-shake-1.ogg` to `dice-shake-3.ogg` - Shaking dice
- `dice-throw-1.ogg` to `dice-throw-3.ogg` - Throwing multiple dice
- `die-throw-1.ogg` to `die-throw-4.ogg` - Throwing single die

## Casino Game Sound Mapping

### Slot Machine Games
```typescript
// Recommended sound mappings for slot machine implementation
const SLOT_SOUNDS = {
  // Spinning reels
  spin: 'slot-machine-wheel.mp3',
  spinAlt: 'arcade-slot-machine-wheel.mp3',
  
  // Wins and payouts
  smallWin: 'slot-machine-win.mp3',
  mediumWin: 'payout-award.mp3', 
  bigWin: 'magical-coin-win.mp3',
  jackpot: 'slot-machine-win-siren.mp3',
  
  // Coin interactions
  coinDrop: 'coins-handling.mp3',
  bonus: 'bonus-collect-award.mp3'
}
```

### Blackjack Games
```typescript
// Recommended sound mappings for blackjack implementation
const BLACKJACK_SOUNDS = {
  // Card actions
  shuffle: 'card-shuffle.ogg',
  dealCard: 'card-slide-1.ogg', // Rotate through card-slide-1 to 8
  placeCard: 'card-place-1.ogg', // Rotate through card-place-1 to 4
  fanCards: 'card-fan-1.ogg',
  
  // Chip actions  
  placeBet: 'chip-lay-1.ogg', // Rotate through chip-lay-1 to 3
  collectChips: 'chips-handle-1.ogg',
  stackChips: 'chips-stack-1.ogg',
  
  // Wins
  win: 'magical-coin-win.mp3',
  blackjack: 'payout-award.mp3'
}
```

### Video Poker Games
```typescript
// Recommended sound mappings for video poker implementation  
const POKER_SOUNDS = {
  // Card actions
  shuffle: 'card-shuffle.ogg',
  deal: 'card-shove-1.ogg', // Rotate through card-shove-1 to 4
  hold: 'card-place-1.ogg',
  draw: 'card-slide-1.ogg',
  
  // Wins by hand strength
  pair: 'slot-machine-win.mp3',
  twoPair: 'payout-award.mp3',
  threeOfAKind: 'magical-coin-win.mp3',
  straight: 'magical-coin-win.mp3',
  flush: 'payout-award.mp3',
  fullHouse: 'magical-coin-win.mp3',
  fourOfAKind: 'slot-machine-win-siren.mp3',
  straightFlush: 'slot-machine-win-siren.mp3',
  royalFlush: 'slot-machine-win-siren.mp3'
}
```

## Implementation Guidelines

### Audio Service Integration
These sounds are designed to integrate with the existing audio service architecture:

```typescript
// Example usage with existing audio service
import { audioService } from '@/services/audio/audioService'

// Play casino sound
audioService.playSound('casino/slot-machine-win.mp3')

// Play with volume control
audioService.playSound('casino/card-shuffle.ogg', { volume: 0.7 })
```

### Performance Considerations
Based on research findings:
- Preload essential sounds only (spin, win, shuffle)
- Use audio pooling for frequently played sounds
- Limit concurrent sounds to maximum 3
- Pause audio when page is not visible
- Provide silent mode detection and visual alternatives

### Mobile Optimization
- All sounds are compressed for mobile data efficiency
- MP3 files from Mixkit are already optimized for web delivery  
- OGG files from Kenney provide excellent compression
- Battery optimization: limit audio duration and frequency

### Accessibility
- Provide visual indicators for all audio cues
- Respect user's reduced motion and silent mode preferences
- Ensure audio never blocks game functionality
- Offer audio toggle controls

## File Format Notes
- **MP3**: Broad browser compatibility, good for slot machine sounds
- **OGG**: Excellent compression, perfect for card/chip sounds
- **Size**: Total library ~1.4MB, individual files range from 5KB to 228KB

## Usage Examples

### Basic Slot Machine
```typescript
// Spin starts
audioService.playSound('casino/slot-machine-wheel.mp3')

// Small win
audioService.playSound('casino/slot-machine-win.mp3') 

// Jackpot win with haptic
audioService.playSound('casino/slot-machine-win-siren.mp3')
navigator.vibrate([100, 50, 100, 50, 200])
```

### Blackjack Card Actions
```typescript
// Shuffle at game start
audioService.playSound('casino/card-shuffle.ogg')

// Deal cards with stagger
dealCards.forEach((card, index) => {
  setTimeout(() => {
    const slideSound = `casino/card-slide-${(index % 8) + 1}.ogg`
    audioService.playSound(slideSound)
  }, index * 200)
})
```

### Chip Betting
```typescript
// Place bet
audioService.playSound('casino/chip-lay-1.ogg')

// Collect winnings
audioService.playSound('casino/chips-handle-3.ogg')
```

This comprehensive sound library provides everything needed for authentic casino gaming experiences while maintaining performance and accessibility standards.