<<<<<<< Updated upstream
import { BackgroundEffectsRenderer } from '../background-effects/BackgroundEffectsRenderer'
=======
import { SafeBackgroundEffectsRenderer } from '../background-effects/BackgroundEffectsRenderer'
>>>>>>> Stashed changes

interface BackgroundEffectsProps {
  className?: string
}

/**
 * Background Effects Component
 * Simplified wrapper around BackgroundEffectsRenderer
 * Maintains backward compatibility with existing AppLayout integration
 */
export function BackgroundEffects({ className = '' }: BackgroundEffectsProps) {
<<<<<<< Updated upstream
  return <BackgroundEffectsRenderer className={className} />
=======
  return <SafeBackgroundEffectsRenderer className={className} />
>>>>>>> Stashed changes
}