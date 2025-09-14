# Backend Systems Proposal

**Document Version:** 1.0  
**Date:** September 2025  
**Status:** PROPOSAL - Database Schema Refactoring  
**Target:** Eliminate redundancy and normalize current 35-table mess

## Overview

The current backend database has grown from a planned 8-table design to 35+ tables with significant redundancy and unused features. This proposal defines 5 core systems with 12 normalized tables to replace the current architecture.

## Current State Analysis

- **Current Tables:** 35 active tables (46 including backups)
- **Original Design:** 8 tables
- **Problem:** Over-engineering, scope creep, redundant functionality
- **Solution:** System-based organization with strict boundaries

## Proposed System Architecture

### 1. User System
**Purpose:** Authentication, profiles, and session management

**Tables:**
- `users` - Core authentication + chess ratings
- `user_profiles` - Display preferences and social data  
- `user_sessions` - Login session tracking

**Consolidates:** Currently scattered across multiple user-related tables

### 2. Games System
**Purpose:** Chess gameplay and game reference data

**Tables:**
- `games` - User gameplay sessions vs AI
- `historic_games` - Famous master games for study
- `openings` - Chess opening reference database

**Eliminates:** Redundant game analysis and review tables

### 3. Puzzles System  
**Purpose:** Tactical training and puzzle management

**Tables:**
- `puzzles` - Individual tactical problems
- `puzzle_sources` - Source collections (Lichess, Chess.com, etc.)
- `puzzle_attempts` - User solving history and performance

**Consolidates:** Puzzle preferences into user system

### 4. Content System
**Purpose:** Educational content and user progress

**Tables:**
- `content` - All educational material (tutorials, lessons, courses)
- `user_content_progress` - User progress through educational content

**Replaces:** 
- `tutorials` (29 records)
- `learning_modules` (2 records) 
- `learning_paths` (33 records)
- `tutorial_steps` (0 records)
- `user_study_plans` (47 records)
- `user_learning_paths` (43 records)
- `user_progress_tracking` (0 records)

### 5. Achievements System
**Purpose:** Gamification and user engagement

**Tables:**
- `achievements` - Achievement definitions
- `user_achievements` - User achievement unlocks

**Normalizes:** Currently mixed between table storage and JSON fields

## System Boundaries

### What Gets Eliminated
**Empty/Unused Tables (0 records):**
- `game_reviews`
- `puzzle_attempts` (will be recreated)
- `opening_moves`
- `tutorial_steps`  
- `user_achievements` (will be recreated)
- `user_analytics`
- `user_progress_tracking`
- `user_puzzle_preferences`

**Redundant Tables:**
- Multiple learning content tables → Single `content` table
- Multiple progress tracking tables → Single `user_content_progress` table
- Settings scattered across tables → Consolidated in user system

**Scope Creep:**
- `subscriptions` - Business feature, not core chess
- `help_content` - Support docs, separate system
- `analysis_positions` - Advanced feature, not MVP
- `endgame_positions` - Can be content entries
- `ai_opponents` - Data should be in games table
- `user_settings` - Belongs in user_profiles

## Implementation Benefits

### Clarity
- Each system has a clear, single responsibility
- Table names clearly indicate their system
- No overlap between systems

### Maintainability  
- Changes isolated to specific systems
- Easier to understand and modify
- Clear ownership of functionality

### Performance
- Fewer tables to join across
- Eliminated unused indexes and constraints
- Reduced query complexity

### Data Integrity
- Proper foreign key relationships
- No duplicate data storage
- Consistent data types and constraints

## Migration Strategy

### Phase 1: Data Consolidation
1. Migrate learning content to unified `content` table
2. Consolidate progress tracking
3. Normalize achievement system

### Phase 2: Table Elimination
1. Drop empty tables
2. Remove redundant tables after data migration
3. Clean up unused indexes

### Phase 3: System Testing
1. Verify all functionality works with new schema
2. Performance testing
3. Data integrity validation

## Proposed Schema Summary

**Total Tables:** 12 (down from 35)
**Systems:** 5 clearly defined systems
**Reduction:** 66% fewer tables

### Final Table List
1. `users`
2. `user_profiles` 
3. `user_sessions`
4. `games`
5. `historic_games`
6. `openings`
7. `puzzles`
8. `puzzle_sources`
9. `puzzle_attempts`
10. `content`
11. `user_content_progress`
12. `achievements`
13. `user_achievements`

## Next Steps

1. **Review and approval** of systems approach
2. **Detailed schema design** for each system  
3. **Migration planning** with data preservation
4. **Implementation timeline** and testing strategy

---

**Status:** AWAITING APPROVAL  
**Risk Level:** Medium - Requires careful data migration  
**Benefit:** High - Dramatic simplification of architecture