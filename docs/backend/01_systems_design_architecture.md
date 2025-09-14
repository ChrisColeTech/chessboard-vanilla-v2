# Systems Design & Architecture

**Document Version:** 1.0  
**Date:** September 2025  
**Status:** DESIGN - Detailed Schema Architecture  
**Prerequisite:** 00_systems_proposal.md

## Design Principles

### Data Normalization
- Each piece of data stored in exactly one place
- Foreign keys enforce relationships
- No duplicate columns across tables
- JSON fields only for truly flexible data

### System Isolation
- Each system owns its data exclusively
- No cross-system data dependencies
- Clear APIs between systems
- Single responsibility per table

### Minimal Overlap Strategy
- One source of truth per data type
- Calculated fields avoided (computed at query time)
- Standardized ID formats across systems
- Consistent naming conventions

---

## System 1: User System

### Purpose
Manage user authentication, profiles, and login sessions.

### Tables

#### `users`
**Purpose:** Core authentication and chess-specific user data
```sql
CREATE TABLE users (
    -- Primary identification (UUID v4)
    id VARCHAR(36) PRIMARY KEY,
    
    -- Authentication (required)
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    
    -- Chess-specific data (core to app purpose)
    chess_elo INTEGER DEFAULT 1200 CHECK (chess_elo BETWEEN 400 AND 3000),
    puzzle_rating INTEGER DEFAULT 1200 CHECK (puzzle_rating BETWEEN 400 AND 3000),
    
    -- Game statistics (denormalized for performance)
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    games_lost INTEGER DEFAULT 0,
    games_drawn INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    
    -- Constraints
    CHECK (games_played >= 0),
    CHECK (games_won + games_lost + games_drawn <= games_played)
);
```

#### `user_profiles`
**Purpose:** Display preferences and social data (separate from authentication)
```sql
CREATE TABLE user_profiles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL UNIQUE,
    
    -- Display information
    display_name VARCHAR(50),
    avatar_url VARCHAR(500),
    bio TEXT,
    country VARCHAR(3), -- ISO 3166-1 alpha-3
    timezone VARCHAR(50),
    
    -- Chess preferences (JSON for flexibility)
    board_preferences JSONB DEFAULT '{}',
    -- Example: {"theme": "wood", "pieces": "staunton", "coordinates": true}
    
    -- Privacy settings
    profile_visibility VARCHAR(20) DEFAULT 'public' CHECK (profile_visibility IN ('public', 'friends', 'private')),
    show_rating BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### `user_sessions`
**Purpose:** Track login sessions for security and "logout all devices"
```sql
CREATE TABLE user_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    
    -- Session data
    refresh_token VARCHAR(500) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    
    -- Metadata for security
    ip_address INET,
    user_agent TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    last_accessed TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (expires_at > created_at)
);
```

### Anti-Redundancy Rules
- **No user data in other systems** - Other tables reference `user_id` only
- **Settings in profiles only** - No user preferences scattered across tables
- **Stats calculation** - Games stats computed from games table, cached in users table

---

## System 2: Games System

### Purpose
Manage chess gameplay and reference games.

### Tables

#### `games`
**Purpose:** User gameplay sessions (vs AI or other players)
```sql
CREATE TABLE games (
    -- Primary identification
    id VARCHAR(36) PRIMARY KEY,
    
    -- Players
    white_player_id VARCHAR(36) NOT NULL,
    black_player_id VARCHAR(36), -- NULL for AI games
    
    -- Game configuration
    time_control VARCHAR(20), -- "10+0", "5+3", "unlimited"
    ai_level INTEGER CHECK (ai_level BETWEEN 1 AND 5), -- NULL if not AI game
    
    -- Game state
    initial_fen VARCHAR(100) DEFAULT 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    current_fen VARCHAR(100) NOT NULL,
    pgn TEXT NOT NULL,
    
    -- Game result
    result VARCHAR(10) CHECK (result IN ('1-0', '0-1', '1/2-1/2', '*')),
    termination VARCHAR(30) CHECK (termination IN ('checkmate', 'resignation', 'timeout', 'draw', 'stalemate', 'insufficient_material')),
    
    -- Metadata
    opening_eco VARCHAR(5), -- A00-E99
    opening_name VARCHAR(100),
    move_count INTEGER DEFAULT 0,
    
    -- Rating changes (for user only, AI has no rating)
    white_elo_before INTEGER,
    white_elo_after INTEGER,
    black_elo_before INTEGER, -- NULL for AI games
    black_elo_after INTEGER,   -- NULL for AI games
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    FOREIGN KEY (white_player_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (black_player_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (move_count >= 0),
    CHECK (completed_at IS NULL OR completed_at >= started_at)
);
```

#### `historic_games`
**Purpose:** Famous games for study and reference (read-only data)
```sql
CREATE TABLE historic_games (
    id VARCHAR(36) PRIMARY KEY,
    
    -- Players (historical, not user references)
    white_player VARCHAR(100) NOT NULL,
    black_player VARCHAR(100) NOT NULL,
    white_rating INTEGER,
    black_rating INTEGER,
    
    -- Tournament context
    tournament_name VARCHAR(200),
    tournament_year INTEGER,
    round_info VARCHAR(50),
    
    -- Game data
    pgn TEXT NOT NULL,
    result VARCHAR(10) CHECK (result IN ('1-0', '0-1', '1/2-1/2')),
    
    -- Chess metadata
    opening_eco VARCHAR(5),
    opening_name VARCHAR(100),
    
    -- Educational metadata
    game_significance TEXT, -- Why this game is notable
    key_moments JSONB, -- Critical positions for study
    
    -- Timestamps
    game_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    
    CHECK (tournament_year IS NULL OR tournament_year BETWEEN 1800 AND 2100)
);
```

#### `openings`
**Purpose:** Chess opening reference database
```sql
CREATE TABLE openings (
    id VARCHAR(36) PRIMARY KEY,
    
    -- Opening identification
    eco_code VARCHAR(5) NOT NULL UNIQUE, -- A00-E99
    name VARCHAR(100) NOT NULL,
    
    -- Opening data
    moves TEXT NOT NULL, -- Standard opening moves
    fen VARCHAR(100) NOT NULL, -- Resulting position
    
    -- Metadata
    popularity INTEGER DEFAULT 0, -- How common this opening is
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Anti-Redundancy Rules
- **Game moves stored in PGN only** - No separate moves table for simplicity
- **Opening data centralized** - All opening info in openings table only
- **Historical vs user games separated** - Different purposes, different tables

---

## System 3: Puzzles System

### Purpose
Tactical training and puzzle management.

### Tables

#### `puzzles`
**Purpose:** Individual tactical problems
```sql
CREATE TABLE puzzles (
    -- Use external ID as primary key (e.g., "lichess_12345")
    id VARCHAR(50) PRIMARY KEY,
    
    -- Source tracking
    source_id VARCHAR(36) NOT NULL, -- References puzzle_sources
    
    -- Puzzle data
    fen VARCHAR(100) NOT NULL, -- Starting position
    moves TEXT NOT NULL, -- Solution moves (UCI format, space-separated)
    
    -- Difficulty and metadata
    rating INTEGER NOT NULL CHECK (rating BETWEEN 600 AND 3000),
    themes VARCHAR(200) NOT NULL, -- Comma-separated: "fork,pin,attack"
    
    -- Game context (optional)
    opening_family VARCHAR(100),
    game_phase VARCHAR(20) CHECK (game_phase IN ('opening', 'middlegame', 'endgame')),
    
    -- Usage statistics
    popularity INTEGER DEFAULT 0, -- -100 to 100 scale
    play_count INTEGER DEFAULT 0,
    success_rate DECIMAL(3,2), -- 0.00 to 1.00
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (source_id) REFERENCES puzzle_sources(id),
    CHECK (play_count >= 0),
    CHECK (success_rate IS NULL OR (success_rate >= 0.00 AND success_rate <= 1.00))
);
```

#### `puzzle_sources`
**Purpose:** Puzzle collection metadata and attribution
```sql
CREATE TABLE puzzle_sources (
    id VARCHAR(36) PRIMARY KEY,
    
    -- Source identification
    name VARCHAR(100) NOT NULL, -- "Lichess", "Chess.com", "Custom"
    description TEXT,
    
    -- Legal and attribution
    attribution TEXT, -- Copyright/credit info
    license VARCHAR(100), -- License type
    source_url VARCHAR(500), -- Original source URL
    
    -- Statistics (updated by triggers/batch jobs)
    total_puzzles INTEGER DEFAULT 0,
    average_rating INTEGER DEFAULT 1500,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_imported TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CHECK (total_puzzles >= 0),
    CHECK (average_rating BETWEEN 600 AND 3000)
);
```

#### `puzzle_attempts`
**Purpose:** User puzzle solving history and performance
```sql
CREATE TABLE puzzle_attempts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    puzzle_id VARCHAR(50) NOT NULL,
    
    -- Attempt data
    solved BOOLEAN NOT NULL,
    user_moves TEXT, -- User's attempted moves (UCI format)
    
    -- Performance metrics
    time_taken INTEGER NOT NULL, -- milliseconds
    hints_used INTEGER DEFAULT 0,
    attempt_number INTEGER DEFAULT 1, -- Multiple attempts on same puzzle
    
    -- Rating impact
    rating_before INTEGER NOT NULL,
    rating_after INTEGER NOT NULL,
    rating_change INTEGER GENERATED ALWAYS AS (rating_after - rating_before) STORED,
    
    -- Timestamp
    attempted_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id),
    CHECK (time_taken > 0),
    CHECK (hints_used >= 0),
    CHECK (attempt_number >= 1),
    CHECK (rating_before BETWEEN 400 AND 3000),
    CHECK (rating_after BETWEEN 400 AND 3000)
);
```

### Anti-Redundancy Rules
- **Puzzle metadata in puzzles table only** - No duplicate difficulty/theme storage
- **User preferences eliminated** - Puzzle difficulty determined by user rating
- **Source attribution centralized** - All legal info in puzzle_sources

---

## System 4: Content System

### Purpose
Educational content and user progress tracking.

### Tables

#### `content`
**Purpose:** All educational material (tutorials, lessons, courses)
```sql
CREATE TABLE content (
    id VARCHAR(36) PRIMARY KEY,
    
    -- Content identification
    title VARCHAR(200) NOT NULL,
    content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('tutorial', 'lesson', 'course', 'exercise')),
    
    -- Hierarchical structure
    parent_id VARCHAR(36), -- NULL for top-level content
    order_index INTEGER DEFAULT 0, -- Order within parent
    
    -- Content data
    description TEXT,
    content_body JSONB NOT NULL, -- Flexible content structure
    -- Example: {"sections": [{"type": "text", "content": "..."}, {"type": "position", "fen": "..."}]}
    
    -- Metadata
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    estimated_duration INTEGER, -- minutes
    category VARCHAR(50), -- "tactics", "endgames", "openings", "strategy"
    
    -- Learning objectives
    objectives JSONB, -- ["Learn basic tactics", "Understand pin patterns"]
    prerequisites JSONB, -- [{"content_id": "...", "required": true}]
    
    -- Status
    is_published BOOLEAN DEFAULT TRUE,
    version INTEGER DEFAULT 1,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (parent_id) REFERENCES content(id) ON DELETE CASCADE,
    CHECK (order_index >= 0),
    CHECK (estimated_duration IS NULL OR estimated_duration > 0)
);
```

#### `user_content_progress`
**Purpose:** User progress through educational content
```sql
CREATE TABLE user_content_progress (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    content_id VARCHAR(36) NOT NULL,
    
    -- Progress data
    status VARCHAR(20) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    progress_percentage DECIMAL(5,2) DEFAULT 0.00 CHECK (progress_percentage BETWEEN 0.00 AND 100.00),
    
    -- Performance metrics
    time_spent INTEGER DEFAULT 0, -- total minutes
    completion_score DECIMAL(5,2), -- 0.00 to 100.00, NULL if not applicable
    
    -- Milestones
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    last_accessed TIMESTAMP,
    
    -- Metadata
    notes TEXT, -- User's personal notes
    bookmarked BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    UNIQUE(user_id, content_id),
    CHECK (time_spent >= 0),
    CHECK (completion_score IS NULL OR (completion_score >= 0.00 AND completion_score <= 100.00)),
    CHECK (completed_at IS NULL OR completed_at >= started_at)
);
```

### Anti-Redundancy Rules
- **Single content table** - No separate tutorial/lesson/course tables
- **Hierarchical relationships** - Parent/child structure handles complexity
- **Progress isolation** - No progress data mixed with content definitions

---

## System 5: Achievements System

### Purpose
Gamification and user engagement tracking.

### Tables

#### `achievements`
**Purpose:** Achievement definitions and requirements
```sql
CREATE TABLE achievements (
    id VARCHAR(36) PRIMARY KEY,
    
    -- Achievement identification
    key VARCHAR(50) NOT NULL UNIQUE, -- "first_win", "puzzle_streak_10", "rating_1500"
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    
    -- Categorization
    category VARCHAR(30) NOT NULL, -- "games", "puzzles", "rating", "learning", "social"
    tier VARCHAR(20) DEFAULT 'bronze' CHECK (tier IN ('bronze', 'silver', 'gold', 'platinum')),
    
    -- Requirements (flexible JSON structure)
    requirements JSONB NOT NULL,
    -- Examples:
    -- {"type": "game_wins", "count": 1}
    -- {"type": "puzzle_streak", "count": 10}
    -- {"type": "rating_threshold", "rating": 1500, "rating_type": "chess"}
    
    -- Rewards
    points INTEGER DEFAULT 0,
    badge_icon VARCHAR(100), -- Icon file name or URL
    
    -- Metadata
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard', 'legendary')),
    is_secret BOOLEAN DEFAULT FALSE, -- Hidden until unlocked
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CHECK (points >= 0)
);
```

#### `user_achievements`
**Purpose:** User achievement unlocks and progress
```sql
CREATE TABLE user_achievements (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    achievement_id VARCHAR(36) NOT NULL,
    
    -- Progress tracking
    current_progress INTEGER DEFAULT 0,
    target_progress INTEGER NOT NULL,
    progress_percentage DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN target_progress = 0 THEN 100.00
            ELSE LEAST(100.00, (current_progress * 100.0) / target_progress)
        END
    ) STORED,
    
    -- Status
    is_completed BOOLEAN DEFAULT FALSE,
    is_notified BOOLEAN DEFAULT FALSE, -- Whether user has been notified of completion
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
    UNIQUE(user_id, achievement_id),
    CHECK (current_progress >= 0),
    CHECK (target_progress > 0),
    CHECK (current_progress <= target_progress OR is_completed = TRUE),
    CHECK (completed_at IS NULL OR completed_at >= started_at),
    CHECK (is_completed = (current_progress >= target_progress))
);
```

### Anti-Redundancy Rules
- **No achievement data in user table** - Achievements tracked separately
- **Flexible requirements** - JSON structure handles various achievement types
- **Progress calculation** - Computed columns prevent inconsistency

---

## Cross-System Data Flow

### User Registration Flow
1. Create record in `users` (User System)
2. Create record in `user_profiles` (User System)
3. Initialize achievement progress in `user_achievements` (Achievements System)

### Game Completion Flow
1. Update `games` table with result (Games System)
2. Update user stats in `users` table (User System)
3. Update achievement progress in `user_achievements` (Achievements System)

### Content Progress Flow
1. Track progress in `user_content_progress` (Content System)
2. Update related achievements in `user_achievements` (Achievements System)

## Indexing Strategy

### User System
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_user_sessions_user_expires ON user_sessions(user_id, expires_at);
```

### Games System
```sql
CREATE INDEX idx_games_user_completed ON games(white_player_id, completed_at DESC);
CREATE INDEX idx_games_opening ON games(opening_eco);
CREATE INDEX idx_historic_games_players ON historic_games(white_player, black_player);
```

### Puzzles System
```sql
CREATE INDEX idx_puzzles_rating_themes ON puzzles(rating, themes);
CREATE INDEX idx_puzzle_attempts_user_date ON puzzle_attempts(user_id, attempted_at DESC);
```

### Content System
```sql
CREATE INDEX idx_content_type_published ON content(content_type, is_published);
CREATE INDEX idx_content_parent_order ON content(parent_id, order_index);
CREATE INDEX idx_user_progress_user_status ON user_content_progress(user_id, status);
```

### Achievements System
```sql
CREATE INDEX idx_achievements_category ON achievements(category, is_active);
CREATE INDEX idx_user_achievements_user_completed ON user_achievements(user_id, is_completed);
```

---

**Total Tables:** 13  
**Total Indexes:** 15  
**Eliminated Redundancy:** 66% reduction from original 35 tables  

**Next Document:** 02_migration_strategy.md