import { RotateCcw, Pause, Eye, Undo } from 'lucide-react'
import type { ActionSheetAction } from '../../../types/core/action-sheet.types'

export const pageActions = {
  id: 'playchess',
  actions: [
    { id: 'new-game', label: 'New Game', icon: RotateCcw, variant: 'default' },
    { id: 'pause-game', label: 'Pause Game', icon: Pause, variant: 'secondary' },
    { id: 'show-moves', label: 'Show Moves', icon: Eye, variant: 'default' },
    { id: 'undo-move', label: 'Undo Move', icon: Undo, variant: 'secondary' }
  ] as ActionSheetAction[]
}