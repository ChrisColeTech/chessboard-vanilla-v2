import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'playchess',
  actions: [
    {
      id: 'playchess-action',
      label: 'Playchess Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'playchess-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'playchess-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}