# Chess Training Frontend API Integration Plan

## Overview
This document outlines the comprehensive plan to replace all mock data in the frontend with real API calls to the backend while following the established SRP (Single Responsibility Principle) architecture patterns.

## Current State Analysis

### Backend API Status
- **Port**: Running on http://localhost:3000
- **Database**: SQLite with 449 records across 28 tables
- **Authentication**: Already integrated with JWT tokens
- **Endpoints**: All API endpoints are functional and tested

### Frontend Mock Data to Replace
Located in `/frontend/src/data/` - 85 files containing mock data that need to be replaced with API calls:
- User profiles and settings
- Puzzle data (tactical, opening, endgame, custom)
- Game history and analysis
- Learning paths and tutorials
- Statistics and progress tracking
- Achievements and gamification
- Opening database
- AI opponents and help content

### Architecture Requirements
All API integration must follow the established SRP patterns where:
- Pages contain ONLY presentation logic
- ALL business logic goes in page-specific hooks
- Components are organized by page, not as generic shared components
- No inline API calls or business logic in page components

## Implementation Strategy

### Phase 1: API Infrastructure Setup
**Goal**: Establish the foundation for all API integration

**Tasks**:
1. Create API client configuration with authentication interceptors
2. Set up error handling and network status management  
3. Configure React Query with proper cache settings
4. Create TypeScript types for all API responses
5. Set up query key factories for cache management

**Files to Create**:
- `services/api/client.ts`
- `services/api/config.ts`
- `services/api/errorHandler.ts`
- `services/api/types/` (folder with all API types)
- `services/api/cache/queryKeys.ts`

**Files to Update**:
- `main.tsx` (React Query configuration)
- Add global error boundary components

### Phase 2: User Profile & Settings Integration
**Goal**: Replace user-related mock data with real API calls

**API Endpoints to Use**:
- `GET /api/user/profile`
- `PUT /api/user/profile`
- `GET /api/user/preferences`
- `PUT /api/user/preferences`
- `GET /api/user/settings`
- `PUT /api/user/settings`

**Tasks**:
1. Create `services/api/endpoints/userApi.ts` with pure API functions
2. Create page-specific hooks:
   - `hooks/profile/useProfilePage.ts`
   - `hooks/profile/useAccountSettingsPage.ts`
   - `hooks/profile/usePreferencesPage.ts`
3. Update corresponding page components to use these hooks
4. Remove mock data imports from user-related components

**Mock Files to Replace**:
- `data/userProfile.ts`
- `data/userSettings.ts`
- `data/userPreferences.ts`
- `data/accountSettings.ts`

### Phase 3: Core Puzzle System Integration
**Goal**: Replace all puzzle-related mock data with API integration

**API Endpoints to Use**:
- `GET /api/puzzles/next`
- `POST /api/puzzles/{id}/solve`
- `GET /api/puzzles/{id}/hint`
- `GET /api/puzzles/categories`
- `GET /api/puzzles/history`
- `POST /api/puzzles/custom`
- `GET /api/puzzles/custom`

**Tasks**:
1. Create `services/api/endpoints/puzzlesApi.ts`
2. Create page-specific puzzle hooks:
   - `hooks/puzzles/useOpeningPuzzlesPage.ts`
   - `hooks/puzzles/useTacticalPuzzlesPage.ts`
   - `hooks/puzzles/useCustomPuzzlesPage.ts`
   - `hooks/puzzles/usePuzzleSelectionPage.ts`
   - `hooks/puzzles/usePuzzleSolvePage.ts`
3. Update puzzle page components to be presentation-only
4. Create page-specific puzzle components in organized folders
5. Implement puzzle solving logic with proper state management

**Mock Files to Replace**:
- `data/tacticalPuzzles.ts`
- `data/openingPuzzles.ts`
- `data/endgamePuzzles.ts`
- `data/customPuzzles.ts`
- `data/puzzleCategories.ts`
- `data/puzzleSourceDatabase.ts`
- `data/userPuzzleSelections.ts`
- `data/userPuzzleSessions.ts`
- `data/userPuzzleStats.ts`

### Phase 4: Games & Analysis Integration
**Goal**: Replace game history and analysis mock data with API calls

**API Endpoints to Use**:
- `GET /api/games`
- `GET /api/games/{id}`
- `POST /api/games`
- `PUT /api/games/{id}`
- `POST /api/games/{id}/analyze`
- `GET /api/games/{id}/analysis`
- `GET /api/games/reviews`

**Tasks**:
1. Create `services/api/endpoints/gamesApi.ts`
2. Create page-specific game hooks:
   - `hooks/play/usePlayComputerPage.ts`
   - `hooks/play/useAnalysisBoardPage.ts`
   - `hooks/play/useGameReviewPage.ts`
   - `hooks/games/useGameHistoryPage.ts`
3. Update game-related page components
4. Implement real-time game state management
5. Add game analysis integration

**Mock Files to Replace**:
- `data/historicGames.ts`
- `data/reviewGames.ts`
- `data/gameAnalysis.ts`
- `data/gameReviews.ts`

### Phase 5: Statistics & Progress Tracking
**Goal**: Replace progress and statistics mock data with real analytics

**API Endpoints to Use**:
- `GET /api/stats/overview`
- `GET /api/stats/puzzles`
- `GET /api/stats/games`
- `GET /api/stats/progress`
- `GET /api/stats/performance`
- `GET /api/stats/ratings`

**Tasks**:
1. Create `services/api/endpoints/statsApi.ts`
2. Create statistics page hooks:
   - `hooks/progress/useProgressOverviewPage.ts`
   - `hooks/progress/useStatisticsPage.ts`
   - `hooks/progress/useAnalyticsPage.ts`
3. Update progress tracking components
4. Implement real-time progress updates
5. Add performance metrics visualization

**Mock Files to Replace**:
- `data/userProgress.ts`
- `data/userProgressTracking.ts`
- `data/analyticsData.ts`
- `data/performanceMetrics.ts`
- `data/userAnalysisPreferences.ts`

### Phase 6: Learning System Integration
**Goal**: Replace learning paths and tutorial mock data

**API Endpoints to Use**:
- `GET /api/learning/paths`
- `GET /api/learning/paths/{id}`
- `GET /api/learning/modules`
- `POST /api/learning/paths/{id}/enroll`
- `GET /api/tutorials`
- `POST /api/tutorials/{id}/complete`

**Tasks**:
1. Create `services/api/endpoints/learningApi.ts` and `tutorialsApi.ts`
2. Create learning page hooks:
   - `hooks/learn/useLearningPathsPage.ts`
   - `hooks/learn/useTutorialsPage.ts`
   - `hooks/learn/useLessonsPage.ts`
3. Update learning components with progress tracking
4. Implement course enrollment and completion

**Mock Files to Replace**:
- `data/learningPaths.ts`
- `data/studyPlansDefaults.ts`
- `data/userStudyPlans.ts`
- `data/tutorials.ts`
- `data/lessonsDatabase.ts`

### Phase 7: Remaining Features Integration
**Goal**: Complete integration of all remaining mock data

**API Endpoints to Use**:
- Opening database endpoints
- Achievement system endpoints  
- AI opponents endpoints
- Help content endpoints
- Subscription management endpoints

**Tasks**:
1. Create remaining API endpoint files
2. Create page-specific hooks for:
   - Opening database pages
   - Achievement pages
   - AI opponent pages
   - Help center pages
   - Subscription pages
3. Update all remaining page components
4. Remove all remaining mock data files

**Remaining Mock Files**:
- `data/openingsDatabase.ts`
- `data/achievements.ts`
- `data/aiOpponents.ts`
- `data/helpContent.ts`
- `data/subscriptionData.ts`
- All other remaining mock files

### Phase 8: Testing & Quality Assurance
**Goal**: Ensure all API integration works properly

**Tasks**:
1. Test all API endpoints with real data
2. Verify SRP compliance in all updated components
3. Test error handling and offline scenarios
4. Performance testing and optimization
5. End-to-end testing of user workflows
6. Code review and cleanup

## Implementation Guidelines

### File Organization
```
frontend/src/
├── services/api/          # Pure API functions (no React hooks)
│   ├── endpoints/         # API endpoint functions
│   ├── types/            # TypeScript interfaces
│   └── cache/            # Query key factories
├── hooks/                # Page-specific hooks only
│   ├── puzzles/          # Puzzle page hooks
│   ├── profile/          # Profile page hooks  
│   ├── play/             # Game play hooks
│   └── [other pages]/    # More page-specific hooks
└── components/           # Page-specific components
    ├── puzzles/          # Components for puzzle pages
    ├── profile/          # Components for profile pages
    └── [other pages]/    # More page-specific components
```

### Key Principles
1. **One hook per page** - Each page has exactly one corresponding hook
2. **All business logic in hooks** - Pages are presentation-only
3. **Page-specific components** - No generic shared components
4. **Pure API functions** - Service layer contains no React hooks
5. **Proper error handling** - All API calls have error states
6. **Loading states** - All data fetching shows loading indicators
7. **Cache management** - Proper query invalidation and updates

## Success Criteria
- [ ] All 85 mock data files replaced with API calls
- [ ] All pages follow SRP architecture with page-specific hooks
- [ ] No inline API calls or business logic in page components
- [ ] Comprehensive error handling for all API operations
- [ ] Loading states implemented for all data fetching
- [ ] Performance maintained or improved from mock data
- [ ] User experience unchanged from user perspective
- [ ] All tests pass with real API data

This plan provides a structured approach to replace all mock data with real API integration while maintaining the established architectural patterns and ensuring code quality.