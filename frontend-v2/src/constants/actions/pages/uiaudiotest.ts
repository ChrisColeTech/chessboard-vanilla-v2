import { EyeOff } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'uiaudiotest',
  actions: [
    {
      id: 'toggle-uiaudiotest',
      label: 'Toggle UIAudioTest',
      icon: EyeOff,
      variant: 'default'
    }
  ] as ActionSheetAction[]
}