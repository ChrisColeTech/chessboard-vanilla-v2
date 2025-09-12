import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'slots',
  actions: [
    {
      id: 'slots-action',
      label: 'Slots Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'slots-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'slots-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}