// Global action handlers that match MenuDropdown functionality
type ActionHandler = () => void | Promise<void>

// We need to get the store and context instances at runtime, not import time
// So we create factory functions that return the handlers

// Simple version that doesn't use hooks - safer for service registration
export const COMMON_ACTION_HANDLERS: Record<string, ActionHandler> = {
  settings: async () => {
    try {
      // Get settings store directly without hook - use dynamic import to avoid circular deps
      const { useAppStore } = await import('../../stores/appStore')
      const { openSettings } = useAppStore.getState()
      openSettings()
    } catch (error) {
      console.error('❌ [COMMON ACTION] Failed to open settings:', error)
    }
  },

  help: async () => {
    // TODO: Implement help action - requires context access
  },

  stats: async () => {
    // TODO: Implement statistics display
  },

  themes: async () => {
    // TODO: Implement theme switching
  }
}