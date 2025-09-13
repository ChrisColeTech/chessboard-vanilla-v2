import type { BackgroundEffectProps } from '../../../types/core/backgroundEffects'

const shapes = ['◇', '◯', '△', '☐', '◊', '○', '▽', '□']
const positions = [
  'top-1/4 left-1/4', 'top-1/3 right-1/3', 'bottom-1/4 right-1/4',
  'bottom-1/3 left-1/3', 'top-2/3 left-1/5', 'bottom-2/3 right-1/5',
  'top-1/5 right-1/5', 'bottom-1/5 left-1/5'
]

/**
 * Minimal Effects Component
 * Clean geometric shapes for professional themes
 */
export function MinimalEffects({ className = '' }: BackgroundEffectProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Subtle gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-background to-muted opacity-30" />
      
      {/* Geometric shapes */}
      {shapes.map((shape, i) => (
        <div
          key={i}
          className={`absolute ${positions[i]} text-foreground/10 text-2xl animate-pulse`}
          style={{
            animationDelay: `${i * 0.5}s`,
            animationDuration: '4s'
          }}
        >
          {shape}
        </div>
      ))}
    </div>
  )
}