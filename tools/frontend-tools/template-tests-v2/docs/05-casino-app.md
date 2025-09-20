# 05 - Casino Gaming App MVP

## Implementation Plan

### Phase 1: Base Application Setup
This app uses the shared base React Vite application with all required dependencies:

1. **Base App Foundation** from `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite + TypeScript
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **Casino App Setup** - Copy base app structure (excluding src) to create casino-app directory

3. **Page Generation** - Use template-based generator to create complete casino gaming structure

### Phase 2: Casino App Generation
Use the template-based generator to create the complete casino gaming app structure on top of the base app foundation.

## App Vision
A comprehensive casino gaming platform featuring classic casino games with realistic animations and social features. Think "Las Vegas meets mobile gaming" with slot machines, card games, and live dealer experiences in a safe, demo environment.

## What Makes This Special
- **Realistic Game Physics** - Authentic casino game mechanics and animations
- **Social Gaming** - Multiplayer tables and chat features
- **Progressive Systems** - Leveling, achievements, and daily bonuses
- **Live Atmosphere** - Sound effects, music, and immersive casino ambiance

## Parent Pages & Children

### 1. **Slots** Parent
**Purpose**: Slot machine games and jackpot features

#### **Classic** Child Page
- **Slot Machine Types**:
  - 3-reel traditional slots with classic symbols
  - 5-reel video slots with bonus rounds
  - Progressive jackpot slots with accumulating prizes
  - Fruit machines with nudge and hold features
- **Game Features**:
  - Animated reel spinning with realistic physics
  - Auto-spin functionality with customizable settings
  - Max bet and quick spin options
  - Payline highlighting and win celebrations
- **Classic Slot Themes**:
  - Fruit machines (cherries, lemons, bars, 7s)
  - Diamond and gem slots
  - Lucky number 7 variations
  - Bell and BAR classic combinations
- **Bonus Features**:
  - Wild symbols and scatter pays
  - Free spin bonus rounds
  - Double-or-nothing gamble feature
  - Progressive jackpot contributions
- **Sound and Atmosphere**:
  - Authentic slot machine sounds
  - Coin dropping effects
  - Celebratory win music
  - Ambient casino background sounds

#### **Video** Child Page
- **Modern Video Slots**:
  - 5-reel, 25+ payline video slots
  - Cascading reels and expanding wilds
  - Multi-level bonus games
  - Interactive storyline slots
- **Themed Video Slots**:
  - Adventure themes (treasure hunting, exploration)
  - Fantasy themes (dragons, magic, mythology)
  - Movie and TV show themed slots
  - Seasonal and holiday special slots
- **Advanced Features**:
  - Pick-me bonus games with hidden prizes
  - Wheel of fortune style bonus rounds
  - Mini-games within slot sessions
  - Achievement-based unlockable content
- **Visual Effects**:
  - High-quality graphics and animations
  - 3D reel effects and transitions
  - Particle effects for big wins
  - Interactive background animations
- **Progressive Features**:
  - Slot tournaments with leaderboards
  - Daily slot challenges and missions
  - VIP levels with exclusive slot access
  - Social sharing of big wins

### 2. **Cards** Parent
**Purpose**: Card-based casino games

#### **Blackjack** Child Page
- **Game Variations**:
  - Classic Vegas Blackjack (3:2 payouts)
  - European Blackjack (no hole card)
  - Multi-hand Blackjack (up to 5 hands)
  - Blackjack Switch with hand swapping
- **Game Features**:
  - Realistic card dealing animations
  - Hand value calculations and soft/hard totals
  - Insurance and even money options
  - Side bets (21+3, Perfect Pairs)
- **Playing Interface**:
  - Touch-friendly hit, stand, double, split buttons
  - Card counting practice mode (educational)
  - Basic strategy hints and tips
  - Game statistics and win/loss tracking
- **Multiplayer Tables**:
  - Seat selection at virtual tables
  - Chat with other players
  - Dealer personality and interactions
  - Tournament play with elimination rounds
- **Strategy Tools**:
  - Basic strategy chart reference
  - Hand history and pattern analysis
  - Bankroll management suggestions
  - Practice mode with unlimited chips

#### **Poker** Child Page
- **Poker Variations**:
  - Texas Hold'em tournaments and cash games
  - Five Card Draw with ante betting
  - Caribbean Stud Poker against dealer
  - Video Poker with Jacks or Better
- **Tournament Features**:
  - Sit & Go tournaments (6-player tables)
  - Multi-table tournaments with prize pools
  - Heads-up poker challenges
  - Freeroll tournaments with no buy-in
- **Cash Game Tables**:
  - Ring game tables with different stakes
  - Fast-fold poker for quick action
  - Short-handed tables (3-6 players)
  - Private tables for friends
- **Poker Tools**:
  - Hand strength indicators
  - Pot odds calculations
  - Player statistics and notes
  - Hand replay and analysis
- **Social Features**:
  - Player avatars and customization
  - Emote reactions and chat
  - Friend challenges and private games
  - Achievement badges and rankings

### 3. **Table** Parent
**Purpose**: Traditional table games with live dealer feel

#### **Roulette** Child Page
- **Roulette Variations**:
  - European Roulette (single zero)
  - American Roulette (double zero)
  - French Roulette with La Partage rule
  - Speed Roulette for faster gameplay
- **Betting Interface**:
  - Visual betting board with chip placement
  - Inside bets (straight, split, street, corner)
  - Outside bets (red/black, odd/even, columns)
  - Neighbor bets and call bets
- **Game Features**:
  - Realistic wheel spinning physics
  - Ball trajectory animations
  - Winning number celebrations
  - Betting history and hot/cold numbers
- **Advanced Betting**:
  - Favorite bet combinations saving
  - Quick bet buttons for common wagers
  - Progressive betting strategies
  - Statistics tracking for number patterns
- **Live Atmosphere**:
  - Professional dealer voice-overs
  - Authentic casino table sounds
  - Multiple camera angles simulation
  - Real-time betting countdown timers

#### **Dice** Child Page
- **Craps Game**:
  - Come-out roll and point establishment
  - Pass line and don't pass betting
  - Odds bets with true odds payouts
  - Proposition bets and hardways
- **Dice Games Collection**:
  - Sic Bo with triple dice betting
  - Chuck-a-Luck carnival dice game
  - Hazard (historical English dice game)
  - Custom dice games and variations
- **Game Interface**:
  - 3D dice rolling with physics simulation
  - Interactive betting layout
  - Multi-roll bet tracking
  - Payout calculations and odds display
- **Social Craps**:
  - Virtual craps table with multiple players
  - Shooter rotation and dice passing
  - Collective cheering for hot shooters
  - Side betting on other players' rolls
- **Educational Mode**:
  - Craps rules tutorial with interactive examples
  - Betting strategy guides
  - Odds explanation and house edge info
  - Practice mode with play money

### 4. **Live** Parent
**Purpose**: Live dealer simulation and social casino features

#### **Dealers** Child Page
- **Virtual Dealers**:
  - Professional dealer personalities with unique styles
  - Interactive dealer chat and responses
  - Dealer biography and specialization info
  - Favorite dealer selection and following
- **Live Table Experience**:
  - High-definition dealer animations
  - Real-time game commentary
  - Multiple table selection and switching
  - VIP tables with exclusive dealers
- **Dealer Interactions**:
  - Customizable dealer greetings
  - Congratulations on wins and condolences on losses
  - Educational tips and game strategy advice
  - Personal dealer preferences and memory
- **Live Features**:
  - Scheduled dealer shifts and rotations
  - Special event dealers for holidays
  - Dealer tournaments and competitions
  - Behind-the-scenes dealer training content
- **Social Elements**:
  - Dealer fan clubs and following systems
  - Tip the dealer with virtual currency
  - Dealer performance ratings and reviews
  - Community feedback on dealer interactions

#### **Tournaments** Child Page
- **Tournament Types**:
  - Daily slot tournaments with leaderboards
  - Weekly poker championship series
  - Monthly blackjack elimination tournaments
  - Seasonal casino game grand championships
- **Competition Features**:
  - Buy-in tournaments with prize pools
  - Freeroll tournaments for all players
  - Satellite tournaments for major events
  - Heads-up tournaments and brackets
- **Tournament Structure**:
  - Blind level increases and time limits
  - Chip stack management and all-ins
  - Final table streaming and spectating
  - Prize distribution and payout schedules
- **Social Competition**:
  - Team tournaments and guild competitions
  - Achievement-based tournament entry
  - Spectator mode with live commentary
  - Tournament chat and community discussions
- **Leaderboards**:
  - Global rankings across all games
  - Weekly and monthly leaderboard resets
  - Regional and country-specific rankings
  - Hall of fame for tournament champions

### 5. **Account** Parent
**Purpose**: Player account management and casino rewards

#### **Wallet** Child Page
- **Chip Management**:
  - Virtual chip balance and denominations
  - Daily bonus chip collection
  - Hourly chip refills and bonuses
  - Achievement-based chip rewards
- **Transaction History**:
  - Detailed game session records
  - Win/loss tracking by game type
  - Bonus collection history
  - VIP point accumulation tracking
- **Rewards System**:
  - Loyalty points for every game played
  - VIP tier progression and benefits
  - Comp points convertible to chips
  - Exclusive high-roller privileges
- **Banking Interface**:
  - Secure chip purchase simulation (demo only)
  - Gift chip sending to friends
  - Jackpot win claiming process
  - Withdrawal request simulation
- **Budget Tools**:
  - Session loss limits and alerts
  - Time-based playing restrictions
  - Reality check notifications
  - Responsible gaming resources

#### **Stats** Child Page
- **Gaming Statistics**:
  - Total games played across all categories
  - Win/loss ratios by game type
  - Biggest wins and largest payouts
  - Longest winning and losing streaks
- **Performance Analytics**:
  - Return to player (RTP) by game
  - Average session length and frequency
  - Favorite games and playing patterns
  - Skill progression in strategy games
- **Achievement Tracking**:
  - Casino milestone badges and trophies
  - Game-specific achievements unlocked
  - Social achievements and friend challenges
  - Rare and legendary achievement pursuit
- **Progress Visualization**:
  - Interactive charts and graphs
  - Monthly and yearly playing summaries
  - Goal setting and progress tracking
  - Comparison with friends and community
- **Historical Data**:
  - Complete gaming history archive
  - Memorable session replays
  - Big win celebrations and recordings
  - Personal gambling journey timeline

## Theme & Layout System

### Copper Theme
This app uses the **Copper** theme from the professional themes collection, providing a warm, luxurious casino aesthetic with rich metallic tones that evoke premium gaming environments.

**Theme Variables (Copper):**
```css
/* Copper Theme Variables */
--primary: #ea580c;           /* Orange copper primary */
--accent: #ea580c;            /* Orange copper accent */
--background: #0f172a;        /* Slate dark background */
--surface: #1e293b;           /* Slate surface */
--surface-variant: #334155;   /* Slate surface variant */
--on-surface: #f1f5f9;        /* Slate light text */
--on-surface-variant: #cbd5e1; /* Slate medium text */
--outline: #475569;           /* Slate outline */
```

### App Layout & Navigation
The app uses `AppLayout.tsx` with TabBar navigation:

**Tab Configuration:**
- **Slots** - Slot machine icon (Classic, Video)
- **Cards** - Playing card icon (Blackjack, Poker)
- **Table** - Roulette icon (Roulette, Dice)
- **Live** - Video camera icon (Dealers, Tournaments)
- **Account** - User icon (Wallet, Stats)

### Layout Templates

#### Desktop Pages (ChessboardLayout)
5-panel design optimized for casino gaming:
```jsx
<ChessboardLayout
  topLeft={<div className="casino-controls">Game Controls</div>}
  top={<div className="casino-info">Game Info/Rules</div>}
  topRight={<div className="casino-balance">Balance/Bets</div>}
  left={<div className="casino-games">Game Selection</div>}
  center={<div className="casino-main">Game Interface</div>}
  right={<div className="casino-stats">Stats/Leaderboards</div>}
  bottomLeft={<div className="casino-social">Chat/Social</div>}
  bottom={<div className="casino-status">Game Status</div>}
  bottomRight={<div className="casino-actions">Quick Actions</div>}
/>
```

#### Mobile Pages (MobileChessboardLayout)
3-panel design optimized for mobile gaming:
```jsx
<MobileChessboardLayout
  topPieces={<div className="casino-mobile-header">Balance/Controls</div>}
  center={<div className="casino-mobile-game">Game Interface</div>}
  bottomPieces={<div className="casino-mobile-actions">Betting/Actions</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `casino-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables
- **NO hardcoded colors** - only theme-aware classes
- **Templates are NEVER modified** - only the generated app's CSS

Add these NEW classes to the generated `casino-app/src/index.css`:

```css
/* Casino App Component Classes */
.casino-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg overflow-hidden;
  @apply hover:bg-surface-variant/60 hover:border-primary/30 hover:shadow-lg transition-all duration-300;
  @apply group cursor-pointer;
}

.casino-slot-machine {
  @apply bg-gradient-to-b from-surface/90 to-surface-variant/90;
  @apply border border-primary/30 rounded-xl p-6;
  @apply shadow-lg backdrop-blur-md;
}

.casino-reel {
  @apply bg-surface/60 border border-outline/30 rounded-lg overflow-hidden;
  @apply flex flex-col items-center justify-center;
  @apply min-h-24 font-bold text-2xl;
}

.casino-spin-button {
  @apply bg-gradient-to-r from-primary to-accent;
  @apply text-white font-bold py-3 px-8 rounded-full;
  @apply hover:from-primary/80 hover:to-accent/80;
  @apply active:scale-95 transition-all duration-200;
  @apply shadow-lg hover:shadow-xl;
}

.casino-chip {
  @apply w-8 h-8 rounded-full border-2 border-primary/60;
  @apply bg-gradient-to-br from-primary/20 to-accent/20;
  @apply flex items-center justify-center text-xs font-bold;
  @apply cursor-pointer hover:scale-110 transition-transform;
}

.casino-card-deck {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply aspect-[2/3] flex items-center justify-center;
  @apply text-4xl select-none;
}

.casino-betting-area {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply grid grid-cols-3 gap-2;
}

.casino-bet-spot {
  @apply aspect-square rounded-lg border border-outline/30;
  @apply bg-surface-variant/40 hover:bg-primary/20;
  @apply flex items-center justify-center cursor-pointer;
  @apply transition-colors duration-200;
}

.casino-jackpot-display {
  @apply bg-gradient-to-r from-primary/20 to-accent/20;
  @apply border border-primary/40 rounded-xl p-6 text-center;
  @apply backdrop-blur-sm;
}

.casino-leaderboard {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply space-y-2;
}

.casino-dealer-card {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply hover:bg-surface-variant/40 transition-colors cursor-pointer;
  @apply text-center space-y-2;
}

.casino-tournament-card {
  @apply bg-gradient-to-br from-primary/10 to-accent/10;
  @apply border border-primary/30 rounded-xl p-6;
  @apply hover:from-primary/20 hover:to-accent/20 transition-all duration-300;
  @apply cursor-pointer;
}

.casino-balance-display {
  @apply bg-primary/20 text-primary px-4 py-2 rounded-full;
  @apply border border-primary/30 font-bold text-lg;
}
```

### ASCII Mockups

#### Desktop Layout (ChessboardLayout)
```
┌─────────────────────────────────────────────────────────────────┐
│                     Casino Gaming App                          │
├─────────┬─────────────────────────┬─────────────────────────────┤
│  Game   │    Game Info/Rules     │     Balance/Bets            │
│Controls │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│         │      🎠 🃏 ♠️ 🎲      │                             │
│  Game   │      ┌───────┐      │   Stats/Leaderboards        │
│Selection│      │ 7 7 7 │      │                             │
│         │      └───────┘      │                             │
│         │       [SPIN]        │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│ Chat/   │     Game Status        │     Quick Actions           │
│ Social  │                         │                             │
├─────────┴─────────────────────────┴─────────────────────────────┤
│                          TabBar                                 │
│     Slots    Cards    Table    Live    Account                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (MobileChessboardLayout)
```
┌─────────────────────────────────┐
│        Casino Gaming App       │
├─────────────────────────────────┤
│      Balance/Controls           │
│                                 │
├─────────────────────────────────┤
│           🎠 🃏 ♠️           │
│         ┌───────┐         │
│         │ 7 7 7 │         │
│         └───────┘         │
│          [SPIN]           │
├─────────────────────────────────┤
│      Betting/Actions            │
│                                 │
├─────────────────────────────────┤
│             TabBar              │
│ Slots Cards Table Live Account  │
└─────────────────────────────────┘
```

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile Classic Slots Page**
- **Portrait Mode**: Optimized slot reels for vertical mobile screens
- **Touch Spin**: Large, finger-friendly spin button
- **Swipe Games**: Horizontal swipe between different slot machines
- **Quick Bets**: One-tap betting with preset amounts
- **Mobile Sounds**: Optimized audio for mobile speakers/headphones

#### **Mobile Video Slots Page**
- **Full-Screen Play**: Immersive full-screen slot experience
- **Gesture Controls**: Pinch to zoom on bonus games
- **Touch Bonus**: Interactive touch-based bonus rounds
- **Mobile Graphics**: Optimized animations for mobile performance
- **Quick Access**: Easy access to auto-spin and game settings

#### **Mobile Blackjack Page**
- **Vertical Layout**: Cards optimized for mobile screen orientation
- **Touch Actions**: Large hit, stand, double, split buttons
- **Swipe Cards**: Gesture-based card reveals
- **Mobile Tables**: Touch-friendly table selection
- **Quick Play**: Simplified interface for faster mobile play

#### **Mobile Poker Page**
- **Compact Table**: Mobile-optimized poker table layout
- **Touch Betting**: Easy chip betting with touch controls
- **Mobile Chat**: Mobile keyboard optimized chat interface
- **Hand Gestures**: Swipe to fold, tap to call/raise
- **Portrait Cards**: Vertical card arrangement for mobile

#### **Mobile Roulette Page**
- **Touch Betting**: Direct touch betting on roulette layout
- **Mobile Wheel**: Optimized roulette wheel for mobile screens
- **Gesture Chips**: Drag and drop chip placement
- **Quick Bets**: One-tap favorite bet combinations
- **Mobile Spin**: Large, prominent spin button

#### **Mobile Dice Page**
- **Shake to Roll**: Motion sensor dice rolling
- **Touch Betting**: Easy craps betting layout for mobile
- **Mobile Physics**: Optimized dice physics for mobile performance
- **Gesture Controls**: Swipe and tap betting interface
- **Quick Games**: Simplified dice games for mobile play

#### **Mobile Dealers Page**
- **Portrait Video**: Mobile-optimized dealer video streams
- **Touch Chat**: Easy dealer interaction via touch
- **Swipe Tables**: Horizontal swipe between live tables
- **Mobile UI**: Simplified live dealer interface
- **Quick Join**: One-tap table joining

#### **Mobile Tournaments Page**
- **Tournament List**: Mobile-optimized tournament browsing
- **Touch Entry**: Easy tournament registration
- **Mobile Leaderboards**: Touch-friendly ranking displays
- **Live Updates**: Push notifications for tournament updates
- **Quick Info**: Tap for tournament details

#### **Mobile Wallet Page**
- **Balance Display**: Prominent chip balance on mobile
- **Touch Transactions**: Easy transaction history browsing
- **Mobile Bonuses**: One-tap bonus collection
- **Quick Buy**: Simplified chip purchase interface
- **Gesture Navigation**: Swipe through wallet sections

#### **Mobile Stats Page**
- **Scrollable Charts**: Mobile-friendly statistics display
- **Touch Details**: Tap to expand statistical information
- **Swipe Categories**: Horizontal navigation between stat types
- **Mobile Achievements**: Touch-friendly achievement gallery
- **Quick Sharing**: Easy stats sharing on mobile

## Implementation Commands

### Phase 1: Setup Casino App Directory

```bash
# Copy base app structure (excluding src folder) to casino-app
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2
mkdir -p casino-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} casino-app/

# Navigate to casino app directory and install dependencies
cd casino-app
npm install
cd ..
```

### Phase 2: Generate Casino App Pages

```bash
# Navigate to generator directory
cd casino-app

# Create parent pages
npm run mobile -- parent Slots
npm run mobile -- parent Cards
npm run mobile -- parent Table
npm run mobile -- parent Live
npm run mobile -- parent Account

# Create child pages with mobile variants under Slots parent
npm run mobile -- child Classic --parent slots npm run mobile -- child Video --parent slots 
# Create child pages with mobile variants under Cards parent
npm run mobile -- child Blackjack --parent cards npm run mobile -- child Poker --parent cards 
# Create child pages with mobile variants under Table parent
npm run mobile -- child Roulette --parent table npm run mobile -- child Dice --parent table 
# Create child pages with mobile variants under Live parent
npm run mobile -- child Dealers --parent live npm run mobile -- child Tournaments --parent live 
# Create child pages with mobile variants under Account parent
npm run mobile -- child Wallet --parent account npm run mobile -- child Stats --parent account ```

## File Structure Tree

```
casino-app/
├── src/
│   ├── components/
│   │   ├── slots/
│   │   │   ├── ClassicPageWrapper.tsx
│   │   │   ├── VideoPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── cards/
│   │   │   ├── BlackjackPageWrapper.tsx
│   │   │   ├── PokerPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── table/
│   │   │   ├── RoulettePageWrapper.tsx
│   │   │   ├── DicePageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── live/
│   │   │   ├── DealersPageWrapper.tsx
│   │   │   ├── TournamentsPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── account/
│   │       ├── WalletPageWrapper.tsx
│   │       ├── StatsPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── slots/
│   │   │   ├── SlotsPage.tsx
│   │   │   ├── SlotsMainPage.tsx
│   │   │   ├── ClassicPage.tsx
│   │   │   ├── MobileClassicPage.tsx
│   │   │   ├── VideoPage.tsx
│   │   │   └── MobileVideoPage.tsx
│   │   ├── cards/
│   │   │   ├── CardsPage.tsx
│   │   │   ├── CardsMainPage.tsx
│   │   │   ├── BlackjackPage.tsx
│   │   │   ├── MobileBlackjackPage.tsx
│   │   │   ├── PokerPage.tsx
│   │   │   └── MobilePokerPage.tsx
│   │   ├── table/
│   │   │   ├── TablePage.tsx
│   │   │   ├── TableMainPage.tsx
│   │   │   ├── RoulettePage.tsx
│   │   │   ├── MobileRoulettePage.tsx
│   │   │   ├── DicePage.tsx
│   │   │   └── MobileDicePage.tsx
│   │   ├── live/
│   │   │   ├── LivePage.tsx
│   │   │   ├── LiveMainPage.tsx
│   │   │   ├── DealersPage.tsx
│   │   │   ├── MobileDealersPage.tsx
│   │   │   ├── TournamentsPage.tsx
│   │   │   └── MobileTournamentsPage.tsx
│   │   └── account/
│   │       ├── AccountPage.tsx
│   │       ├── AccountMainPage.tsx
│   │       ├── WalletPage.tsx
│   │       ├── MobileWalletPage.tsx
│   │       ├── StatsPage.tsx
│   │       └── MobileStatsPage.tsx
│   ├── hooks/
│   │   ├── slots/
│   │   │   └── useSlotsActions.ts
│   │   ├── cards/
│   │   │   └── useCardsActions.ts
│   │   ├── table/
│   │   │   └── useTableActions.ts
│   │   ├── live/
│   │   │   └── useLiveActions.ts
│   │   └── account/
│   │       └── useAccountActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── gamesApi.ts
│   │   │   ├── slotsApi.ts
│   │   │   ├── cardsApi.ts
│   │   │   ├── tableApi.ts
│   │   │   ├── tournamentsApi.ts
│   │   │   └── walletApi.ts
│   │   ├── games/
│   │   │   ├── slotEngine.ts
│   │   │   ├── blackjackEngine.ts
│   │   │   ├── pokerEngine.ts
│   │   │   ├── rouletteEngine.ts
│   │   │   └── diceEngine.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── slots.ts
│   │           ├── cards.ts
│   │           ├── table.ts
│   │           ├── live.ts
│   │           └── account.ts
│   ├── constants/
│   │   ├── games/
│   │   │   ├── slots.ts
│   │   │   ├── cards.ts
│   │   │   ├── roulette.ts
│   │   │   └── dice.ts
│   │   └── actions/
│   │       └── pages/
│   │           ├── slots.ts
│   │           ├── cards.ts
│   │           ├── table.ts
│   │           ├── live.ts
│   │           └── account.ts
│   └── types/
│       ├── games.ts
│       ├── slots.ts
│       ├── cards.ts
│       ├── table.ts
│       ├── tournaments.ts
│       └── wallet.ts
```

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(500),
    vip_level INTEGER DEFAULT 1, -- 1-10 VIP tiers
    total_chips BIGINT DEFAULT 10000, -- starting chips
    daily_bonus_claimed_at DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW()
);

-- Slot machines
CREATE TABLE slot_machines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    theme VARCHAR(100), -- classic, video, progressive
    reels INTEGER DEFAULT 5, -- number of reels
    paylines INTEGER DEFAULT 25, -- number of paylines
    min_bet INTEGER DEFAULT 1,
    max_bet INTEGER DEFAULT 100,
    rtp_percentage DECIMAL(5,2) DEFAULT 95.00, -- return to player
    jackpot_base INTEGER DEFAULT 1000,
    jackpot_current BIGINT DEFAULT 1000,
    symbols JSONB NOT NULL, -- reel symbols and weights
    paytable JSONB NOT NULL, -- winning combinations
    bonus_features JSONB, -- free spins, multipliers, etc.
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Slot game sessions
CREATE TABLE slot_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    machine_id INTEGER REFERENCES slot_machines(id),
    spins_count INTEGER DEFAULT 0,
    total_bet BIGINT DEFAULT 0,
    total_win BIGINT DEFAULT 0,
    biggest_win BIGINT DEFAULT 0,
    bonus_rounds_triggered INTEGER DEFAULT 0,
    session_duration INTEGER DEFAULT 0, -- seconds
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

-- Individual slot spins
CREATE TABLE slot_spins (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES slot_sessions(id),
    user_id INTEGER REFERENCES users(id),
    machine_id INTEGER REFERENCES slot_machines(id),
    bet_amount INTEGER NOT NULL,
    reel_results JSONB NOT NULL, -- actual reel symbols
    win_amount BIGINT DEFAULT 0,
    winning_lines JSONB, -- which paylines won
    bonus_triggered BOOLEAN DEFAULT FALSE,
    jackpot_won BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Blackjack tables
CREATE TABLE blackjack_tables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    min_bet INTEGER DEFAULT 5,
    max_bet INTEGER DEFAULT 500,
    max_players INTEGER DEFAULT 7,
    current_players INTEGER DEFAULT 0,
    dealer_stands_soft_17 BOOLEAN DEFAULT TRUE,
    blackjack_pays VARCHAR(10) DEFAULT '3:2', -- 3:2 or 6:5
    insurance_available BOOLEAN DEFAULT TRUE,
    double_after_split BOOLEAN DEFAULT TRUE,
    surrender_allowed BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE
);

-- Blackjack games
CREATE TABLE blackjack_games (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES blackjack_tables(id),
    game_state VARCHAR(20) DEFAULT 'waiting', -- waiting, dealing, playing, completed
    dealer_cards JSONB DEFAULT '[]',
    dealer_hand_value INTEGER DEFAULT 0,
    dealer_busted BOOLEAN DEFAULT FALSE,
    shoe_cards JSONB, -- remaining cards in shoe
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Blackjack hands (individual player hands)
CREATE TABLE blackjack_hands (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES blackjack_games(id),
    user_id INTEGER REFERENCES users(id),
    seat_position INTEGER, -- 1-7 seat at table
    cards JSONB DEFAULT '[]',
    hand_value INTEGER DEFAULT 0,
    soft_ace BOOLEAN DEFAULT FALSE,
    bet_amount INTEGER NOT NULL,
    insurance_bet INTEGER DEFAULT 0,
    doubled_down BOOLEAN DEFAULT FALSE,
    split_from_hand_id INTEGER REFERENCES blackjack_hands(id),
    hand_status VARCHAR(20) DEFAULT 'playing', -- playing, stand, busted, blackjack
    result VARCHAR(20), -- win, lose, push, blackjack
    payout INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Poker tables
CREATE TABLE poker_tables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    game_type VARCHAR(50) NOT NULL, -- holdem, draw, stud
    table_type VARCHAR(20) DEFAULT 'cash', -- cash, tournament, sit_n_go
    max_players INTEGER DEFAULT 9,
    current_players INTEGER DEFAULT 0,
    small_blind INTEGER,
    big_blind INTEGER,
    buy_in_min INTEGER,
    buy_in_max INTEGER,
    active BOOLEAN DEFAULT TRUE
);

-- Poker games
CREATE TABLE poker_games (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES poker_tables(id),
    game_state VARCHAR(20) DEFAULT 'waiting', -- waiting, dealing, betting, showdown
    dealer_position INTEGER, -- button position
    small_blind_position INTEGER,
    big_blind_position INTEGER,
    current_actor INTEGER, -- whose turn it is
    pot_size INTEGER DEFAULT 0,
    community_cards JSONB DEFAULT '[]',
    deck_cards JSONB, -- shuffled deck
    betting_round VARCHAR(20), -- preflop, flop, turn, river
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Poker hands (individual player participation)
CREATE TABLE poker_hands (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES poker_games(id),
    user_id INTEGER REFERENCES users(id),
    seat_position INTEGER,
    hole_cards JSONB, -- private cards
    hand_rank VARCHAR(50), -- high card, pair, etc.
    best_hand JSONB, -- best 5-card hand
    total_bet INTEGER DEFAULT 0,
    action_history JSONB DEFAULT '[]', -- fold, call, raise, etc.
    result VARCHAR(20), -- win, lose
    winnings INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Roulette tables
CREATE TABLE roulette_tables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    wheel_type VARCHAR(20) DEFAULT 'european', -- european, american, french
    min_bet INTEGER DEFAULT 1,
    max_bet INTEGER DEFAULT 1000,
    max_players INTEGER DEFAULT 8,
    current_players INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

-- Roulette spins
CREATE TABLE roulette_spins (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES roulette_tables(id),
    winning_number INTEGER NOT NULL, -- 0-36 (or 00 for American)
    winning_color VARCHAR(10), -- red, black, green
    spin_time TIMESTAMP DEFAULT NOW()
);

-- Roulette bets
CREATE TABLE roulette_bets (
    id SERIAL PRIMARY KEY,
    spin_id INTEGER REFERENCES roulette_spins(id),
    user_id INTEGER REFERENCES users(id),
    bet_type VARCHAR(50) NOT NULL, -- straight, split, corner, red, black, etc.
    bet_numbers INTEGER[], -- numbers covered by bet
    bet_amount INTEGER NOT NULL,
    payout_ratio DECIMAL(5,2), -- 35:1, 17:1, 1:1, etc.
    won BOOLEAN DEFAULT FALSE,
    winnings INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dice games (Craps)
CREATE TABLE dice_games (
    id SERIAL PRIMARY KEY,
    table_id VARCHAR(100) DEFAULT 'main_craps',
    game_state VARCHAR(20) DEFAULT 'come_out', -- come_out, point
    point_number INTEGER, -- established point (4,5,6,8,9,10)
    shooter_id INTEGER REFERENCES users(id),
    roll_count INTEGER DEFAULT 0,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

-- Dice rolls
CREATE TABLE dice_rolls (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES dice_games(id),
    shooter_id INTEGER REFERENCES users(id),
    die1 INTEGER NOT NULL, -- 1-6
    die2 INTEGER NOT NULL, -- 1-6
    total INTEGER NOT NULL, -- sum of dice
    roll_type VARCHAR(20), -- come_out, point, seven_out
    created_at TIMESTAMP DEFAULT NOW()
);

-- Dice bets
CREATE TABLE dice_bets (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES dice_games(id),
    roll_id INTEGER REFERENCES dice_rolls(id),
    user_id INTEGER REFERENCES users(id),
    bet_type VARCHAR(50) NOT NULL, -- pass, dont_pass, come, field, etc.
    bet_amount INTEGER NOT NULL,
    odds_bet_amount INTEGER DEFAULT 0, -- additional odds bet
    won BOOLEAN DEFAULT FALSE,
    winnings INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tournaments
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    game_type VARCHAR(50) NOT NULL, -- slots, blackjack, poker, etc.
    tournament_type VARCHAR(20) DEFAULT 'scheduled', -- scheduled, sit_n_go
    buy_in INTEGER DEFAULT 0,
    prize_pool INTEGER DEFAULT 0,
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, active, completed
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tournament participants
CREATE TABLE tournament_participants (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(id),
    user_id INTEGER REFERENCES users(id),
    entry_fee INTEGER,
    current_score BIGINT DEFAULT 0,
    final_rank INTEGER,
    prize_won INTEGER DEFAULT 0,
    eliminated BOOLEAN DEFAULT FALSE,
    registered_at TIMESTAMP DEFAULT NOW()
);

-- User transactions (chips)
CREATE TABLE chip_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(50) NOT NULL, -- game_win, game_loss, daily_bonus, purchase
    amount BIGINT NOT NULL, -- positive or negative
    balance_after BIGINT NOT NULL,
    game_type VARCHAR(50), -- slots, blackjack, poker, etc.
    game_id INTEGER, -- reference to specific game
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User achievements
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- gaming, social, progression
    icon_url VARCHAR(500),
    points INTEGER DEFAULT 0,
    rarity VARCHAR(20) DEFAULT 'common', -- common, rare, epic, legendary
    criteria JSONB NOT NULL, -- conditions to unlock
    active BOOLEAN DEFAULT TRUE
);

-- User achievement progress
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    achievement_id INTEGER REFERENCES achievements(id),
    progress DECIMAL(5,2) DEFAULT 0.00, -- percentage completed
    unlocked BOOLEAN DEFAULT FALSE,
    unlocked_at TIMESTAMP,
    UNIQUE(user_id, achievement_id)
);

-- Friends and social
CREATE TABLE friendships (
    id SERIAL PRIMARY KEY,
    requester_id INTEGER REFERENCES users(id),
    addressee_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, blocked
    created_at TIMESTAMP DEFAULT NOW(),
    accepted_at TIMESTAMP,
    UNIQUE(requester_id, addressee_id)
);

-- Daily bonuses and rewards
CREATE TABLE daily_bonuses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    bonus_date DATE NOT NULL,
    consecutive_days INTEGER DEFAULT 1,
    bonus_amount INTEGER NOT NULL,
    bonus_type VARCHAR(50) DEFAULT 'daily', -- daily, weekly, special
    claimed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, bonus_date)
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
```

### Slot Game Routes (Slots Pages)
```
GET    /api/slots/machines       # Get available slot machines
POST   /api/slots/:id/spin       # Spin slot machine
GET    /api/slots/:id/info       # Get machine details and paytable
POST   /api/slots/session/start  # Start new slot session
POST   /api/slots/session/end    # End slot session
GET    /api/slots/jackpots       # Get current jackpot amounts
GET    /api/slots/leaderboard    # Get biggest winners
```

### Card Game Routes (Cards Pages)
```
GET    /api/blackjack/tables     # Get available blackjack tables
POST   /api/blackjack/:id/join   # Join blackjack table
POST   /api/blackjack/:id/bet    # Place bet
POST   /api/blackjack/:id/hit    # Hit (take card)
POST   /api/blackjack/:id/stand  # Stand (no more cards)
POST   /api/blackjack/:id/double # Double down
POST   /api/blackjack/:id/split  # Split hand
GET    /api/poker/tables         # Get poker tables
POST   /api/poker/:id/join       # Join poker table
POST   /api/poker/:id/action     # Poker action (fold, call, raise)
```

### Table Game Routes (Table Pages)
```
GET    /api/roulette/tables      # Get roulette tables
POST   /api/roulette/:id/bet     # Place roulette bet
GET    /api/roulette/:id/spin    # Get spin result
GET    /api/roulette/:id/history # Get recent numbers
GET    /api/craps/tables         # Get craps tables
POST   /api/craps/:id/bet        # Place craps bet
POST   /api/craps/:id/roll       # Roll dice (if shooter)
GET    /api/craps/:id/state      # Get current game state
```

### Live Casino Routes (Live Pages)
```
GET    /api/live/dealers         # Get available dealers
GET    /api/live/tables          # Get live dealer tables
POST   /api/live/:id/join        # Join live table
GET    /api/tournaments          # Get tournaments
POST   /api/tournaments/:id/join # Join tournament
GET    /api/tournaments/:id      # Get tournament details
GET    /api/leaderboards         # Get game leaderboards
```

### Account Routes (Account Pages)
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update profile
GET    /api/user/balance         # Get chip balance
GET    /api/user/transactions    # Get transaction history
POST   /api/user/daily-bonus     # Claim daily bonus
GET    /api/user/achievements    # Get achievements
GET    /api/user/stats           # Get gaming statistics
GET    /api/user/friends         # Get friends list
POST   /api/user/friends/add     # Send friend request
```

### Social and Competition Routes
```
POST   /api/friends/request      # Send friend request
POST   /api/friends/accept       # Accept friend request
GET    /api/achievements         # Get all achievements
POST   /api/chat/send            # Send chat message
GET    /api/chat/:tableId        # Get table chat history
```

## Key Features
- Realistic slot machine physics and animations
- Multi-player card games with live chat
- Progressive jackpots and daily bonuses
- Tournament competitions with leaderboards
- Social features and achievement system
- VIP progression and exclusive benefits
- Responsible gaming tools and limits

## Technical Implementation
- HTML5 Canvas for game animations
- WebSocket connections for real-time multiplayer
- Random number generation with cryptographic security
- Game state management and persistence
- Sound effects and ambient casino audio
- Mobile touch optimizations

## Demo Highlights
- Smooth slot reel animations with realistic physics
- Interactive card games with drag-and-drop
- Real-time multiplayer tables with chat
- Progressive jackpot tracking and celebrations
- Achievement unlock animations and rewards
- Mobile-optimized touch gaming interface