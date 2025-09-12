import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'users',
  actions: [
    {
      id: 'users-action',
      label: 'Users Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'users-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'users-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}