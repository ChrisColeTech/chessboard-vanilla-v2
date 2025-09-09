// Updated ThemeContext.tsx logic

// Theme application logic - updated for new naming
useEffect(() => {
  const html = document.documentElement
  
  console.log('🎨 [THEME] Applying theme:', currentTheme)
  
  // Remove all theme classes (old and new)
  const allThemeClasses = [
    // Old system classes to remove
    'dark', 'theme-cyber-neon', 'theme-dragon-gold', 'theme-shadow-knight', 
    'theme-forest-mystique', 'theme-royal-purple', 'theme-cyber-neon-light',
    'theme-dragon-gold-light', 'theme-shadow-knight-light', 
    'theme-forest-mystique-light', 'theme-royal-purple-light',
    
    // New organized theme classes
    'theme-onyx', 'theme-sage', 'theme-amber', 'theme-crimson',
    'theme-gold', 'theme-copper', 'theme-violet', 'theme-matrix',
    'theme-neon', 'theme-scarlet', 'theme-azure', 'theme-bronze', 'theme-teal'
  ]
  
  allThemeClasses.forEach(cls => html.classList.remove(cls))
  
  // Add current theme class
  if (currentTheme !== 'light') {
    html.classList.add(currentTheme)
  }
  
  // Handle dark mode for professional themes
  if (currentTheme.startsWith('theme-') && isDarkMode) {
    html.classList.add('dark')
  }
  
  console.log('🎨 [THEME] Document classes:', Array.from(html.classList).join(', '))
  
  // Save to localStorage
  localStorage.setItem('chess-app-theme', currentTheme)
}, [currentTheme, isDarkMode])