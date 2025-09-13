import { useState, useEffect } from 'react'

export function useMenuDropdown() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const openMenu = () => {
    setIsMenuOpen(true)
  }
  const closeMenu = () => {
    setIsMenuOpen(false)
  }
  const toggleMenu = () => {
    setIsMenuOpen(prev => !prev)
  }

  // Close menu when clicking outside
  useEffect(() => {
    if (isMenuOpen) {
      const handleClickOutside = (event: MouseEvent) => {
        const target = event.target as Element
        if (!target.closest('[data-menu-button]') && !target.closest('[data-menu-dropdown]')) {
          closeMenu()
        }
      }
      
      document.addEventListener('click', handleClickOutside)
      return () => document.removeEventListener('click', handleClickOutside)
    }
  }, [isMenuOpen])

  return {
    isMenuOpen,
    openMenu,
    closeMenu,
    toggleMenu
  }
}