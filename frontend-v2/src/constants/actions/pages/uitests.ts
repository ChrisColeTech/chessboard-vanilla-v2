import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'uitests',
  actions: [
    {
      id: 'uitests-action',
      label: 'Ui Tests Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'uitests-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'uitests-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}