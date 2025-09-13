import { useState, useCallback } from 'react'

/**
 * Hook for action sheet state management only
 * Following SRP - ONLY manages open/close state, no business logic
 * Matches existing pattern from useMenuDropdown.ts
 */
export function useActionSheet() {
  const [isOpen, setIsOpen] = useState(false)

  const openSheet = useCallback(() => {
    setIsOpen(true)
  }, [])

  const closeSheet = useCallback(() => {
    setIsOpen(false)
  }, [])

  const toggleSheet = useCallback(() => {
    setIsOpen(prev => !prev)
  }, [isOpen])

  return {
    isOpen,
    openSheet,
    closeSheet,
    toggleSheet
  }
}