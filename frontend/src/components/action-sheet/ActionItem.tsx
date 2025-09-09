import type { ActionSheetAction } from '../../types/core/action-sheet.types'

/**
 * Pure action item component - NO BUSINESS LOGIC
 * Just renders the action button with proper accessibility
 * Receives all handlers via props following SRP
 */
interface ActionItemProps {
  action: ActionSheetAction
  onSelect: () => void
  onHover?: () => void
}

export function ActionItem({ action, onSelect, onHover }: ActionItemProps) {
  const IconComponent = action.icon

  const getVariantClass = (variant: ActionSheetAction['variant']) => {
    switch (variant) {
      case 'destructive':
        return 'action-item-destructive'
      case 'secondary':
        return 'action-item-secondary'
      default:
        return 'action-item-default'
    }
  }

  const className = [
    "action-item group", // Base action item class with all common styles
    getVariantClass(action.variant), // Variant-specific class
    action.disabled && "opacity-50 cursor-not-allowed"
  ].filter(Boolean).join(' ')

  return (
    <button
      onClick={onSelect}
      onMouseEnter={onHover}
      disabled={action.disabled}
      className={className}
      role="menuitem"
      aria-label={action.label}
      {...(action.hasOwnAudio && { 'data-no-sound': true })}
    >
      <IconComponent className="action-item-icon w-6 h-6" />
      <span className="action-item-text">{action.label}</span>
      {action.badge && (
        <span className="ml-auto px-2 py-1 text-xs bg-primary/20 text-primary rounded-full">
          {action.badge}
        </span>
      )}
      {action.shortcut && (
        <kbd className="ml-auto px-1.5 py-0.5 text-xs bg-black/20 text-muted-foreground rounded border hidden sm:inline-flex">
          {action.shortcut}
        </kbd>
      )}
    </button>
  )
}