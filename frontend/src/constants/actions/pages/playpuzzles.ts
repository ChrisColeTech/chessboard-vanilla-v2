import { RotateCcw, Brain, SkipForward, RefreshCw } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'playpuzzles',
  actions: [
    { id: 'new-puzzle', label: 'New Puzzle', icon: RotateCcw, variant: 'default' },
    { id: 'hint', label: 'Get Hint', icon: Brain, variant: 'secondary' },
    { id: 'skip-puzzle', label: 'Skip Puzzle', icon: SkipForward, variant: 'secondary' },
    { id: 'reset-puzzle', label: 'Reset', icon: RefreshCw, variant: 'default' }
  ] as ActionSheetAction[]
}