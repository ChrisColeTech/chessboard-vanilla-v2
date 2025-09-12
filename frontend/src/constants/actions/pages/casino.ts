import { Target, Sword, RotateCw, BarChart3 } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'casino',
  actions: [
    { id: 'go-to-slots', label: 'Play Slots', icon: Target, variant: 'default' },
    { id: 'go-to-blackjack', label: 'Play Blackjack', icon: Sword, variant: 'default' },
    { id: 'go-to-roulette', label: 'Play Roulette', icon: RotateCw, variant: 'default' },
    { id: 'view-stats', label: 'View Stats', icon: BarChart3, variant: 'secondary' }
  ] as ActionSheetAction[]
}