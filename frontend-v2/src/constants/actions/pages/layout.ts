import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'layout',
  actions: [
    {
      id: 'layout-action',
      label: 'Layout Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'layout-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'layout-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}