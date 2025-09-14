<<<<<<< Updated upstream
// DifficultySelector.tsx - AI difficulty selection following SRP
// Single Responsibility: Handle computer difficulty level selection

import React from 'react';
import type { ComputerDifficulty } from '../../types';

interface DifficultySelectorProps {
  /** Current difficulty level (1-10) */
  currentLevel: ComputerDifficulty;
  /** Handler for difficulty level change */
  onLevelChange: (level: ComputerDifficulty) => void;
  /** Whether the selector should be disabled */
  disabled?: boolean;
  /** Whether to show expanded view with descriptions */
  showDescriptions?: boolean;
}

const DIFFICULTY_DESCRIPTIONS: Record<ComputerDifficulty, string> = {
  1: 'Beginner',
  2: 'Novice', 
  3: 'Easy',
  4: 'Casual',
  5: 'Medium',
  6: 'Intermediate',
  7: 'Hard',
  8: 'Advanced',
  9: 'Expert',
  10: 'Master'
};

export const DifficultySelector: React.FC<DifficultySelectorProps> = ({
  currentLevel,
  onLevelChange,
  disabled = false,
  showDescriptions = false
}) => {
  const levels: ComputerDifficulty[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  return (
    <div className="bg-card border-b border-border p-2 sm:p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex flex-col gap-2 sm:gap-3">
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm font-medium text-foreground">
              AI Difficulty
            </span>
            {showDescriptions && (
              <span className="text-xs sm:text-sm text-muted-foreground">
                Current: {DIFFICULTY_DESCRIPTIONS[currentLevel]}
              </span>
            )}
          </div>
          
          {/* Mobile-first responsive button grid */}
          <div className="grid grid-cols-5 sm:grid-cols-10 gap-1 sm:gap-2">
            {levels.map(level => (
              <button
                key={level}
                onClick={() => onLevelChange(level)}
                disabled={disabled}
                className={`
                  aspect-square w-full min-w-0 rounded text-xs sm:text-sm font-bold transition-all duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed
                  ${level === currentLevel 
                    ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                    : 'bg-secondary text-secondary-foreground hover:bg-secondary/90 hover:scale-105'
                  }
                  ${!disabled && 'active:scale-95'}
                  focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50
                `}
                title={`${DIFFICULTY_DESCRIPTIONS[level]} (Level ${level})`}
                aria-label={`Set difficulty to level ${level}: ${DIFFICULTY_DESCRIPTIONS[level]}`}
              >
                {level}
              </button>
            ))}
          </div>
          
          {/* Descriptions shown on mobile when space allows */}
          {showDescriptions && (
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-1 text-xs text-muted-foreground mt-1">
              {levels.map((level, index) => (
                <div key={level} className={`text-center ${index >= 5 ? 'block sm:block' : ''}`}>
                  <span className="font-medium">{level}:</span> {DIFFICULTY_DESCRIPTIONS[level]}
                </div>
              ))}
            </div>
          )}
          
          {/* Mobile-friendly current level indicator */}
          <div className="flex justify-center sm:justify-start">
            <span className="text-xs text-foreground bg-muted px-2 py-1 rounded">
              Level {currentLevel}: {DIFFICULTY_DESCRIPTIONS[currentLevel]}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
=======
// DifficultySelector.tsx - AI difficulty selection following SRP
// Single Responsibility: Handle computer difficulty level selection

import React from 'react';
import type { ComputerDifficulty } from '../../types';

interface DifficultySelectorProps {
  /** Current difficulty level (1-10) */
  currentLevel: ComputerDifficulty;
  /** Handler for difficulty level change */
  onLevelChange: (level: ComputerDifficulty) => void;
  /** Whether the selector should be disabled */
  disabled?: boolean;
  /** Whether to show expanded view with descriptions */
  showDescriptions?: boolean;
}

const DIFFICULTY_DESCRIPTIONS: Record<ComputerDifficulty, string> = {
  1: 'Beginner',
  2: 'Novice', 
  3: 'Easy',
  4: 'Casual',
  5: 'Medium',
  6: 'Intermediate',
  7: 'Hard',
  8: 'Advanced',
  9: 'Expert',
  10: 'Master'
};

export const DifficultySelector: React.FC<DifficultySelectorProps> = ({
  currentLevel,
  onLevelChange,
  disabled = false,
  showDescriptions = false
}) => {
  const levels: ComputerDifficulty[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  return (
    <div className="bg-card border-b border-border p-2 sm:p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex flex-col gap-2 sm:gap-3">
          <div className="flex items-center justify-between">
            <span className="text-xs sm:text-sm font-medium text-foreground">
              AI Difficulty
            </span>
            {showDescriptions && (
              <span className="text-xs sm:text-sm text-muted-foreground">
                Current: {DIFFICULTY_DESCRIPTIONS[currentLevel]}
              </span>
            )}
          </div>
          
          {/* Mobile-first responsive button grid */}
          <div className="grid grid-cols-5 sm:grid-cols-10 gap-1 sm:gap-2">
            {levels.map(level => (
              <button
                key={level}
                onClick={() => onLevelChange(level)}
                disabled={disabled}
                className={`
                  aspect-square w-full min-w-0 rounded text-xs sm:text-sm font-bold transition-all duration-200
                  disabled:opacity-50 disabled:cursor-not-allowed
                  ${level === currentLevel 
                    ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                    : 'bg-secondary text-secondary-foreground hover:bg-secondary/90 hover:scale-105'
                  }
                  ${!disabled && 'active:scale-95'}
                  focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50
                `}
                title={`${DIFFICULTY_DESCRIPTIONS[level]} (Level ${level})`}
                aria-label={`Set difficulty to level ${level}: ${DIFFICULTY_DESCRIPTIONS[level]}`}
              >
                {level}
              </button>
            ))}
          </div>
          
          {/* Descriptions shown on mobile when space allows */}
          {showDescriptions && (
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-1 text-xs text-muted-foreground mt-1">
              {levels.map((level, index) => (
                <div key={level} className={`text-center ${index >= 5 ? 'block sm:block' : ''}`}>
                  <span className="font-medium">{level}:</span> {DIFFICULTY_DESCRIPTIONS[level]}
                </div>
              ))}
            </div>
          )}
          
          {/* Mobile-friendly current level indicator */}
          <div className="flex justify-center sm:justify-start">
            <span className="text-xs text-foreground bg-muted px-2 py-1 rounded">
              Level {currentLevel}: {DIFFICULTY_DESCRIPTIONS[currentLevel]}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
>>>>>>> Stashed changes
};