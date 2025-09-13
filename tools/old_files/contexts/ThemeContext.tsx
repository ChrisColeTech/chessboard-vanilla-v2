import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { type ThemeId, type BaseTheme } from '../components/core/ThemeSwitcher'

interface ThemeContextValue {
  currentTheme: ThemeId
  isDarkMode: boolean
  selectedBaseTheme: BaseTheme
  setTheme: (themeId: ThemeId) => void
  setBaseTheme: (baseTheme: BaseTheme) => void
  toggleMode: () => void
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

interface ThemeProviderProps {
  children: ReactNode
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [currentTheme, setCurrentTheme] = useState<ThemeId>('theme-onyx')
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [selectedBaseTheme, setSelectedBaseTheme] = useState<BaseTheme>('onyx')

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('chess-app-theme') as ThemeId || 'theme-onyx'
    const savedDarkMode = localStorage.getItem('chess-app-dark-mode') === 'true'
    
    setCurrentTheme(savedTheme)
    setIsDarkMode(savedDarkMode)
    
    // Determine base theme from saved theme
    if (savedTheme === 'light' || savedTheme === 'dark') {
      setSelectedBaseTheme('default')
    } else if (savedTheme.startsWith('theme-')) {
      // Extract base theme name (e.g., 'theme-bronze' -> 'bronze')
      const baseThemeId = savedTheme.replace('theme-', '') as BaseTheme
      setSelectedBaseTheme(baseThemeId)
    }
  }, [])

  // Apply theme to document when currentTheme changes
  useEffect(() => {
    const html = document.documentElement
    
    
    // Remove all theme classes (old and new)
    const themeClasses = [
      'dark', 
      // Old gaming themes
      'theme-cyber-neon', 'theme-cyber-neon-light', 'theme-dragon-gold', 'theme-dragon-gold-light', 
      'theme-shadow-knight', 'theme-shadow-knight-light', 'theme-forest-mystique', 'theme-forest-mystique-light', 
      'theme-royal-purple', 'theme-royal-purple-light',
      // Professional themes  
      'theme-onyx', 'theme-sage', 'theme-amber', 'theme-crimson', 'theme-gold', 'theme-copper', 
      'theme-violet', 'theme-matrix', 'theme-neon', 'theme-scarlet', 'theme-azure', 'theme-bronze', 'theme-teal'
    ]
    
    themeClasses.forEach(cls => {
      if (html.classList.contains(cls)) {
        html.classList.remove(cls)
      }
    })
    
    
    // Add current theme class
    let classesToAdd = []
    if (currentTheme === 'dark') {
      classesToAdd.push('dark')
    } else if (currentTheme !== 'light') {
      const themeClass = currentTheme.startsWith('theme-') ? currentTheme : `theme-${currentTheme}`
      classesToAdd.push(themeClass)
    }
    
    // For professional themes, also add dark class if needed
    if (currentTheme.startsWith('theme-') && isDarkMode) {
      if (!classesToAdd.includes('dark')) {
        classesToAdd.push('dark')
      }
    }
    
    classesToAdd.forEach(cls => html.classList.add(cls))
    
    
    // Save to localStorage
    localStorage.setItem('chess-app-theme', currentTheme)
    localStorage.setItem('chess-app-dark-mode', isDarkMode.toString())
  }, [currentTheme, isDarkMode, selectedBaseTheme])

  const setTheme = (themeId: ThemeId) => {
    setCurrentTheme(themeId)
    
    // Update derived state
    if (themeId === 'light' || themeId === 'dark') {
      setSelectedBaseTheme('default')
      setIsDarkMode(themeId === 'dark')
    } else {
      const baseThemeId = themeId.replace('-light', '') as BaseTheme
      setSelectedBaseTheme(baseThemeId)
      setIsDarkMode(!themeId.endsWith('-light'))
    }
  }

  const setBaseTheme = (baseTheme: BaseTheme) => {
    setSelectedBaseTheme(baseTheme)
    
    // Calculate the actual theme ID
    let actualThemeId: ThemeId
    if (baseTheme === 'default') {
      actualThemeId = isDarkMode ? 'dark' : 'light'
    } else {
      actualThemeId = isDarkMode ? `theme-${baseTheme}` as ThemeId : `theme-${baseTheme}-light` as ThemeId
    }
    
    setCurrentTheme(actualThemeId)
  }

  const toggleMode = () => {
    const newIsDarkMode = !isDarkMode
    setIsDarkMode(newIsDarkMode)
    
    // Calculate the actual theme ID
    let actualThemeId: ThemeId
    if (selectedBaseTheme === 'default') {
      actualThemeId = newIsDarkMode ? 'dark' : 'light'
    } else {
      // For professional themes, the theme ID stays the same, only isDarkMode changes
      actualThemeId = `theme-${selectedBaseTheme}` as ThemeId
    }
    
    setCurrentTheme(actualThemeId)
  }

  const value: ThemeContextValue = {
    currentTheme,
    isDarkMode,
    selectedBaseTheme,
    setTheme,
    setBaseTheme,
    toggleMode
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}