import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'dragtest',
  actions: [
    {
      id: 'dragtest-action',
      label: 'Drag Test Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'dragtest-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'dragtest-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}