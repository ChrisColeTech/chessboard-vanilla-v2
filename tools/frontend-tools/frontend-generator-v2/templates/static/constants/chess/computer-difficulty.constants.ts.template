// computer-difficulty.constants.ts - Computer difficulty level configurations
// Phase 2: Utilities & Constants - Difficulty configurations

import type { ComputerDifficulty, ComputerOpponentConfig } from '../../types';

/**
 * Complete difficulty configuration mapping from user-friendly 1-10 scale
 * to Stockfish's internal 0-20 skill level scale with appropriate time limits
 * 
 * Design principles:
 * - User scale 1-10 is intuitive and matches common game difficulty systems
 * - Stockfish skill levels are mapped to provide meaningful strength differences
 * - Time limits increase with difficulty for more realistic behavior
 * - Each level provides a noticeable but not overwhelming difficulty increase
 */
export const DIFFICULTY_CONFIGS: Record<ComputerDifficulty, ComputerOpponentConfig> = {
  // Beginner levels - Learning the rules
  1: { 
    difficulty: 1, 
    timeLimit: 500,      // 0.5 seconds - very quick moves
    skillLevel: 0,       // Weakest Stockfish setting
    searchDepth: 1       // Very shallow search
  },
  2: { 
    difficulty: 2, 
    timeLimit: 600,      // 0.6 seconds
    skillLevel: 2,       // Still very weak but slightly better
    searchDepth: 2
  },
  
  // Casual levels - Playing for fun
  3: { 
    difficulty: 3, 
    timeLimit: 700,      // 0.7 seconds
    skillLevel: 4,       // Casual player strength
    searchDepth: 3
  },
  4: { 
    difficulty: 4, 
    timeLimit: 800,      // 0.8 seconds
    skillLevel: 6,       // Improved casual player
    searchDepth: 4
  },
  
  // Club player levels - Regular players
  5: { 
    difficulty: 5, 
    timeLimit: 1000,     // 1 second - standard thinking time
    skillLevel: 8,       // Club player strength
    searchDepth: 5
  },
  6: { 
    difficulty: 6, 
    timeLimit: 1200,     // 1.2 seconds
    skillLevel: 10,      // Strong club player
    searchDepth: 6
  },
  
  // Strong player levels - Quite good
  7: { 
    difficulty: 7, 
    timeLimit: 1400,     // 1.4 seconds
    skillLevel: 12,      // Strong player
    searchDepth: 7
  },
  8: { 
    difficulty: 8, 
    timeLimit: 1600,     // 1.6 seconds
    skillLevel: 14,      // Very strong player
    searchDepth: 8
  },
  
  // Expert levels - Very strong
  9: { 
    difficulty: 9, 
    timeLimit: 1800,     // 1.8 seconds
    skillLevel: 16,      // Expert level
    searchDepth: 9
  },
  10: { 
    difficulty: 10, 
    timeLimit: 2000,     // 2 seconds - maximum thinking time
    skillLevel: 18,      // Near-master strength (not quite max to avoid perfect play)
    searchDepth: 10
  }
};

/**
 * Human-readable descriptions for each difficulty level
 * These descriptions help users understand what they're choosing
 */
export const DIFFICULTY_DESCRIPTIONS: Record<ComputerDifficulty, string> = {
  1: "Beginner (learning the rules)",
  2: "Beginner+ (making basic moves)",
  3: "Casual player (plays for fun)",  
  4: "Casual+ (knows basic tactics)",
  5: "Club player (plays regularly)",
  6: "Strong club player (quite good)",
  7: "Tournament player (competitive)",
  8: "Strong tournament player (very good)",
  9: "Expert level (very strong)",
  10: "Master level (extremely strong)"
};

/**
 * Skill level categories for grouping difficulties
 */
export const SKILL_CATEGORIES = {
  BEGINNER: [1, 2] as ComputerDifficulty[],
  CASUAL: [3, 4] as ComputerDifficulty[],
  CLUB: [5, 6] as ComputerDifficulty[],
  STRONG: [7, 8] as ComputerDifficulty[],
  EXPERT: [9, 10] as ComputerDifficulty[]
} as const;

/**
 * Get difficulty configuration for a specific level
 * @param level Difficulty level (1-10)
 * @returns Configuration object for the level
 * @throws Error if level is invalid
 */
export const getDifficultyConfig = (level: ComputerDifficulty): ComputerOpponentConfig => {
  const config = DIFFICULTY_CONFIGS[level];
  
  if (!config) {
    throw new Error(`Invalid difficulty level: ${level}. Must be between 1 and 10.`);
  }
  
  return { ...config }; // Return a copy to prevent mutation
};

/**
 * Get human-readable description for a difficulty level
 * @param level Difficulty level (1-10)
 * @returns Human-readable description
 */
export const getDifficultyDescription = (level: ComputerDifficulty): string => {
  const description = DIFFICULTY_DESCRIPTIONS[level];
  
  if (!description) {
    return `Level ${level}`;
  }
  
  return description;
};

/**
 * Get the skill category for a difficulty level
 * @param level Difficulty level (1-10)  
 * @returns Skill category name
 */
export const getSkillCategory = (level: ComputerDifficulty): keyof typeof SKILL_CATEGORIES => {
  if (SKILL_CATEGORIES.BEGINNER.includes(level)) return 'BEGINNER';
  if (SKILL_CATEGORIES.CASUAL.includes(level)) return 'CASUAL';
  if (SKILL_CATEGORIES.CLUB.includes(level)) return 'CLUB';
  if (SKILL_CATEGORIES.STRONG.includes(level)) return 'STRONG';
  if (SKILL_CATEGORIES.EXPERT.includes(level)) return 'EXPERT';
  
  // Fallback (shouldn't happen with valid levels)
  return 'CLUB';
};

/**
 * Get all available difficulty levels
 * @returns Array of all valid difficulty levels
 */
export const getAllDifficultyLevels = (): ComputerDifficulty[] => {
  return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
};

/**
 * Validate a difficulty level
 * @param level Level to validate
 * @returns True if level is valid
 */
export const isValidDifficultyLevel = (level: number): level is ComputerDifficulty => {
  return Number.isInteger(level) && level >= 1 && level <= 10;
};

/**
 * Get the default difficulty level for new games
 */
export const DEFAULT_DIFFICULTY: ComputerDifficulty = 5;

/**
 * Recommended difficulty levels for different player types
 */
export const RECOMMENDED_DIFFICULTIES = {
  NEW_PLAYER: 1,
  LEARNING: 2,
  CASUAL: 3,
  IMPROVING: 5,
  EXPERIENCED: 7,
  STRONG: 9
} as const;

/**
 * Convert Stockfish skill level (0-20) back to user difficulty level (1-10)
 * This is useful for reverse lookups
 * @param stockfishLevel Stockfish skill level (0-20)
 * @returns User difficulty level (1-10)
 */
export const stockfishLevelToUserDifficulty = (stockfishLevel: number): ComputerDifficulty => {
  // Find the difficulty level that matches this Stockfish level
  for (const [userLevel, config] of Object.entries(DIFFICULTY_CONFIGS)) {
    if (config.skillLevel === stockfishLevel) {
      return parseInt(userLevel) as ComputerDifficulty;
    }
  }
  
  // If no exact match, find the closest one
  let closest: ComputerDifficulty = 5;
  let minDifference = Math.abs(DIFFICULTY_CONFIGS[5].skillLevel - stockfishLevel);
  
  for (const [userLevel, config] of Object.entries(DIFFICULTY_CONFIGS)) {
    const difference = Math.abs(config.skillLevel - stockfishLevel);
    if (difference < minDifference) {
      minDifference = difference;
      closest = parseInt(userLevel) as ComputerDifficulty;
    }
  }
  
  return closest;
};