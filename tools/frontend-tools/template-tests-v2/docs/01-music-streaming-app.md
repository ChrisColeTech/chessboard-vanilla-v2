# 01 - Music Streaming App MVP

## Implementation Plan

### Phase 1: Base Application Setup
This app uses the shared base React Vite application with all required dependencies:

1. **Base App Foundation** from `/mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2/base-app`
   - Vanilla React + Vite + TypeScript
   - Tailwind CSS 3.x
   - HeadlessUI components
   - Lucide React icons
   - React Icons library

2. **Music App Setup** - Copy base app structure (excluding src) to create music-app directory

3. **Page Generation** - Use template-based generator to create complete music streaming structure

### Phase 2: Music App Generation
Use the template-based generator to create the complete music streaming app structure on top of the base app foundation.

## App Vision
A clean, modern music streaming app with focus on discovery and playlists. Think "Spotify simplified" with beautiful album art, smooth playback controls, and personalized recommendations.

## What Makes This Special
- **Visual-first design** - Large album artwork and artist photos
- **Smart playlists** - Auto-generated based on mood, genre, activity
- **Social sharing** - Share songs and playlists easily
- **Offline-ready** - Download songs for offline listening simulation

## Parent Pages & Children

### 1. **Discover** Parent
**Purpose**: Find new music and trending content

#### **Trending** Child Page
- **Hero Section**: Large featured album/song of the day
- **Charts Section**:
  - Top 50 global songs list
  - Song cards with: album art, title, artist, play button, heart icon
  - Chart position numbers (1, 2, 3...)
  - Play count and trending indicator
- **New Releases Grid**:
  - Album covers with release date badges
  - Artist name and album title
  - "New" badge for recent releases
  - Quick play button overlay on hover
- **Viral Tracks Section**:
  - Horizontal scrollable list
  - Songs going viral on social platforms
  - Social media engagement metrics
- **Genre Charts Tabs**:
  - Pop, Hip-Hop, Rock, Electronic, Country
  - Mini charts for each genre (top 10)
- **Weekly Playlist**:
  - Auto-generated trending playlist
  - Play all button
  - Add to library option

#### **Genres** Child Page
- **Genre Grid**: Large colorful cards for each genre
  - Rock, Hip-Hop, Pop, Electronic, Jazz, Classical, Country, R&B
  - Background gradient matching genre vibe
  - Representative artist photos
  - Song count for each genre
- **Genre Detail View** (when genre clicked):
  - Top artists in genre
  - Popular albums grid
  - Playlist recommendations
  - Subgenre tags (Indie Rock, Trap, etc.)
  - Mood-based playlists (Chill Hip-Hop, Workout Rock)
- **Featured Playlists**:
  - Curated genre playlists
  - "Best of [Genre] 2024"
  - Mood-based collections
- **Rising Artists Section**:
  - New artists in each genre
  - "Artists to Watch" carousel

### 2. **Library** Parent
**Purpose**: Personal music collection and playlists

#### **Playlists** Child Page
- **Create Playlist Button**: Large, prominent at top
- **Recently Played Section**:
  - Horizontal scroll of recent albums/playlists
  - Continue listening from where left off
- **Your Playlists Grid**:
  - User-created playlists with custom covers
  - Song count and total duration
  - Last updated date
  - Play, edit, and share options
- **Liked Songs Playlist**:
  - Special playlist for all hearted songs
  - Heart icon and song count
  - Quick access to all favorites
- **Playlist Creation Modal**:
  - Name input
  - Description text area
  - Cover photo upload/selection
  - Privacy settings (public/private)
- **Playlist Edit Mode**:
  - Drag and drop reordering
  - Remove songs with swipe
  - Add songs search interface
  - Bulk select and delete

#### **Downloads** Child Page
- **Download Status Bar**:
  - Total downloaded storage used
  - Available space remaining
  - Download quality settings
- **Downloaded Albums/Playlists**:
  - Grid view of offline content
  - Download date and size
  - Remove download option
  - Storage usage per item
- **Recently Played Section**:
  - Last 20 played songs
  - Play again buttons
  - Add to playlist options
- **Smart Downloads**:
  - Auto-download based on listening habits
  - Weekly discovery download
  - Toggle auto-download settings
- **Download Queue**:
  - Currently downloading items
  - Progress bars
  - Pause/cancel options
- **Download History**:
  - Previously downloaded but removed items
  - Re-download options

### 3. **Search** Parent
**Purpose**: Find specific songs, artists, albums

#### **Songs** Child Page
- **Search Bar**: Large, prominent with voice search option
- **Search Suggestions**: Auto-complete as user types
- **Recent Searches**: Quick access to previous searches
- **Search Results List**:
  - Song title, artist, album
  - Album artwork thumbnail
  - Duration
  - Play button
  - Add to playlist button
  - Heart/favorite button
  - Share button
- **Filter Options**:
  - By genre, release year, duration
  - Explicit content filter
  - Audio quality filter
- **Sort Options**:
  - Relevance, popularity, release date
  - Alphabetical by title/artist
- **Advanced Search**:
  - Search by lyrics
  - Search by mood/tempo
  - Search by decade

#### **Artists** Child Page
- **Artist Search Results**:
  - Artist photo, name, follower count
  - Top songs preview
  - Follow/unfollow button
  - Play top songs button
- **Artist Detail Page**:
  - Large header with artist photo
  - Bio and stats (monthly listeners)
  - Top 5 songs with play buttons
  - Albums discography grid
  - Similar artists section
  - Artist radio playlist
- **Follow System**:
  - Follow/unfollow artists
  - New release notifications
  - Artist activity feed
- **Concert Info**:
  - Upcoming tour dates
  - Ticket purchase links
  - Venue information

### 4. **Profile** Parent
**Purpose**: User account and listening habits

#### **Stats** Child Page
- **Listening Overview Card**:
  - Total hours listened this month
  - Songs discovered
  - Artists followed
  - Playlists created
- **Top Artists Section**:
  - Your most played artists (top 10)
  - Play time per artist
  - Artist photos and names
  - Percentage of total listening
- **Top Songs Section**:
  - Your most played tracks
  - Play count for each song
  - Quick play buttons
- **Genre Distribution**:
  - Pie chart of listening by genre
  - Percentage breakdown
  - Mood analysis (happy, energetic, chill)
- **Listening Habits**:
  - Most active listening hours
  - Peak listening days
  - Average session length
- **Year in Review**:
  - Annual summary statistics
  - Top songs/artists of the year
  - Musical journey timeline

#### **Settings** Child Page
- **Account Information**:
  - Profile photo upload
  - Display name editing
  - Email and password change
  - Subscription status
- **Audio Settings**:
  - Streaming quality (Low, Normal, High, Lossless)
  - Download quality settings
  - Crossfade duration
  - Volume normalization toggle
- **Notification Preferences**:
  - New releases from followed artists
  - Playlist recommendations
  - Social activity notifications
  - Email newsletter subscription
- **Privacy Settings**:
  - Make listening activity public/private
  - Allow friend requests
  - Show in search results
  - Data sharing preferences
- **Connected Accounts**:
  - Link social media accounts
  - Connect to last.fm
  - Import playlists from other services
- **Playback Settings**:
  - Autoplay similar songs
  - Shuffle by default
  - Show explicit content
  - Offline mode preferences

## Theme & Layout System

### Azure Theme
This app uses the **Azure** theme from the professional themes collection, providing a clean, modern music streaming aesthetic.

**Theme Variables (Azure):**
```css
/* Azure Theme Variables */
--primary: #0ea5e9;           /* Sky blue primary */
--accent: #0ea5e9;            /* Sky blue accent */
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
- **Discover** - Music note icon (Trending, Genres)
- **Library** - Collection icon (Playlists, Downloads) 
- **Search** - Search icon (Songs, Artists)
- **Profile** - User icon (Stats, Settings)

### Layout Templates

#### Desktop Pages (ChessboardLayout)
5-panel design for comprehensive music browsing:
```jsx
<ChessboardLayout
  topLeft={<div className="music-actions">Quick Actions</div>}
  top={<div className="music-navigation">Search/Navigation</div>}
  topRight={<div className="music-player-controls">Player Controls</div>}
  left={<div className="music-sidebar">Playlists/Filters</div>}
  center={<div className="music-content">Main Content</div>}
  right={<div className="music-details">Track/Artist Info</div>}
  bottomLeft={<div className="music-queue">Queue/History</div>}
  bottom={<div className="music-progress">Progress/Status</div>}
  bottomRight={<div className="music-social">Share/Social</div>}
/>
```

#### Mobile Pages (MobileChessboardLayout)
3-panel design optimized for touch:
```jsx
<MobileChessboardLayout
  topPieces={<div className="music-mobile-header">Player/Search</div>}
  center={<div className="music-mobile-content">Main Content</div>}
  bottomPieces={<div className="music-mobile-actions">Controls/Actions</div>}
/>
```

### Custom Component Classes

**⚠️ IMPORTANT**: After app generation, add these NEW custom classes to the generated `music-app/src/index.css` file:
- **Use ONLY existing theme variables** (--primary, --accent, --surface, etc.) from professional themes
- **Use standard Tailwind classes** that reference theme variables
- **NO hardcoded colors** - only theme-aware classes  
- **Templates are NEVER modified** - only the generated app's CSS

Add these NEW classes to the generated `music-app/src/index.css`:

```css
/* Music App Component Classes */
.music-card {
  @apply bg-surface/80 backdrop-blur-sm border border-outline/20 rounded-lg p-4;
  @apply hover:bg-surface-variant/60 transition-all duration-200;
}

.music-player-bar {
  @apply bg-surface/90 backdrop-blur-md border-t border-outline/20;
  @apply flex items-center justify-between p-4 sticky bottom-0;
}

.music-album-art {
  @apply rounded-lg shadow-lg overflow-hidden aspect-square;
  @apply hover:shadow-xl hover:scale-105 transition-all duration-300;
}

.music-track-item {
  @apply flex items-center gap-3 p-3 rounded-lg;
  @apply hover:bg-surface-variant/40 cursor-pointer group;
}

.music-genre-card {
  @apply bg-gradient-to-br from-primary/20 to-accent/20;
  @apply border border-primary/30 rounded-xl p-6 text-center;
  @apply hover:from-primary/30 hover:to-accent/30 transition-all duration-300;
}

.music-playlist-cover {
  @apply aspect-square rounded-lg bg-gradient-to-br from-primary/10 to-accent/10;
  @apply border border-outline/20 flex items-center justify-center;
}

.music-search-bar {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/30 rounded-full;
  @apply px-4 py-2 w-full focus-within:border-primary/50 transition-colors;
}

.music-stats-card {
  @apply bg-surface/60 backdrop-blur-sm border border-outline/20 rounded-xl p-6;
  @apply text-center space-y-2;
}
```

### ASCII Mockups

#### Desktop Layout (ChessboardLayout)
```
┌─────────────────────────────────────────────────────────────────┐
│                     Music Streaming App                        │
├─────────┬─────────────────────────┬─────────────────────────────┤
│ Quick   │   Search/Navigation     │    Player Controls          │
│ Actions │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│         │                         │                             │
│Playlists│                         │    Track/Artist Info        │
│Filters  │     Main Content        │                             │
│         │                         │                             │
│         │                         │                             │
├─────────┼─────────────────────────┼─────────────────────────────┤
│ Queue/  │   Progress/Status       │    Share/Social             │
│ History │                         │                             │
├─────────┴─────────────────────────┴─────────────────────────────┤
│                          TabBar                                 │
│    Discover    Library    Search    Profile                     │
└─────────────────────────────────────────────────────────────────┘
```

#### Mobile Layout (MobileChessboardLayout)
```
┌─────────────────────────────────┐
│        Music Streaming App      │
├─────────────────────────────────┤
│        Player/Search            │
│                                 │
├─────────────────────────────────┤
│                                 │
│                                 │
│        Main Content             │
│                                 │
│                                 │
├─────────────────────────────────┤
│       Controls/Actions          │
│                                 │
├─────────────────────────────────┤
│             TabBar              │
│  Discover Library Search Profile│
└─────────────────────────────────┘
```

## Key Features
- Large, beautiful album art display
- Clean audio player with scrub bar
- Heart/favorite button on every song
- Playlist creation and editing
- Share song links functionality
- Mood-based playlist suggestions
- Artist follow/unfollow system

## Technical Implementation
- Mock audio playback with progress simulation
- Sample music data with album artwork URLs
- Local storage for playlists and favorites
- CSS animations for player controls
- Responsive grid layouts for albums
- Search filtering with instant results

## Demo Highlights
- Smooth audio player with beautiful controls
- Browse trending music with large artwork
- Create and edit playlists with drag-and-drop
- Artist pages with discography
- Personalized listening statistics
- Mobile-friendly swipe gestures

## Mobile Page Variants

Each child page has a corresponding mobile version optimized for touch and smaller screens:

#### **Mobile Trending Page**
- **Vertical Scroll Layout**: Single column for charts and releases
- **Swipe Navigation**: Horizontal swipe through album covers
- **Touch-Optimized Play Buttons**: Large tap targets for play controls
- **Pull-to-Refresh**: Update trending charts with pull gesture
- **Bottom Player Bar**: Persistent mini-player at bottom

#### **Mobile Genres Page**
- **Category Cards**: Full-width genre cards for easy tapping
- **Gesture Navigation**: Swipe between genre details
- **Touch-Friendly Filters**: Large filter buttons and toggles
- **Quick Actions**: Swipe to add to playlist or favorites

#### **Mobile Playlists Page**
- **Grid Layout**: Optimized playlist grid for mobile viewing
- **Swipe Actions**: Swipe to play, edit, or share playlists
- **Touch Creation**: Mobile-optimized playlist creation flow
- **Drag Reorder**: Touch-friendly song reordering in playlists

#### **Mobile Downloads Page**
- **Storage Visualization**: Mobile-friendly storage usage display
- **Swipe Management**: Swipe to delete downloads or manage queue
- **Touch Download**: One-tap download buttons
- **Offline Indicators**: Clear offline availability status

#### **Mobile Songs Search Page**
- **Voice Search**: Large voice search button for mobile
- **Auto-complete**: Mobile keyboard optimized suggestions
- **Filter Slides**: Slide-out filter panels for mobile
- **Touch Results**: Large tap targets for search results

#### **Mobile Artists Search Page**
- **Artist Cards**: Mobile-optimized artist profile cards
- **Follow Actions**: Large follow/unfollow buttons
- **Touch Bio**: Expandable artist bio sections
- **Quick Play**: One-tap artist top songs playback

#### **Mobile Stats Page**
- **Scrollable Charts**: Vertical scroll through listening stats
- **Interactive Graphs**: Touch-friendly chart interactions
- **Share Stats**: Mobile sharing for year-in-review stats
- **Gesture Navigation**: Swipe between different stat views

#### **Mobile Settings Page**
- **Settings Sections**: Collapsible mobile-friendly sections
- **Toggle Controls**: Large toggle switches for mobile
- **Audio Quality**: Mobile-optimized quality selection
- **Account Management**: Touch-friendly account settings

## Implementation Commands

### Phase 1: Setup Music App Directory

```bash
# Copy base app structure (excluding src folder) to music-app
cd /mnt/c/Projects/chessboard-vanilla-v2/tools/frontend-tools/template-tests-v2
mkdir -p music-app
cp -r base-app/{package.json,package-lock.json,vite.config.ts,tsconfig.json,tsconfig.node.json,tailwind.config.js,postcss.config.js,index.html,public} music-app/

# Navigate to music app directory and install dependencies
cd music-app
npm install
cd ..
```

### Phase 2: Generate Music App Pages

```bash
# Navigate to generator directory
cd music-app

# Create parent pages
npm run mobile -- parent Discover
npm run mobile -- parent Library
npm run mobile -- parent Search
npm run mobile -- parent Profile

# Create child pages with mobile variants under Discover parent
npm run mobile -- child Trending --parent discover npm run mobile -- child Genres --parent discover 
# Create child pages with mobile variants under Library parent
npm run mobile -- child Playlists --parent library npm run mobile -- child Downloads --parent library 
# Create child pages with mobile variants under Search parent
npm run mobile -- child Songs --parent search npm run mobile -- child Artists --parent search 
# Create child pages with mobile variants under Profile parent
npm run mobile -- child Stats --parent profile npm run mobile -- child Settings --parent profile ```

## File Structure Tree

```
music-app/
├── src/
│   ├── components/
│   │   ├── discover/
│   │   │   ├── TrendingPageWrapper.tsx
│   │   │   ├── GenresPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── library/
│   │   │   ├── PlaylistsPageWrapper.tsx
│   │   │   ├── DownloadsPageWrapper.tsx
│   │   │   └── index.ts
│   │   ├── search/
│   │   │   ├── SongsPageWrapper.tsx
│   │   │   ├── ArtistsPageWrapper.tsx
│   │   │   └── index.ts
│   │   └── profile/
│   │       ├── StatsPageWrapper.tsx
│   │       ├── SettingsPageWrapper.tsx
│   │       └── index.ts
│   ├── pages/
│   │   ├── discover/
│   │   │   ├── DiscoverPage.tsx
│   │   │   ├── DiscoverMainPage.tsx
│   │   │   ├── TrendingPage.tsx
│   │   │   ├── MobileTrendingPage.tsx
│   │   │   ├── GenresPage.tsx
│   │   │   └── MobileGenresPage.tsx
│   │   ├── library/
│   │   │   ├── LibraryPage.tsx
│   │   │   ├── LibraryMainPage.tsx
│   │   │   ├── PlaylistsPage.tsx
│   │   │   ├── MobilePlaylistsPage.tsx
│   │   │   ├── DownloadsPage.tsx
│   │   │   └── MobileDownloadsPage.tsx
│   │   ├── search/
│   │   │   ├── SearchPage.tsx
│   │   │   ├── SearchMainPage.tsx
│   │   │   ├── SongsPage.tsx
│   │   │   ├── MobileSongsPage.tsx
│   │   │   ├── ArtistsPage.tsx
│   │   │   └── MobileArtistsPage.tsx
│   │   └── profile/
│   │       ├── ProfilePage.tsx
│   │       ├── ProfileMainPage.tsx
│   │       ├── StatsPage.tsx
│   │       ├── MobileStatsPage.tsx
│   │       ├── SettingsPage.tsx
│   │       └── MobileSettingsPage.tsx
│   ├── hooks/
│   │   ├── discover/
│   │   │   └── useDiscoverActions.ts
│   │   ├── library/
│   │   │   └── useLibraryActions.ts
│   │   ├── search/
│   │   │   └── useSearchActions.ts
│   │   └── profile/
│   │       └── useProfileActions.ts
│   ├── services/
│   │   ├── api/
│   │   │   ├── musicApi.ts
│   │   │   ├── playlistApi.ts
│   │   │   ├── searchApi.ts
│   │   │   └── userApi.ts
│   │   └── instructions/
│   │       └── pages/
│   │           ├── discover.ts
│   │           ├── library.ts
│   │           ├── search.ts
│   │           └── profile.ts
│   ├── constants/
│   │   └── actions/
│   │       └── pages/
│   │           ├── discover.ts
│   │           ├── library.ts
│   │           ├── search.ts
│   │           └── profile.ts
│   └── types/
│       ├── music.ts
│       ├── playlist.ts
│       ├── user.ts
│       └── search.ts
```

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    profile_image_url VARCHAR(500),
    subscription_type VARCHAR(20) DEFAULT 'free', -- free, premium
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Artists table
CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    image_url VARCHAR(500),
    genres TEXT[],
    monthly_listeners INTEGER DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Albums table
CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES artists(id),
    cover_image_url VARCHAR(500),
    release_date DATE,
    total_tracks INTEGER DEFAULT 0,
    duration_seconds INTEGER DEFAULT 0,
    genre VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Songs table
CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER REFERENCES artists(id),
    album_id INTEGER REFERENCES albums(id),
    duration_seconds INTEGER NOT NULL,
    file_url VARCHAR(500),
    preview_url VARCHAR(500),
    lyrics TEXT,
    explicit BOOLEAN DEFAULT FALSE,
    track_number INTEGER,
    play_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Playlists table
CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    cover_image_url VARCHAR(500),
    is_public BOOLEAN DEFAULT TRUE,
    total_tracks INTEGER DEFAULT 0,
    total_duration INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Playlist songs junction table
CREATE TABLE playlist_songs (
    id SERIAL PRIMARY KEY,
    playlist_id INTEGER REFERENCES playlists(id),
    song_id INTEGER REFERENCES songs(id),
    position INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(playlist_id, song_id)
);

-- User listening history
CREATE TABLE listening_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    song_id INTEGER REFERENCES songs(id),
    played_at TIMESTAMP DEFAULT NOW(),
    duration_played INTEGER, -- seconds played
    completed BOOLEAN DEFAULT FALSE -- if user played full song
);

-- User favorites (liked songs)
CREATE TABLE user_favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    song_id INTEGER REFERENCES songs(id),
    liked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, song_id)
);

-- User follows (followed artists)
CREATE TABLE user_follows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    artist_id INTEGER REFERENCES artists(id),
    followed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, artist_id)
);

-- Downloads table (for offline listening)
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    song_id INTEGER REFERENCES songs(id),
    quality VARCHAR(20) DEFAULT 'normal', -- low, normal, high
    file_size INTEGER, -- bytes
    downloaded_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, song_id)
);

-- User preferences
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    streaming_quality VARCHAR(20) DEFAULT 'normal',
    download_quality VARCHAR(20) DEFAULT 'normal',
    crossfade_duration INTEGER DEFAULT 0, -- seconds
    volume_normalization BOOLEAN DEFAULT TRUE,
    autoplay_enabled BOOLEAN DEFAULT TRUE,
    explicit_content_filter BOOLEAN DEFAULT FALSE,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Routes

### Authentication Routes
```
POST   /api/auth/register        # User registration
POST   /api/auth/login           # User login
POST   /api/auth/logout          # User logout
POST   /api/auth/refresh         # Refresh access token
```

### Music Discovery Routes (Discover Pages)
```
GET    /api/discover/trending    # Get trending songs and charts
GET    /api/discover/new-releases # Get new album releases
GET    /api/discover/genres      # Get all music genres
GET    /api/discover/genre/:id   # Get songs by genre
GET    /api/discover/featured    # Get featured playlists
```

### Library Routes (Library Pages)
```
GET    /api/library/playlists    # Get user's playlists
POST   /api/library/playlists    # Create new playlist
PUT    /api/library/playlists/:id # Update playlist
DELETE /api/library/playlists/:id # Delete playlist
GET    /api/library/downloads    # Get downloaded songs
POST   /api/library/downloads    # Download song for offline
DELETE /api/library/downloads/:id # Remove download
GET    /api/library/recent       # Get recently played songs
```

### Search Routes (Search Pages)
```
GET    /api/search/songs         # Search songs
GET    /api/search/artists       # Search artists
GET    /api/search/albums        # Search albums
GET    /api/search/playlists     # Search public playlists
GET    /api/search/suggestions   # Get search suggestions
```

### Music Playback Routes
```
GET    /api/songs/:id            # Get song details
POST   /api/songs/:id/play       # Log song play (analytics)
GET    /api/songs/:id/lyrics     # Get song lyrics
POST   /api/songs/:id/favorite   # Add to favorites
DELETE /api/songs/:id/favorite   # Remove from favorites
```

### Artist Routes
```
GET    /api/artists/:id          # Get artist details
GET    /api/artists/:id/songs    # Get artist's songs
GET    /api/artists/:id/albums   # Get artist's albums
POST   /api/artists/:id/follow   # Follow artist
DELETE /api/artists/:id/follow   # Unfollow artist
```

### User Profile Routes (Profile Pages)
```
GET    /api/user/profile         # Get user profile
PUT    /api/user/profile         # Update user profile
GET    /api/user/stats           # Get listening statistics
GET    /api/user/stats/yearly    # Get year in review stats
GET    /api/user/preferences     # Get user preferences
PUT    /api/user/preferences     # Update preferences
GET    /api/user/favorites       # Get favorite songs
GET    /api/user/following       # Get followed artists
```

### Playlist Management Routes
```
GET    /api/playlists/:id        # Get playlist details
POST   /api/playlists/:id/songs  # Add song to playlist
DELETE /api/playlists/:id/songs/:songId # Remove song from playlist
PUT    /api/playlists/:id/reorder # Reorder playlist songs
POST   /api/playlists/:id/follow # Follow public playlist
```