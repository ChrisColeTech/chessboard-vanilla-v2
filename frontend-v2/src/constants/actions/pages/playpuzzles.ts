import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'playpuzzles',
  actions: [
    {
      id: 'playpuzzles-action',
      label: 'Playpuzzles Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'playpuzzles-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'playpuzzles-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}