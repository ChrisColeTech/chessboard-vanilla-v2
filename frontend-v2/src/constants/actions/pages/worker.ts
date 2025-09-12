import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'worker',
  actions: [
    {
      id: 'worker-action',
      label: 'Worker Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'worker-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'worker-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}