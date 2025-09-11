import { Settings, Sun, Moon, Zap, Crown, TreePine, Gem, Shield, Wrench, Palette, Monitor, Target, Globe, Coins, Droplets } from 'lucide-react'
import { useUIClickSound } from '../../hooks/audio/useUIClickSound'

export type ThemeId = 'light' | 'dark' | 'theme-onyx' | 'theme-sage' | 'theme-amber' | 'theme-crimson' | 'theme-gold' | 'theme-copper' | 'theme-violet' | 'theme-matrix' | 'theme-neon' | 'theme-scarlet' | 'theme-azure' | 'theme-bronze' | 'theme-teal' | 'theme-cyber-neon' | 'theme-cyber-neon-light' | 'theme-dragon-gold' | 'theme-dragon-gold-light' | 'theme-shadow-knight' | 'theme-shadow-knight-light' | 'theme-forest-mystique' | 'theme-forest-mystique-light' | 'theme-royal-purple' | 'theme-royal-purple-light'

export type BaseTheme = 'default' | 'onyx' | 'sage' | 'amber' | 'crimson' | 'gold' | 'copper' | 'violet' | 'matrix' | 'neon' | 'scarlet' | 'azure' | 'bronze' | 'teal' | 'cyber-neon' | 'dragon-gold' | 'shadow-knight' | 'forest-mystique' | 'royal-purple'

export interface Theme {
  id: ThemeId
  name: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  preview: string
}

export interface BaseThemeConfig {
  id: BaseTheme
  name: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  darkPreview: string
  lightPreview: string
}

export const themes: Theme[] = [
  { 
    id: 'light', 
    name: 'Light', 
    description: 'Clean light theme', 
    icon: Sun,
    preview: 'bg-slate-50 border-slate-200'
  },
  { 
    id: 'dark', 
    name: 'Dark', 
    description: 'Pure dark elegance', 
    icon: Moon,
    preview: 'bg-gray-900 border-gray-600'
  },
  { 
    id: 'theme-cyber-neon', 
    name: 'Cyber Neon', 
    description: 'Electric neon glow', 
    icon: Zap,
    preview: 'bg-gray-900 border-pink-500'
  },
  { 
    id: 'theme-cyber-neon-light', 
    name: 'Cyber Light', 
    description: 'Bright neon colors', 
    icon: Zap,
    preview: 'bg-purple-50 border-pink-400'
  },
  { 
    id: 'theme-dragon-gold', 
    name: 'Dragon Gold', 
    description: 'Medieval dragon theme', 
    icon: Crown,
    preview: 'bg-orange-950 border-yellow-400'
  },
  { 
    id: 'theme-dragon-gold-light', 
    name: 'Gold Light', 
    description: 'Light dragon theme', 
    icon: Crown,
    preview: 'bg-orange-50 border-red-500'
  },
  { 
    id: 'theme-shadow-knight', 
    name: 'Shadow Knight', 
    description: 'Dark steel armor', 
    icon: Shield,
    preview: 'bg-black border-blue-400'
  },
  { 
    id: 'theme-shadow-knight-light', 
    name: 'Knight Light', 
    description: 'Polished steel', 
    icon: Shield,
    preview: 'bg-blue-50 border-blue-500'
  },
  { 
    id: 'theme-forest-mystique', 
    name: 'Forest Mystique', 
    description: 'Mystic forest theme', 
    icon: TreePine,
    preview: 'bg-green-950 border-green-400'
  },
  { 
    id: 'theme-forest-mystique-light', 
    name: 'Forest Light', 
    description: 'Light forest theme', 
    icon: TreePine,
    preview: 'bg-green-50 border-green-500'
  },
  { 
    id: 'theme-royal-purple', 
    name: 'Royal Purple', 
    description: 'Majestic purple theme', 
    icon: Gem,
    preview: 'bg-purple-950 border-purple-400'
  },
  { 
    id: 'theme-royal-purple-light', 
    name: 'Purple Light', 
    description: 'Lavender royalty', 
    icon: Gem,
    preview: 'bg-purple-100 border-purple-600'
  }
]

export const baseThemes: BaseThemeConfig[] = [
  {
    id: 'default',
    name: 'Default',
    description: 'Classic clean theme',
    icon: Settings,
    darkPreview: 'bg-gray-900 border-gray-600',
    lightPreview: 'bg-slate-50 border-slate-200'
  },
  {
    id: 'onyx',
    name: 'Onyx',
    description: 'Monochrome professional',
    icon: Settings,
    darkPreview: 'bg-gray-900 border-gray-400',
    lightPreview: 'bg-gray-50 border-gray-300'
  },
  {
    id: 'sage',
    name: 'Sage',
    description: 'Professional green theme',
    icon: TreePine,
    darkPreview: 'bg-green-950 border-green-400',
    lightPreview: 'bg-green-50 border-green-500'
  },
  {
    id: 'amber',
    name: 'Amber',
    description: 'Professional orange theme',
    icon: Crown,
    darkPreview: 'bg-orange-950 border-orange-400',
    lightPreview: 'bg-orange-50 border-orange-500'
  },
  {
    id: 'crimson',
    name: 'Crimson',
    description: 'Professional red theme',
    icon: Shield,
    darkPreview: 'bg-red-950 border-red-400',
    lightPreview: 'bg-red-50 border-red-500'
  },
  {
    id: 'gold',
    name: 'Gold',
    description: 'Investigative amber theme',
    icon: Coins,
    darkPreview: 'bg-yellow-950 border-yellow-400',
    lightPreview: 'bg-yellow-50 border-yellow-500'
  },
  {
    id: 'copper',
    name: 'Copper',
    description: 'Warm debugging theme',
    icon: Wrench,
    darkPreview: 'bg-orange-950 border-orange-400',
    lightPreview: 'bg-orange-50 border-orange-500'
  },
  {
    id: 'violet',
    name: 'Violet',
    description: 'Low-level analysis theme',
    icon: Palette,
    darkPreview: 'bg-purple-950 border-purple-400',
    lightPreview: 'bg-purple-50 border-purple-500'
  },
  {
    id: 'matrix',
    name: 'Matrix',
    description: 'Binary explorer theme',
    icon: Monitor,
    darkPreview: 'bg-green-950 border-green-400',
    lightPreview: 'bg-green-50 border-green-500'
  },
  {
    id: 'neon',
    name: 'Neon',
    description: 'Cyber forensics theme',
    icon: Zap,
    darkPreview: 'bg-cyan-950 border-cyan-400',
    lightPreview: 'bg-cyan-50 border-cyan-500'
  },
  {
    id: 'scarlet',
    name: 'Scarlet',
    description: 'Threat hunter theme',
    icon: Target,
    darkPreview: 'bg-red-950 border-red-400',
    lightPreview: 'bg-red-50 border-red-500'
  },
  {
    id: 'azure',
    name: 'Azure',
    description: 'Network analysis theme',
    icon: Globe,
    darkPreview: 'bg-blue-950 border-blue-400',
    lightPreview: 'bg-blue-50 border-blue-500'
  },
  {
    id: 'bronze',
    name: 'Bronze',
    description: 'Malware analyst theme',
    icon: Shield,
    darkPreview: 'bg-amber-950 border-amber-400',
    lightPreview: 'bg-amber-50 border-amber-500'
  },
  {
    id: 'teal',
    name: 'Teal',
    description: 'Digital sleuth theme',
    icon: Droplets,
    darkPreview: 'bg-teal-950 border-teal-400',
    lightPreview: 'bg-teal-50 border-teal-500'
  },
  {
    id: 'cyber-neon',
    name: 'Cyber Neon',
    description: 'Electric neon gaming',
    icon: Zap,
    darkPreview: 'bg-gray-900 border-pink-500',
    lightPreview: 'bg-purple-50 border-pink-400'
  },
  {
    id: 'dragon-gold',
    name: 'Dragon Gold',
    description: 'Medieval dragon power',
    icon: Crown,
    darkPreview: 'bg-orange-950 border-yellow-400',
    lightPreview: 'bg-orange-50 border-red-500'
  },
  {
    id: 'shadow-knight',
    name: 'Shadow Knight',
    description: 'Dark steel armor',
    icon: Shield,
    darkPreview: 'bg-black border-blue-400',
    lightPreview: 'bg-blue-50 border-blue-500'
  },
  {
    id: 'forest-mystique',
    name: 'Forest Mystique',
    description: 'Mystic nature theme',
    icon: TreePine,
    darkPreview: 'bg-green-950 border-green-400',
    lightPreview: 'bg-green-50 border-green-500'
  },
  {
    id: 'royal-purple',
    name: 'Royal Purple',
    description: 'Majestic royal theme',
    icon: Gem,
    darkPreview: 'bg-purple-950 border-purple-400',
    lightPreview: 'bg-purple-100 border-purple-600'
  }
]

interface ThemeSwitcherProps {
  onOpenSettings: () => void
  isSettingsOpen?: boolean
}

export function ThemeSwitcher({ onOpenSettings, isSettingsOpen = false }: ThemeSwitcherProps) {
  const { playUIClick } = useUIClickSound()

  const handleSettingsClick = () => {
    playUIClick('Settings Button')
    onOpenSettings()
  }

  return (
    <button
      onClick={handleSettingsClick}
      className={`flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10 border border-primary/20 text-primary hover:bg-primary/20 hover:border-primary/40 hover:shadow-lg hover:shadow-primary/20 hover:scale-105 transition-all duration-300 ${isSettingsOpen ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
      title="Change Theme"
    >
      <Settings className="w-5 h-5" />
    </button>
  )
}