// Persistence utilities for localStorage
export class PersistenceStore {
  private static readonly PREFIX = 'chess-app-'

  static get<T>(key: string, defaultValue: T): T {
    try {
      const stored = localStorage.getItem(this.PREFIX + key)
      return stored ? JSON.parse(stored) : defaultValue
    } catch {
      return defaultValue
    }
  }

  static set<T>(key: string, value: T): void {
    try {
      localStorage.setItem(this.PREFIX + key, JSON.stringify(value))
    } catch {
      // Silently fail if localStorage is not available
    }
  }

  static remove(key: string): void {
    try {
      localStorage.removeItem(this.PREFIX + key)
    } catch {
      // Silently fail if localStorage is not available
    }
  }

  static clear(): void {
    try {
      const keys = Object.keys(localStorage).filter(key => key.startsWith(this.PREFIX))
      keys.forEach(key => localStorage.removeItem(key))
    } catch {
      // Silently fail if localStorage is not available
    }
  }
}

// Convenience functions for common persistence patterns
export const persist = {
  theme: (themeId: string) => PersistenceStore.set('theme', themeId),
  getTheme: (defaultTheme: string) => PersistenceStore.get('theme', defaultTheme),
  
  tab: (tabId: string) => PersistenceStore.set('selected-tab', tabId),
  getTab: (defaultTab: string) => PersistenceStore.get('selected-tab', defaultTab),
  
  settings: (settings: Record<string, any>) => PersistenceStore.set('settings', settings),
  getSettings: (defaultSettings: Record<string, any>) => PersistenceStore.get('settings', defaultSettings),
}