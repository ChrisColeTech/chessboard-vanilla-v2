import { EyeOff } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'layouttest',
  actions: [
    {
      id: 'toggle-layouttest',
      label: 'Toggle LayoutTest',
      icon: EyeOff,
      variant: 'default'
    }
  ] as ActionSheetAction[]
}