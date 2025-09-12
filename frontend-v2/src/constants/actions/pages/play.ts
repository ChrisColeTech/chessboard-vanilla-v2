import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'play',
  actions: [
    {
      id: 'play-action',
      label: 'Play Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'play-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'play-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}