import type { BackgroundEffectProps } from '../../../types/core/backgroundEffects'

const particles = ['●', '◦', '▪', '▫', '•', '∘', '▴', '▾']
const sizes = ['text-xs', 'text-sm', 'text-base', 'text-lg']
const positions = [
  'top-[10%] left-[15%]', 'top-[25%] right-[20%]', 'bottom-[30%] right-[25%]',
  'bottom-[15%] left-[30%]', 'top-[60%] left-[10%]', 'bottom-[60%] right-[15%]',
  'top-[40%] right-[40%]', 'bottom-[40%] left-[45%]'
]

/**
 * Particle Effects Component
 * Physics-inspired particles with subtle animation
 */
export function ParticleEffects({ className = '' }: BackgroundEffectProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Subtle radial gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-accent/5" />
      
      {/* Particle system */}
      {particles.map((particle, i) => (
        <div
          key={i}
          className={`absolute ${positions[i]} ${sizes[i % sizes.length]} text-primary/20 animate-bounce`}
          style={{
            animationDelay: `${i * 0.3}s`,
            animationDuration: '3s'
          }}
        >
          {particle}
        </div>
      ))}
    </div>
  )
}