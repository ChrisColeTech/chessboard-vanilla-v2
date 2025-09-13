import { EyeOff } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'dragtest',
  actions: [
    {
      id: 'toggle-dragtest',
      label: 'Toggle DragTest',
      icon: EyeOff,
      variant: 'default'
    }
  ] as ActionSheetAction[]
}