import { Sparkles, Shapes, Atom, Infinity, Zap } from 'lucide-react'
import { BackgroundEffectsService } from './BackgroundEffectsService'
import { GamingEffects } from '../../components/background-effects/effects/GamingEffects'
import { MinimalEffects } from '../../components/background-effects/effects/MinimalEffects'
import { ParticleEffects } from '../../components/background-effects/effects/ParticleEffects'
import { AbstractEffects } from '../../components/background-effects/effects/AbstractEffects'
import { CasinoEffects } from '../../components/background-effects/effects/CasinoEffects'

// Synchronous registration function for immediate effect availability
const registerEffects = () => {
  const service = BackgroundEffectsService.getInstance()
  
  // Register Gaming Effects
  service.registerEffect({
    id: 'gaming',
    name: 'Gaming',
    description: 'Animated orbs, chess pieces, and sparkles',
    icon: Sparkles,
    preview: 'bg-gradient-to-br from-purple-500/20 to-pink-500/20 border-purple-400',
    component: GamingEffects,
  })

  // Register Minimal Effects  
  service.registerEffect({
    id: 'minimal',
    name: 'Minimal',
    description: 'Clean geometric shapes',
    icon: Shapes,
    preview: 'bg-gradient-to-br from-slate-100 to-slate-200 border-slate-300',
    component: MinimalEffects,
  })

  // Register Particle Effects
  service.registerEffect({
    id: 'particles', 
    name: 'Particles',
    description: 'Physics-based particles',
    icon: Atom,
    preview: 'bg-gradient-to-br from-blue-100 to-cyan-100 border-blue-300',
    component: ParticleEffects,
  })

  // Register Abstract Effects
  service.registerEffect({
    id: 'abstract',
    name: 'Abstract', 
    description: 'Mathematical symbols',
    icon: Infinity,
    preview: 'bg-gradient-to-br from-indigo-100 to-purple-100 border-indigo-300',
    component: AbstractEffects,
  })

  // Register Casino Effects
  service.registerEffect({
    id: 'casino',
    name: 'Casino',
    description: 'Enhanced floating orbs and sparkles',
    icon: Zap,
    preview: 'bg-gradient-to-br from-yellow-100 to-orange-100 border-yellow-300',
    component: CasinoEffects,
  })

  // Initialize service
  service.initialize()
  
  return service
}

// Register effects immediately and synchronously
registerEffects()

export { BackgroundEffectsService as backgroundEffectsService }