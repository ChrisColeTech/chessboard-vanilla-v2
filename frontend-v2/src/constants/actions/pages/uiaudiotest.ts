import { Navigation, Play, Settings } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'uiaudiotest',
  actions: [
    {
      id: 'uiaudiotest-action',
      label: 'Uiaudio Test Action',
      icon: Navigation,
      variant: 'default'
    },
    {
      id: 'uiaudiotest-settings',
      label: 'Settings',
      icon: Settings,
      variant: 'default'
    },
    {
      id: 'uiaudiotest-play',
      label: 'Start',
      icon: Play,
      variant: 'primary'
    }
  ] as ActionSheetAction[]
}