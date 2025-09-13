/**
 * Auto-generated Filter Configuration
 * 
 * This file maps chess themes to visual filter effects for different game states.
 * 
 * Generated on: 2025-09-09T00:27:38.872Z
 * 
 * Themes found: 23
 * Filters found: 15
 */

// Available visual effect filters from chess-filters.css
export const AVAILABLE_FILTERS = [
  'cyberpunk',
  'frosted',
  'glassmorphism',
  'high-contrast',
  'high-visibility',
  'holographic',
  'luxury-gold',
  'matrix',
  'neon-glow',
  'noir',
  'retro-invert',
  'rgb-pulse',
  'shimmer',
  'soft-depth',
  'vintage'
] as const;

// Available themes from theme CSS files
export const AVAILABLE_THEMES = [
  'theme-amber',
  'theme-azure',
  'theme-bronze',
  'theme-copper',
  'theme-crimson',
  'theme-gold',
  'theme-matrix',
  'theme-neon',
  'theme-onyx',
  'theme-sage',
  'theme-scarlet',
  'theme-teal',
  'theme-violet',
  'theme-cyber-neon',
  'theme-cyber-neon-light',
  'theme-dragon-gold',
  'theme-dragon-gold-light',
  'theme-forest-mystique',
  'theme-forest-mystique-light',
  'theme-royal-purple',
  'theme-royal-purple-light',
  'theme-shadow-knight',
  'theme-shadow-knight-light'
] as const;

// Game states that can trigger filter effects
export const FILTER_STATES = [
  'selected',
  'king-in-check',
  'valid-move', 
  'checkmate',
  'last-move',
  'capture-target',
  'under-attack',
  'promotion'
] as const;

// Theme to filter mappings for different game states
export const THEME_FILTER_CONFIG: Record<string, Partial<Record<typeof FILTER_STATES[number], typeof AVAILABLE_FILTERS[number]>>> = {
  'theme-amber': {
    'selected': 'retro-invert',
    'valid-move': 'high-contrast'
  },
  'theme-azure': {
    'selected': 'soft-depth',
    'valid-move': 'glassmorphism'
  },
  'theme-bronze': {
    'selected': 'luxury-gold',
    'valid-move': 'glassmorphism'
  },
  'theme-copper': {
    'selected': 'luxury-gold',
    'valid-move': 'glassmorphism'
  },
  'theme-crimson': {
    'selected': 'noir',
    'valid-move': 'high-visibility'
  },
  'theme-gold': {
    'selected': 'luxury-gold',
    'valid-move': 'glassmorphism'
  },
  'theme-matrix': {
    'selected': 'matrix',
    'valid-move': 'cyberpunk'
  },
  'theme-neon': {
    'selected': 'neon-glow',
    'valid-move': 'rgb-pulse'
  },
  'theme-onyx': {
    'selected': 'retro-invert',
    'valid-move': 'high-contrast'
  },
  'theme-sage': {
    'selected': 'frosted',
    'valid-move': 'vintage'
  },
  'theme-scarlet': {
    'selected': 'soft-depth',
    'valid-move': 'frosted'
  },
  'theme-teal': {
    'selected': 'vintage',
    'valid-move': 'frosted'
  },
  'theme-violet': {
    'selected': 'holographic',
    'valid-move': 'shimmer'
  },
  'theme-cyber-neon': {
    'selected': 'neon-glow',
    'valid-move': 'rgb-pulse'
  },
  'theme-cyber-neon-light': {
    'selected': 'neon-glow',
    'valid-move': 'rgb-pulse'
  },
  'theme-dragon-gold': {
    'selected': 'luxury-gold',
    'valid-move': 'glassmorphism'
  },
  'theme-dragon-gold-light': {
    'selected': 'luxury-gold',
    'valid-move': 'glassmorphism'
  },
  'theme-forest-mystique': {
    'selected': 'soft-depth',
    'valid-move': 'frosted'
  },
  'theme-forest-mystique-light': {
    'selected': 'soft-depth',
    'valid-move': 'frosted'
  },
  'theme-royal-purple': {
    'selected': 'holographic',
    'valid-move': 'shimmer'
  },
  'theme-royal-purple-light': {
    'selected': 'holographic',
    'valid-move': 'shimmer'
  },
  'theme-shadow-knight': {
    'selected': 'noir',
    'valid-move': 'high-contrast'
  },
  'theme-shadow-knight-light': {
    'selected': 'noir',
    'valid-move': 'high-contrast'
  }
};

/**
 * Get the appropriate filter for a theme and game state
 */
export function getThemeFilter(theme: string, state: string): string | null {
  return THEME_FILTER_CONFIG[theme]?.[state as keyof typeof THEME_FILTER_CONFIG[string]] || null;
}

/**
 * Get all filter classes for a theme and list of states
 */
export function getThemeFilterClasses(theme: string, states: string[]): string[] {
  const filters: string[] = [];
  
  states.forEach(state => {
    const filter = getThemeFilter(theme, state);
    if (filter) {
      filters.push(filter);
    }
  });
  
  return [...new Set(filters)]; // Remove duplicates
}
