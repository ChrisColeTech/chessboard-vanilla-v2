import type { BackgroundEffectProps } from '../../../types/core/backgroundEffects'

const symbols = ['∞', '◊', '※', '⟡', '⬟', '⬢', '⬣', '⬡']
const rotations = ['rotate-0', 'rotate-45', 'rotate-90', 'rotate-180']
const positions = [
  'top-[20%] left-[20%]', 'top-[30%] right-[25%]', 'bottom-[25%] right-[30%]',
  'bottom-[20%] left-[25%]', 'top-[70%] left-[15%]', 'bottom-[70%] right-[20%]',
  'top-[50%] right-[50%]', 'bottom-[50%] left-[50%]'
]

/**
 * Abstract Effects Component
 * Mathematical and abstract symbols with geometric transformations
 */
export function AbstractEffects({ className = '' }: BackgroundEffectProps) {
  return (
    <div className={`bg-overlay ${className}`}>
      {/* Abstract gradient background */}
      <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 to-accent/5" />
      
      {/* Mathematical symbols */}
      {symbols.map((symbol, i) => (
        <div
          key={i}
          className={`absolute ${positions[i]} ${rotations[i % rotations.length]} text-xl text-accent/15 animate-spin`}
          style={{
            animationDelay: `${i * 0.7}s`,
            animationDuration: '8s'
          }}
        >
          {symbol}
        </div>
      ))}
    </div>
  )
}