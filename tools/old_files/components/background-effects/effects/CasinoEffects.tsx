import type { BackgroundEffectProps } from '../../../types/core/backgroundEffects'

/**
 * Casino Effects Component
 * Enhanced gaming background with floating orbs and sparkles
 * Extracted from SlotMachineTestPage for reuse
 */
export function CasinoEffects({ className = '' }: BackgroundEffectProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Floating Gaming Elements */}
      <div className="bg-orb bg-orb-lg bg-orb-primary top-20 left-20 animation-delay-500"></div>
      <div className="bg-orb bg-orb-md bg-orb-accent bottom-32 right-16 animation-delay-1000"></div>
      <div className="bg-orb bg-orb-sm bg-orb-primary-light top-1/3 left-1/4 animation-delay-1500"></div>
      
      {/* Additional floating orbs for richer effect */}
      <div className="bg-orb bg-orb-md bg-orb-accent-light top-2/3 right-1/5 animation-delay-2000"></div>
      <div className="bg-orb bg-orb-sm bg-orb-primary bottom-1/4 left-1/5 animation-delay-2500"></div>
      
      {/* Sparkle Effects */}
      <div className="bg-sparkle bg-sparkle-lg bg-orb-primary-60 top-1/4 right-1/4 animation-delay-300"></div>
      <div className="bg-sparkle bg-sparkle-sm bg-orb-accent-40 bottom-1/3 left-1/3 animation-delay-700"></div>
      <div className="bg-sparkle bg-sparkle-md bg-orb-foreground-50 top-2/3 right-1/3 animation-delay-1200"></div>
      
      {/* Additional sparkles for enhanced effect */}
      <div className="bg-sparkle bg-sparkle-sm bg-orb-primary-40 top-1/2 left-1/6 animation-delay-1600"></div>
      <div className="bg-sparkle bg-sparkle-lg bg-orb-accent-60 bottom-1/5 right-2/5 animation-delay-2100"></div>
    </div>
  )
}