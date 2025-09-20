# 04 - Chess Training App MVP

## Implementation Plan

### Phase 1: Base Application Setup
This app uses the shared base React Vite application with all required dependencies:

1. **Base App Foundation** from `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite + TypeScript
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **Chess App Setup** - Copy base app structure (excluding src) to create chess-app directory

3. **Page Generation** - Use template-based generator to create complete chess training structure

### Phase 2: Chess App Generation
Use the template-based generator to create the complete chess training app structure on top of the base app foundation.

## App Vision
A comprehensive chess training platform focusing on skill development through play, puzzles, and structured learning. Think "Chess.com meets Khan Academy" with interactive lessons, tactical puzzles, and both single-player and multiplayer gameplay.

## What Makes This Special
- **Interactive Chess Board** - Full-featured chess board with piece movement
- **Adaptive Learning** - Personalized training based on skill level
- **Puzzle Engine** - Thousands of tactical puzzles with difficulty progression
- **Live Analysis** - Real-time position evaluation and move suggestions

## Parent Pages & Children

### 1. **Play** Parent
**Purpose**: Chess gameplay in various formats

#### **SinglePlayer** Child Page
- **Game Modes**:
  - vs Computer with adjustable difficulty (1-10 levels)
  - Analysis Board for position study
  - Practice specific openings
  - Endgame training scenarios
- **AI Opponent Features**:
  - Stockfish integration for computer moves
  - Difficulty slider from beginner to master
  - Playing style selection (aggressive, positional, tactical)
  - Hint system with move suggestions
- **Game Interface**:
  - Interactive chess board with drag-and-drop
  - Move notation display (algebraic notation)
  - Captured pieces display
  - Clock/timer for timed games
  - Take back move functionality
  - Game save/load capabilities
- **Post-Game Analysis**:
  - Move-by-move analysis with engine evaluation
  - Blunder detection and highlighting
  - Alternative move suggestions
  - Opening identification and statistics
- **Training Scenarios**:
  - Mate in 1, 2, 3 puzzles
  - Specific endgame positions (K+Q vs K, etc.)
  - Opening trap avoidance
  - Tactical pattern recognition

#### **Multiplayer** Child Page
- **Game Matching**:
  - Quick pairing by rating range
  - Custom game creation (time controls, rated/unrated)
  - Challenge friends by username
  - Tournament brackets and swiss pairings
- **Live Game Features**:
  - Real-time move synchronization
  - Chat system with quick phrases
  - Draw offers and resignation
  - Spectator mode for watching games
  - Game recording and PGN export
- **Time Controls**:
  - Bullet (1-2 minutes)
  - Blitz (3-10 minutes) 
  - Rapid (10-30 minutes)
  - Classical (30+ minutes)
  - Custom increment and delay options
- **Rating System**:
  - Elo rating calculations
  - Separate ratings for different time controls
  - Rating history graphs and progress tracking
  - Leaderboards and ranking displays
- **Social Features**:
  - Friend lists and online status
  - Game history vs specific opponents
  - Challenge notifications
  - Profile pages with game statistics

### 2. **Puzzles** Parent
**Purpose**: Tactical training and puzzle solving

#### **Tactics** Child Page
- **Puzzle Database**:
  - 10,000+ tactical puzzles from real games
  - Difficulty ratings from 800-2800 Elo
  - Puzzle themes: pins, forks, skewers, discoveries
  - Daily fresh puzzles and puzzle of the day
- **Adaptive Training**:
  - Personalized puzzle difficulty based on performance
  - Spaced repetition for failed puzzles
  - Progress tracking with success rates
  - Time-based scoring and leaderboards
- **Puzzle Interface**:
  - Clean board presentation with highlighted pieces
  - Multiple choice hints for beginners
  - Solution explanations with variations
  - Progress indicators and streak counters
- **Training Modes**:
  - Timed puzzle rushes (5 puzzles in 3 minutes)
  - Themed puzzle sets (e.g., "Knight Forks")
  - Progressive difficulty climbs
  - Puzzle competitions and tournaments
- **Performance Analytics**:
  - Success rate by puzzle theme
  - Average solve time tracking
  - Difficulty progression graphs
  - Weak area identification and recommendations

#### **Endgames** Child Page
- **Endgame Categories**:
  - Basic checkmates (Q+K vs K, R+K vs K)
  - Pawn endgames (opposition, passed pawns)
  - Rook endgames (Lucena, Philidor positions)
  - Knight and Bishop endgames
- **Interactive Lessons**:
  - Step-by-step endgame technique tutorials
  - Practice positions with guided solutions
  - Common mistakes and how to avoid them
  - Theoretical position database
- **Endgame Trainer**:
  - Random position generator for practice
  - Win/draw evaluation challenges
  - Time pressure endgame solving
  - Progress tracking for each endgame type
- **Study Materials**:
  - Endgame principle explanations
  - Famous endgame studies and compositions
  - Practical endgame tips and tricks
  - Video lessons with grandmaster analysis

### 3. **Learn** Parent
**Purpose**: Structured chess education and improvement

#### **Openings** Child Page
- **Opening Explorer**:
  - Comprehensive opening database
  - Move tree navigation with statistics
  - Master game examples for each opening
  - Opening popularity and success rates
- **Opening Trainer**:
  - Memorization drills for opening moves
  - Repertoire building tools
  - Opening mistake identification
  - Transposition recognition practice
- **Opening Categories**:
  - King's Pawn (1.e4) openings
  - Queen's Pawn (1.d4) openings  
  - English Opening and Réti System
  - Sicilian Defense variations
  - French, Caro-Kann, and other defenses
- **Study Tools**:
  - Personal opening repertoire builder
  - Opening preparation against specific opponents
  - Novelty detection and analysis
  - Opening quiz and testing system
- **Analysis Features**:
  - Engine evaluation of opening positions
  - Statistical analysis of your opening performance
  - Trending openings and meta shifts
  - Opening traps and tactical motifs

#### **Strategy** Child Page
- **Strategic Concepts**:
  - Pawn structure evaluation and planning
  - Piece activity and coordination
  - King safety and attacking patterns
  - Positional sacrifices and compensation
- **Interactive Lessons**:
  - Annotated master games with explanations
  - Position evaluation exercises
  - Strategic decision-making practice
  - Plan formulation training
- **Strategic Themes**:
  - Weak squares and outposts
  - Open files and diagonals
  - Pawn storms and breakthroughs
  - Piece exchanges and simplification
- **Study Materials**:
  - Classic strategic games collection
  - Positional pattern recognition
  - Strategic principles and guidelines
  - Advanced strategic concepts

### 4. **Profile** Parent
**Purpose**: Personal progress and statistics

#### **Stats** Child Page
- **Performance Metrics**:
  - Current ratings across all categories
  - Rating progression graphs over time
  - Win/loss/draw statistics
  - Average game length and time usage
- **Game Analysis**:
  - Recent games with computer analysis
  - Blunder rate and accuracy percentage
  - Opening repertoire success rates
  - Endgame conversion rates
- **Training Progress**:
  - Puzzles solved and accuracy rates
  - Lessons completed and mastery levels
  - Time spent training vs playing
  - Skill area improvements and weaknesses
- **Achievement System**:
  - Chess achievement badges and trophies
  - Milestone celebrations (rating milestones)
  - Training streaks and consistency rewards
  - Tournament victories and placements

#### **Settings** Child Page
- **Board Preferences**:
  - Board themes and piece sets
  - Square highlighting and move indicators
  - Animation speed and sound effects
  - Coordinate display and orientation
- **Game Settings**:
  - Default time controls and preferences
  - Auto-queen promotion vs promotion choice
  - Premove settings for online play
  - Analysis depth and engine strength
- **Training Configuration**:
  - Puzzle difficulty ranges
  - Lesson pace and review settings
  - Notification preferences for training reminders
  - Progress tracking and privacy settings
- **Account Management**:
  - Profile information and avatar
  - Privacy settings and data export
  - Subscription management (if applicable)
  - Account deletion and data removal

## Theme & Layout System

### Onyx Theme
This app uses the **Onyx** theme from the professional themes collection, providing a sophisticated, chess-focused aesthetic with high contrast for optimal board visibility.

**Theme Variables (Onyx):**
```css
/* Onyx Theme Variables */
--primary: #71717a;           /* Zinc gray primary */
--accent: #71717a;            /* Zinc gray accent */
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
- **Play** - Chess piece icon (SinglePlayer, Multiplayer)
- **Puzzles** - Puzzle piece icon (Tactics, Endgames)
- **Learn** - Book icon (Openings, Strategy)
- **Profile** - User icon (Stats, Settings)

### Layout Templates

#### Desktop Pages (ChessboardLayout)
5-panel design optimized for chess interfaces:
```jsx
<ChessboardLayout
  topLeft={<div className="chess-controls">Game Controls</div>}
  top={<div className="chess-notation">Move Notation</div>}
  topRight={<div className="chess-timer">Game Timer</div>}
  left={<div className="chess-captured">Captured Pieces</div>}
  center={<div className="chess-board">Chess Board</div>}
  right={<div className="chess-analysis">Analysis/Engine</div>}
  bottomLeft={<div className="chess-history">Move History</div>}
  bottom={<div className="chess-status">Game Status</div>}
  bottomRight={<div className="chess-actions">Quick Actions</div>}
/>
```

#### Mobile Pages (MobileChessboardLayout)
3-panel design optimized for mobile chess:
```jsx
<MobileChessboardLayout
  topPieces={<div className="chess-mobile-header">Timer/Controls</div>}
  center={<div className="chess-mobile-board">Chess Board</div>}
  bottomPieces={<div className="chess-mobile-actions">Notation/Actions</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `chess-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables
- **NO hardcoded colors** - only theme-aware classes
- **Templates are NEVER modified** - only the generated app's CSS

Add these NEW classes to the generated `chess-app/src/index.css`:

```css
/* Chess App Component Classes */
.chess-board {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg;
  @apply aspect-square w-full max-w-lg mx-auto;
  @apply relative overflow-hidden;
}

.chess-square {
  @apply absolute cursor-pointer transition-all duration-200;
  @apply hover:bg-primary/20;
}

.chess-square.light {
  @apply bg-gray-100;
}

.chess-square.dark {
  @apply bg-gray-700;
}

.chess-piece {
  @apply w-full h-full flex items-center justify-center;
  @apply text-4xl select-none cursor-grab;
  @apply hover:scale-110 transition-transform duration-200;
}

.chess-notation {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply font-mono text-sm max-h-64 overflow-y-auto;
}

.chess-captured-pieces {
  @apply flex flex-wrap gap-1 p-2;
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg;
}

.chess-timer {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply text-center font-mono text-lg;
}

.chess-analysis {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply space-y-2;
}

.chess-puzzle-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply hover:bg-surface-variant/60 hover:border-primary/30 transition-all duration-300;
  @apply cursor-pointer;
}

.chess-rating-badge {
  @apply bg-primary/20 text-primary px-2 py-1 rounded-full text-xs font-semibold;
  @apply border border-primary/30;
}

.chess-difficulty-indicator {
  @apply flex items-center gap-1;
}

.chess-difficulty-dot {
  @apply w-2 h-2 rounded-full;
  @apply data-[active=true]:bg-primary data-[active=false]:bg-outline/30;
}

.chess-lesson-card {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply hover:bg-surface-variant/40 transition-colors cursor-pointer;
}

.chess-stats-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-xl p-6;
  @apply text-center space-y-2;
}
```

### ASCII Mockups

#### Desktop Layout (ChessboardLayout)
```
┌─────────────────────────────────────────────────────────────────┐
│                     Chess Training App                        │
├─────────┬─────────────────────────┬─────────────────────────────┤
│  Game   │      Move Notation      │       Game Timer           │
│Controls │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│         │        ┌────────┐        │                             │
│Captured │        │♖♗♘♙♚♛♜♝│        │   Analysis/Engine          │
│ Pieces  │        │♔♕♖♗♘♙♚♛│        │                             │
│         │        │♜♝♞♟♠♡♢♣│        │                             │
│         │        └────────┘        │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│  Move   │      Game Status       │     Quick Actions          │
│ History │                         │                             │
├─────────┴─────────────────────────┴─────────────────────────────┤
│                          TabBar                                 │
│       Play     Puzzles    Learn    Profile                      │
└─────────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (MobileChessboardLayout)
```
┌─────────────────────────────────┐
│       Chess Training App       │
├─────────────────────────────────┤
│       Timer/Controls            │
│                                 │
├─────────────────────────────────┤
│           ┌────────┐           │
│           │♖♗♘♙♚♛♜♝│           │
│           │♔♕♖♗♘♙♚♛│           │
│           │♜♝♞♟♠♡♢♣│           │
│           └────────┘           │
├─────────────────────────────────┤
│      Notation/Actions           │
│                                 │
├─────────────────────────────────┤
│             TabBar              │
│   Play  Puzzles Learn Profile   │
└─────────────────────────────────┘
```

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile SinglePlayer Page**
- **Touch Chess Board**: Large, finger-friendly piece movement
- **Gesture Controls**: Tap to select, tap to move pieces
- **Mobile UI**: Collapsible panels for notation and captured pieces
- **Portrait Mode**: Optimized board size for vertical screens
- **Quick Actions**: Easy access to hint, takeback, and resign

#### **Mobile Multiplayer Page**
- **Swipe Navigation**: Swipe between active games
- **Touch Chat**: Mobile keyboard optimized chat interface
- **Game Notifications**: Push notifications for moves and challenges
- **Quick Pairing**: One-tap game matching
- **Mobile Timer**: Large, visible countdown clocks

#### **Mobile Tactics Page**
- **Full-Screen Puzzles**: Immersive puzzle solving experience
- **Touch Hints**: Tap for progressive hint system
- **Swipe Progress**: Swipe to next puzzle
- **Mobile Timer**: Prominent puzzle timer display
- **Quick Rating**: Immediate feedback after solving

#### **Mobile Endgames Page**
- **Step-by-Step**: Mobile-friendly lesson progression
- **Touch Practice**: Easy endgame position practice
- **Guided Solutions**: Touch-friendly move guidance
- **Progress Tracking**: Visual progress indicators
- **Quick Access**: Easy navigation between endgame types

#### **Mobile Openings Page**
- **Tree Navigation**: Touch-friendly opening explorer
- **Swipe Moves**: Horizontal swipe through move sequences
- **Mobile Repertoire**: Easy repertoire building tools
- **Quick Drill**: One-tap opening practice sessions
- **Touch Analysis**: Easy access to move evaluations

#### **Mobile Strategy Page**
- **Scrollable Lessons**: Mobile-optimized lesson content
- **Interactive Examples**: Touch-friendly position exploration
- **Mobile Quizzes**: Touch-optimized strategic tests
- **Progress Indicators**: Clear lesson completion tracking
- **Quick Review**: Easy access to completed lessons

#### **Mobile Stats Page**
- **Scrollable Charts**: Mobile-friendly performance graphs
- **Touch Details**: Tap to expand statistical details
- **Swipe Categories**: Horizontal navigation between stat types
- **Mobile Dashboard**: Key metrics at a glance
- **Quick Analysis**: Easy access to recent game analysis

#### **Mobile Settings Page**
- **Collapsible Sections**: Mobile-friendly settings organization
- **Touch Controls**: Large toggle switches and sliders
- **Mobile Themes**: Touch preview of board themes
- **Quick Setup**: One-tap configuration presets
- **Touch Save**: Easy settings synchronization

## Implementation Commands

### Phase 1: Setup Chess App Directory

```bash
# Copy base app structure (excluding src folder) to chess-app
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2
mkdir -p chess-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} chess-app/

# Navigate to chess app directory and install dependencies
cd chess-app
npm install
cd ..
```

### Phase 2: Generate Chess App Pages

```bash
# Navigate to generator directory
cd chess-app

# Create parent pages
npm run mobile -- parent Play
npm run mobile -- parent Puzzles
npm run mobile -- parent Learn
npm run mobile -- parent Profile

# Create child pages with mobile variants under Play parent
npm run mobile -- child SinglePlayer --parent play npm run mobile -- child Multiplayer --parent play 
# Create child pages with mobile variants under Puzzles parent
npm run mobile -- child Tactics --parent puzzles npm run mobile -- child Endgames --parent puzzles 
# Create child pages with mobile variants under Learn parent
npm run mobile -- child Openings --parent learn npm run mobile -- child Strategy --parent learn 
# Create child pages with mobile variants under Profile parent
npm run mobile -- child Stats --parent profile npm run mobile -- child Settings --parent profile ```

## File Structure Tree

```
chess-app/
├── src/
│   ├── components/
│   │   ├── play/
│   │   │   ├── SinglePlayerPageWrapper.tsx
│   │   │   ├── MultiplayerPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── puzzles/
│   │   │   ├── TacticsPageWrapper.tsx
│   │   │   ├── EndgamesPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── learn/
│   │   │   ├── OpeningsPageWrapper.tsx
│   │   │   ├── StrategyPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── profile/
│   │       ├── StatsPageWrapper.tsx
│   │       ├── SettingsPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── play/
│   │   │   ├── PlayPage.tsx
│   │   │   ├── PlayMainPage.tsx
│   │   │   ├── SinglePlayerPage.tsx
│   │   │   ├── MobileSinglePlayerPage.tsx
│   │   │   ├── MultiplayerPage.tsx
│   │   │   └── MobileMultiplayerPage.tsx
│   │   ├── puzzles/
│   │   │   ├── PuzzlesPage.tsx
│   │   │   ├── PuzzlesMainPage.tsx
│   │   │   ├── TacticsPage.tsx
│   │   │   ├── MobileTacticsPage.tsx
│   │   │   ├── EndgamesPage.tsx
│   │   │   └── MobileEndgamesPage.tsx
│   │   ├── learn/
│   │   │   ├── LearnPage.tsx
│   │   │   ├── LearnMainPage.tsx
│   │   │   ├── OpeningsPage.tsx
│   │   │   ├── MobileOpeningsPage.tsx
│   │   │   ├── StrategyPage.tsx
│   │   │   └── MobileStrategyPage.tsx
│   │   └── profile/
│   │       ├── ProfilePage.tsx
│   │       ├── ProfileMainPage.tsx
│   │       ├── StatsPage.tsx
│   │       ├── MobileStatsPage.tsx
│   │       ├── SettingsPage.tsx
│   │       └── MobileSettingsPage.tsx
│   ├── hooks/
│   │   ├── play/
│   │   │   └── usePlayActions.ts
│   │   ├── puzzles/
│   │   │   └── usePuzzlesActions.ts
│   │   ├── learn/
│   │   │   └── useLearnActions.ts
│   │   └── profile/
│   │       └── useProfileActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── gamesApi.ts
│   │   │   ├── puzzlesApi.ts
│   │   │   ├── openingsApi.ts
│   │   │   ├── analysisApi.ts
│   │   │   └── userApi.ts
│   │   ├── chess/
│   │   │   ├── chessEngine.ts
│   │   │   ├── moveValidation.ts
│   │   │   ├── pgn.ts
│   │   │   └── fen.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── play.ts
│   │           ├── puzzles.ts
│   │           ├── learn.ts
│   │           └── profile.ts
│   ├── constants/
│   │   ├── chess/
│   │   │   ├── pieces.ts
│   │   │   ├── squares.ts
│   │   │   └── openings.ts
│   │   └── actions/
│   │       └── pages/
│   │           ├── play.ts
│   │           ├── puzzles.ts
│   │           ├── learn.ts
│   │           └── profile.ts
│   └── types/
│       ├── chess.ts
│       ├── games.ts
│       ├── puzzles.ts
│       ├── openings.ts
│       └── user.ts
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
    country VARCHAR(50),
    rating_bullet INTEGER DEFAULT 1200,
    rating_blitz INTEGER DEFAULT 1200,
    rating_rapid INTEGER DEFAULT 1200,
    rating_classical INTEGER DEFAULT 1200,
    rating_tactics INTEGER DEFAULT 1200,
    premium_member BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW()
);

-- Games table
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    white_player_id INTEGER REFERENCES users(id),
    black_player_id INTEGER REFERENCES users(id),
    game_type VARCHAR(20) NOT NULL, -- bullet, blitz, rapid, classical, computer
    time_control VARCHAR(20), -- 3+0, 5+3, 10+0, etc.
    rated BOOLEAN DEFAULT TRUE,
    status VARCHAR(20) DEFAULT 'active', -- active, completed, aborted
    result VARCHAR(10), -- 1-0, 0-1, 1/2-1/2
    termination VARCHAR(30), -- checkmate, resignation, timeout, draw
    moves TEXT[], -- array of moves in algebraic notation
    pgn TEXT, -- full PGN of the game
    starting_fen VARCHAR(100) DEFAULT 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    white_rating_before INTEGER,
    black_rating_before INTEGER,
    white_rating_after INTEGER,
    black_rating_after INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Computer games (single player)
CREATE TABLE computer_games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    user_color VARCHAR(5) NOT NULL, -- white, black
    computer_level INTEGER NOT NULL, -- 1-10 difficulty
    status VARCHAR(20) DEFAULT 'active',
    result VARCHAR(10),
    moves TEXT[],
    pgn TEXT,
    analysis JSONB, -- post-game analysis data
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Puzzles table
CREATE TABLE puzzles (
    id SERIAL PRIMARY KEY,
    fen VARCHAR(100) NOT NULL, -- position FEN
    moves TEXT[] NOT NULL, -- solution moves
    themes TEXT[] NOT NULL, -- pin, fork, skewer, etc.
    rating INTEGER NOT NULL, -- puzzle difficulty rating
    popularity INTEGER DEFAULT 0,
    game_url VARCHAR(200), -- source game if available
    created_at TIMESTAMP DEFAULT NOW()
);

-- User puzzle attempts
CREATE TABLE puzzle_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    puzzle_id INTEGER REFERENCES puzzles(id),
    solved BOOLEAN NOT NULL,
    time_spent INTEGER, -- seconds to solve
    attempts INTEGER DEFAULT 1, -- number of attempts
    rating_change INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Opening database
CREATE TABLE openings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL, -- Sicilian Defense, King's Indian, etc.
    eco_code VARCHAR(10), -- ECO classification (A00-E99)
    moves TEXT[] NOT NULL, -- opening moves sequence
    parent_opening_id INTEGER REFERENCES openings(id),
    popularity INTEGER DEFAULT 0,
    white_win_rate DECIMAL(5,2),
    black_win_rate DECIMAL(5,2),
    draw_rate DECIMAL(5,2)
);

-- User opening repertoire
CREATE TABLE user_repertoire (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    opening_id INTEGER REFERENCES openings(id),
    color VARCHAR(5) NOT NULL, -- white, black
    priority INTEGER DEFAULT 1, -- 1=main line, 2=secondary, etc.
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Training sessions
CREATE TABLE training_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_type VARCHAR(30) NOT NULL, -- tactics, endgames, openings
    problems_attempted INTEGER DEFAULT 0,
    problems_solved INTEGER DEFAULT 0,
    time_spent INTEGER DEFAULT 0, -- seconds
    accuracy_rate DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Lessons and courses
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL, -- openings, strategy, endgames
    difficulty_level INTEGER NOT NULL, -- 1-5 beginner to advanced
    content JSONB NOT NULL, -- lesson content and positions
    prerequisites INTEGER[], -- array of required lesson IDs
    estimated_time INTEGER, -- minutes to complete
    created_at TIMESTAMP DEFAULT NOW()
);

-- User lesson progress
CREATE TABLE user_lesson_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    completed BOOLEAN DEFAULT FALSE,
    progress_percent INTEGER DEFAULT 0,
    time_spent INTEGER DEFAULT 0,
    score INTEGER, -- lesson completion score
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
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

-- Game challenges
CREATE TABLE challenges (
    id SERIAL PRIMARY KEY,
    challenger_id INTEGER REFERENCES users(id),
    challenged_id INTEGER REFERENCES users(id),
    time_control VARCHAR(20),
    rated BOOLEAN DEFAULT TRUE,
    color_preference VARCHAR(10) DEFAULT 'random', -- white, black, random
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, declined, expired
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP DEFAULT (NOW() + INTERVAL '5 minutes')
);

-- Tournaments
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    format VARCHAR(20) NOT NULL, -- swiss, knockout, round_robin
    time_control VARCHAR(20),
    rated BOOLEAN DEFAULT TRUE,
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    entry_fee INTEGER DEFAULT 0, -- premium feature
    prize_description TEXT,
    status VARCHAR(20) DEFAULT 'upcoming', -- upcoming, active, completed
    registration_deadline TIMESTAMP,
    start_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tournament participants
CREATE TABLE tournament_participants (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(id),
    user_id INTEGER REFERENCES users(id),
    rating_at_entry INTEGER,
    final_score DECIMAL(3,1) DEFAULT 0.0,
    final_rank INTEGER,
    registered_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tournament_id, user_id)
);

-- User preferences and settings
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    board_theme VARCHAR(50) DEFAULT 'classic',
    piece_set VARCHAR(50) DEFAULT 'classic',
    auto_queen BOOLEAN DEFAULT FALSE,
    show_coordinates BOOLEAN DEFAULT TRUE,
    highlight_legal_moves BOOLEAN DEFAULT TRUE,
    animation_speed INTEGER DEFAULT 3, -- 1-5 scale
    sound_enabled BOOLEAN DEFAULT TRUE,
    notification_challenges BOOLEAN DEFAULT TRUE,
    notification_moves BOOLEAN DEFAULT TRUE,
    premove_enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
```

### Game Routes (Play Pages)
```
GET    /api/games/active         # Get user's active games
POST   /api/games/computer       # Start computer game
POST   /api/games/create         # Create multiplayer game
POST   /api/games/:id/join       # Join game
POST   /api/games/:id/move       # Make a move
GET    /api/games/:id            # Get game details
POST   /api/games/:id/resign     # Resign game
POST   /api/games/:id/draw       # Offer/accept draw
GET    /api/games/history        # Get game history
POST   /api/games/:id/analyze    # Request post-game analysis
```

### Puzzle Routes (Puzzles Pages)
```
GET    /api/puzzles/daily        # Get daily puzzle
GET    /api/puzzles/random       # Get random puzzle by rating
GET    /api/puzzles/themed       # Get puzzles by theme
POST   /api/puzzles/:id/attempt  # Submit puzzle solution
GET    /api/puzzles/stats        # Get user puzzle statistics
GET    /api/puzzles/leaderboard  # Get puzzle leaderboard
```

### Learning Routes (Learn Pages)
```
GET    /api/openings             # Get opening database
GET    /api/openings/:id         # Get specific opening
GET    /api/openings/explorer    # Opening move tree
POST   /api/repertoire           # Add to repertoire
GET    /api/repertoire           # Get user repertoire
GET    /api/lessons              # Get available lessons
GET    /api/lessons/:id          # Get lesson content
POST   /api/lessons/:id/complete # Mark lesson complete
GET    /api/endgames             # Get endgame positions
```

### User Profile Routes (Profile Pages)
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update profile
GET    /api/user/stats           # Get user statistics
GET    /api/user/rating-history  # Get rating progression
GET    /api/user/achievements    # Get achievements
GET    /api/user/preferences     # Get user preferences
PUT    /api/user/preferences     # Update preferences
```

### Social Routes
```
GET    /api/friends              # Get friends list
POST   /api/friends/request      # Send friend request
POST   /api/friends/accept       # Accept friend request
GET    /api/challenges           # Get game challenges
POST   /api/challenges           # Send game challenge
POST   /api/challenges/:id/accept # Accept challenge
```

### Tournament Routes
```
GET    /api/tournaments          # Get tournaments
POST   /api/tournaments/:id/join # Join tournament
GET    /api/tournaments/:id      # Get tournament details
GET    /api/tournaments/:id/pairings # Get tournament pairings
```

### Analysis Routes
```
POST   /api/analysis/position    # Analyze chess position
GET    /api/analysis/engine      # Get engine evaluation
POST   /api/analysis/game        # Analyze complete game
```

## Key Features
- Interactive chess board with drag-and-drop
- Real-time multiplayer gameplay
- Comprehensive puzzle training system
- Opening repertoire builder
- Post-game analysis with engine
- Rating system and progress tracking
- Tournament and challenge system

## Technical Implementation
- Chess.js library for move validation
- Stockfish engine integration for analysis
- WebSocket connections for real-time play
- PGN parsing and export functionality
- FEN position handling
- Rating calculation algorithms

## Demo Highlights
- Smooth chess piece animations
- Real-time opponent move updates
- Interactive puzzle solving interface
- Comprehensive opening explorer
- Detailed performance analytics
- Mobile-optimized chess board