import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'splash',
  actions: [
    {
      id: 'splash-action',
      label: 'Splash Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'splash-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'splash-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}