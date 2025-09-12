import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'casino',
  actions: [
    {
      id: 'casino-action',
      label: 'Casino Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'casino-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'casino-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}