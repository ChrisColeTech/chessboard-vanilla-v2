import { BackgroundEffectsRenderer } from '../background-effects/BackgroundEffectsRenderer'

interface BackgroundEffectsProps {
  className?: string
}

/**
 * Background Effects Component
 * Simplified wrapper around BackgroundEffectsRenderer
 * Maintains backward compatibility with existing AppLayout integration
 */
export function BackgroundEffects({ className = '' }: BackgroundEffectsProps) {
  return <BackgroundEffectsRenderer className={className} />
}