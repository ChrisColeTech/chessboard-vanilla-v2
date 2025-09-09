// Core action sheet component types - following clean component architecture
export interface ActionSheetAction {
  id: string
  label: string
  icon: React.ComponentType<{ className?: string }>
  variant: 'default' | 'destructive' | 'secondary'
  disabled?: boolean
  badge?: string | number
  shortcut?: string
  hasOwnAudio?: boolean // If true, action plays its own sound and doesn't need UI click sound
}

export interface ActionSheetProps {
  actions: ActionSheetAction[]
  onActionClick: (action: ActionSheetAction, close: () => void) => void
  onActionHover?: (actionLabel: string) => void
  onKeyDown: (event: React.KeyboardEvent) => void
  onClose: () => void
  isOpen: boolean
  className?: string
}

export interface ActionSheetContainerProps {
  currentPage: string
  className?: string
  onClose: () => void
  isOpen: boolean
  onOpenSettings: () => void
}