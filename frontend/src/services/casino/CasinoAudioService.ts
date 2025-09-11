import { Howl } from 'howler'

export type CasinoSoundEffect = 
  | 'cardDeal' 
  | 'cardFlip' 
  | 'cardShuffle'
  | 'chipBet' 
  | 'chipCollect'
  | 'winSmall' 
  | 'winBig' 
  | 'lose'
  | 'gameStart'

interface CasinoAudioSettings {
  enabled: boolean
  volume: number
}

class CasinoAudioService {
  private sounds: Map<CasinoSoundEffect, Howl> = new Map()
  private settings: CasinoAudioSettings = {
    enabled: true,
    volume: 0.7,
  }
  private initialized = false

  constructor() {
    this.initializeSounds()
  }

  private initializeSounds() {
    const soundDefinitions: Record<CasinoSoundEffect, { src: string[]; volume: number }> = {
      cardDeal: {
        src: ['/sounds/casino/card-place-1.ogg', '/sounds/casino/card-slide-1.ogg'],
        volume: 0.6,
      },
      cardFlip: {
        src: ['/sounds/casino/card-place-2.ogg', '/sounds/casino/card-slide-2.ogg'],
        volume: 0.5,
      },
      cardShuffle: {
        src: ['/sounds/casino/card-shuffle.ogg'],
        volume: 0.4,
      },
      chipBet: {
        src: ['/sounds/casino/chip-lay-1.ogg', '/sounds/casino/chip-lay-2.ogg'],
        volume: 0.7,
      },
      chipCollect: {
        src: ['/sounds/casino/chips-handle-1.ogg', '/sounds/casino/chips-collide-1.ogg'],
        volume: 0.6,
      },
      winSmall: {
        src: ['/sounds/casino/payout-award.mp3'],
        volume: 0.8,
      },
      winBig: {
        src: ['/sounds/casino/bonus-collect-award.mp3', '/sounds/casino/magical-coin-win.mp3'],
        volume: 0.9,
      },
      lose: {
        src: ['/sounds/casino/chips-handle-3.ogg'],
        volume: 0.5,
      },
      gameStart: {
        src: ['/sounds/casino/card-fan-1.ogg'],
        volume: 0.6,
      },
    }

    Object.entries(soundDefinitions).forEach(([key, config]) => {
      const sound = new Howl({
        src: config.src,
        volume: config.volume * this.settings.volume,
        preload: true,
        html5: false,
        onloaderror: () => {
          console.warn(`Casino sound file not found: ${key}`)
        },
        onload: () => {
          console.log(`✅ Casino sound loaded: ${key}`)
        },
      })

      this.sounds.set(key as CasinoSoundEffect, sound)
    })

    this.initialized = true
    console.log('🎰 Casino audio service initialized')
  }

  public play(effect: CasinoSoundEffect): void {
    if (!this.initialized || !this.settings.enabled) {
      return
    }

    const sound = this.sounds.get(effect)
    if (sound) {
      try {
        sound.play()
        console.log(`🎰 Playing casino sound: ${effect}`)
      } catch (error) {
        console.error(`🎰 Error playing casino sound ${effect}:`, error)
      }
    } else {
      console.warn(`🎰 Casino sound not found: ${effect}`)
    }
  }

  public playCardDeal(): void {
    this.play('cardDeal')
  }

  public playCardFlip(): void {
    this.play('cardFlip')
  }

  public playCardShuffle(): void {
    this.play('cardShuffle')
  }

  public playChipBet(): void {
    this.play('chipBet')
  }

  public playChipCollect(): void {
    this.play('chipCollect')
  }

  public playWin(amount: number, betAmount: number): void {
    // Play big win sound for 3x bet or more
    const isBigWin = amount >= betAmount * 3
    this.play(isBigWin ? 'winBig' : 'winSmall')
  }

  public playLose(): void {
    this.play('lose')
  }

  public playGameStart(): void {
    this.play('gameStart')
  }

  public setVolume(volume: number): void {
    this.settings.volume = Math.max(0, Math.min(1, volume))
    
    this.sounds.forEach((sound) => {
      sound.volume(this.settings.volume)
    })
    
    console.log(`🎰 Casino audio volume set to: ${this.settings.volume}`)
  }

  public setEnabled(enabled: boolean): void {
    this.settings.enabled = enabled
    console.log(`🎰 Casino audio ${enabled ? 'enabled' : 'disabled'}`)
  }

  public getSettings(): CasinoAudioSettings {
    return { ...this.settings }
  }

  public preloadSounds(): void {
    this.sounds.forEach((sound) => {
      sound.load()
    })
    console.log('🎰 All casino sounds preloaded')
  }

  public destroy(): void {
    this.sounds.forEach((sound) => {
      sound.unload()
    })
    this.sounds.clear()
    console.log('🎰 Casino audio service destroyed')
  }
}

// Create singleton instance
export const casinoAudioService = new CasinoAudioService()

// Hook for React components  
export function useCasinoAudio() {
  return {
    playCardDeal: () => casinoAudioService.playCardDeal(),
    playCardFlip: () => casinoAudioService.playCardFlip(),
    playCardShuffle: () => casinoAudioService.playCardShuffle(),
    playChipBet: () => casinoAudioService.playChipBet(),
    playChipCollect: () => casinoAudioService.playChipCollect(),
    playWin: (amount: number, betAmount: number) => casinoAudioService.playWin(amount, betAmount),
    playLose: () => casinoAudioService.playLose(),
    playGameStart: () => casinoAudioService.playGameStart(),
    setVolume: (volume: number) => casinoAudioService.setVolume(volume),
    setEnabled: (enabled: boolean) => casinoAudioService.setEnabled(enabled),
    getSettings: () => casinoAudioService.getSettings(),
    preloadSounds: () => casinoAudioService.preloadSounds(),
  }
}

export default casinoAudioService