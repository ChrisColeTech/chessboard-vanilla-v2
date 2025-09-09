// Updated ThemeSwitcher.tsx types and configurations
export type ThemeId = 
  // Professional themes (solid colors, no effects)
  | 'theme-onyx' | 'theme-sage' | 'theme-amber' | 'theme-crimson'
  | 'theme-gold' | 'theme-copper' | 'theme-violet' | 'theme-matrix' 
  | 'theme-neon' | 'theme-scarlet' | 'theme-azure' | 'theme-bronze' | 'theme-teal'
  // Gaming themes (with effects) 
  | 'theme-cyber-neon' | 'theme-dragon-gold' | 'theme-shadow-knight'
  | 'theme-forest-mystique' | 'theme-royal-purple'
  // Gaming light variants
  | 'theme-cyber-neon-light' | 'theme-dragon-gold-light' | 'theme-shadow-knight-light'
  | 'theme-forest-mystique-light' | 'theme-royal-purple-light'

export type BaseTheme = 
  // Professional themes  
  | 'onyx' | 'sage' | 'amber' | 'crimson' | 'gold' | 'copper' | 'violet'
  | 'matrix' | 'neon' | 'scarlet' | 'azure' | 'bronze' | 'teal'
  // Gaming themes
  | 'cyber-neon' | 'dragon-gold' | 'shadow-knight' | 'forest-mystique' | 'royal-purple'

export const professionalThemes: BaseThemeConfig[] = [
  {
    id: 'onyx',
    name: 'Onyx',
    description: 'Classic monochrome professional',
    icon: Settings,
    category: 'professional'
  },
  {
    id: 'sage', 
    name: 'Sage',
    description: 'Professional green theme',
    icon: Leaf,
    category: 'professional'
  },
  {
    id: 'amber',
    name: 'Amber', 
    description: 'Professional orange theme',
    icon: Zap,
    category: 'professional'
  },
  {
    id: 'crimson',
    name: 'Crimson',
    description: 'Professional red theme', 
    icon: Shield,
    category: 'professional'
  }
  // ... add the other 9 professional themes
]

export const gamingThemes: BaseThemeConfig[] = [
  {
    id: 'cyber-neon',
    name: 'Cyber Neon',
    description: 'Electric neon gaming',
    icon: Zap,
    category: 'gaming'
  },
  {
    id: 'dragon-gold',
    name: 'Dragon Gold', 
    description: 'Medieval dragon power',
    icon: Crown,
    category: 'gaming'
  }
  // ... add the other gaming themes
]