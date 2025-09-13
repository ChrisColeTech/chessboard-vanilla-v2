import { useEffect, useState } from 'react'
import { useBackgroundEffects } from '../../hooks/core/useBackgroundEffects'

interface BackgroundEffectsRendererProps {
  className?: string
}

/**
 * Background Effects Renderer with smooth transitions
 * Dynamically renders the appropriate background effect component based on current variant
 * Handles mounting, loading states, smooth transitions, and component switching
 */
export function BackgroundEffectsRenderer({ className = '' }: BackgroundEffectsRendererProps) {
  const [mounted, setMounted] = useState(false)
  const { currentVariant, isEnabled, service } = useBackgroundEffects()

  // Handle mounting (SSR safety)
  useEffect(() => {
    setMounted(true)
  }, [])

  // Don't render anything until component is mounted (SSR safety)
  if (!mounted) {
    return null
  }

  // Get the effect for the current variant
  const currentEffect = service.getEffect(currentVariant as any)

  // If effects are disabled or no effect is registered, render base overlay
  if (!isEnabled || currentVariant === 'off' || !currentEffect) {
    return <div className={`bg-overlay ${className}`} />
  }

  // Get the effect component from the configuration
  const EffectComponent = currentEffect.component

  // Render the effect component with proper props
  return (
    <EffectComponent 
      className={className} 
      variant={currentVariant as any}
    />
  )
}

/**
 * Fallback component for when an effect fails to render
 */
export function BackgroundEffectsFallback({ className = '' }: { className?: string }) {
  return (
    <div className={`bg-overlay ${className}`}>
      <div className="absolute inset-0 bg-gaming-gradient opacity-30" />
    </div>
  )
}

/**
 * Error boundary wrapper for background effects
 * Provides fallback rendering if an effect component throws an error
 */
interface BackgroundEffectsErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<{ className?: string }>
  className?: string
}

export function BackgroundEffectsErrorBoundary({ 
  children, 
  fallback: Fallback = BackgroundEffectsFallback,
  className = ''
}: BackgroundEffectsErrorBoundaryProps) {
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    // Reset error state when children change (effect switching)
    setHasError(false)
  }, [children])

  if (hasError) {
    console.warn('🎨 [BackgroundEffects] Effect component error, falling back to default')
    return <Fallback className={className} />
  }

  return <>{children}</>
}

/**
 * Main renderer with error boundary protection
 */
export function SafeBackgroundEffectsRenderer({ className = '' }: BackgroundEffectsRendererProps) {
  return (
    <BackgroundEffectsErrorBoundary className={className}>
      <BackgroundEffectsRenderer className={className} />
    </BackgroundEffectsErrorBoundary>
  )
}