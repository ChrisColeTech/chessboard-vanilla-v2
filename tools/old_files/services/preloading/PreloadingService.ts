import { preload } from 'react-dom'
import { PIECE_SETS } from '../../constants/pieces.constants'
import { assetCacheService } from './AssetCacheService'

export interface LoadingPriority {
  critical: string[]    // Must load before app access (selected piece set, theme)
  important: string[]   // Should load early (audio files if enabled)
  background: string[]  // Can load after app ready (other piece sets)
}

export interface LoadingProgress {
  stage: string
  progress: number  // 0-100
  loaded: number
  total: number
  status: string
}

export interface LoadingResults {
  successful: string[]
  failed: string[]
  totalTime: number
}

/**
 * Modern asset preloading service using 2024 React best practices
 * Coordinates with Zustand store for user-preference-driven loading
 */
export class PreloadingService {
  private progressCallback?: (progress: LoadingProgress) => void
  private loadingStartTime: number = 0

  /**
   * Set callback for real-time progress updates
   */
  onProgress(callback: (progress: LoadingProgress) => void) {
    this.progressCallback = callback
  }

  /**
   * Get assets to preload based on user preferences
   */
  getAssetsToPreload(userPrefs: {
    selectedPieceSet?: keyof typeof PIECE_SETS
    audioEnabled?: boolean
    currentTheme?: string
    lastVisited?: Date
  }): LoadingPriority {
    const { selectedPieceSet = 'classic', audioEnabled = false } = userPrefs

    return {
      critical: this.generatePieceSetPaths(selectedPieceSet),
      important: audioEnabled ? this.getAudioFiles() : [],
      background: this.getOtherPieceSets(selectedPieceSet)
    }
  }

  /**
   * Generate file paths for a specific piece set
   */
  private generatePieceSetPaths(pieceSet: keyof typeof PIECE_SETS): string[] {
    const pieces = ['wK', 'wQ', 'wR', 'wB', 'wN-left', 'wN-right', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN-left', 'bN-right', 'bP']
    return pieces.map(piece => `/assets/sets/${pieceSet}/${piece}.svg`)
  }

  /**
   * Get audio files based on user preferences
   */
  private getAudioFiles(): string[] {
    return [
      '/assets/audio/move.mp3',
      '/assets/audio/capture.mp3', 
      '/assets/audio/check.mp3',
      '/assets/audio/ui-click.mp3'
    ]
  }

  /**
   * Get all piece sets except the selected one
   */
  private getOtherPieceSets(excludeSet: keyof typeof PIECE_SETS): string[] {
    const allSets = Object.keys(PIECE_SETS) as Array<keyof typeof PIECE_SETS>
    const otherSets = allSets.filter(set => set !== excludeSet)
    
    return otherSets.flatMap(set => this.generatePieceSetPaths(set))
  }

  /**
   * Preload image with Promise-based coordination and caching
   */
  private async preloadImage(src: string): Promise<HTMLImageElement> {
    try {
      // Try to get from persistent cache first
      const cachedBlob = await assetCacheService.fetchWithCache(src)
      const objectUrl = URL.createObjectURL(cachedBlob)
      
      return new Promise((resolve, reject) => {
        const img = new Image()
        img.onload = () => {
          // Keep object URL for this session, cleanup will happen on page unload
          resolve(img)
        }
        img.onerror = img.onabort = () => {
          URL.revokeObjectURL(objectUrl)
          reject(new Error(`Failed to load cached ${src}`))
        }
        img.src = objectUrl
      })
    } catch (error) {
      // Fallback to direct loading if cache fails
      console.warn(`Cache failed for ${src}, falling back to direct load:`, error)
      
      return new Promise((resolve, reject) => {
        const img = new Image()
        img.onload = () => resolve(img)
        img.onerror = img.onabort = () => reject(new Error(`Failed to load ${src}`))
        img.src = src
      })
    }
  }

  /**
   * Load with timeout for network resilience
   */
  private loadWithTimeout<T>(promise: Promise<T>, timeout: number): Promise<T> {
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), timeout)
    })
    
    return Promise.race([promise, timeoutPromise])
  }

  /**
   * Preload critical assets - blocks app initialization
   */
  async preloadCritical(assets: string[]): Promise<LoadingResults> {
    if (assets.length === 0) {
      return { successful: [], failed: [], totalTime: 0 }
    }

    this.emitProgress('critical', 0, 0, assets.length, 'Loading critical assets...')
    
    const startTime = Date.now()

    // Initialize cache service
    await assetCacheService.initialize()

    // Use cache-aware bulk preloading
    const { cached, fetched, failed } = await assetCacheService.preloadAssets(assets)
    const successful = [...cached, ...fetched]

    // Use React's official preload API for immediate availability
    successful.forEach(asset => {
      try {
        preload(asset, { as: 'image' })
      } catch (error) {
        console.warn('React preload failed for:', asset, error)
      }
    })

    // Update progress based on results
    this.emitProgress('critical', 65, successful.length, assets.length, 
      `Loaded ${successful.length}/${assets.length} assets (${cached.length} cached)`)
    
    return {
      successful,
      failed,
      totalTime: Date.now() - startTime
    }
  }

  /**
   * Preload important assets - parallel with app render
   */
  async preloadImportant(assets: string[]): Promise<LoadingResults> {
    if (assets.length === 0) {
      this.emitProgress('important', 85, 0, 0, 'Skipping audio (disabled)')
      return { successful: [], failed: [], totalTime: 0 }
    }

    this.emitProgress('important', 65, 0, assets.length, 'Loading audio system...')
    
    const successful: string[] = []
    const failed: string[] = []
    const startTime = Date.now()

    // Don't await - load in background
    const promises = assets.map(async (asset, index) => {
      try {
        // For audio files, we might need different preloading strategy
        if (asset.includes('.mp3') || asset.includes('.wav')) {
          const audio = new Audio()
          audio.preload = 'auto'
          audio.src = asset
          await new Promise((resolve, reject) => {
            audio.addEventListener('canplaythrough', resolve, { once: true })
            audio.addEventListener('error', reject, { once: true })
          })
        } else {
          await this.loadWithTimeout(this.preloadImage(asset), 3000)
        }
        successful.push(asset)
        this.emitProgress('important', 65 + Math.round((index + 1) / assets.length * 20), index + 1, assets.length, `Loaded ${asset.split('/').pop()}`)
      } catch (error) {
        console.warn('Failed to preload important asset:', asset, error)
        failed.push(asset)
      }
    })

    Promise.allSettled(promises) // Don't await - continues in background
    
    return {
      successful,
      failed,
      totalTime: Date.now() - startTime
    }
  }

  /**
   * Preload background assets - when browser idle
   */
  preloadBackground(assets: string[]): Promise<LoadingResults> {
    return new Promise((resolve) => {
      const successful: string[] = []
      const failed: string[] = []
      const startTime = Date.now()

      if (assets.length === 0) {
        this.emitProgress('background', 100, 0, 0, 'Ready to play!')
        resolve({ successful, failed, totalTime: 0 })
        return
      }

      this.emitProgress('background', 85, 0, assets.length, 'Loading additional piece sets...')

      // Use requestIdleCallback for background loading
      const loadInIdle = () => {
        if ('requestIdleCallback' in window) {
          requestIdleCallback(async () => {
            const promises = assets.map(async (asset) => {
              try {
                await this.preloadImage(asset)
                successful.push(asset)
              } catch (error) {
                failed.push(asset)
              }
            })

            await Promise.allSettled(promises)
            this.emitProgress('background', 100, assets.length, assets.length, 'Ready to play!')
            resolve({ successful, failed, totalTime: Date.now() - startTime })
          })
        } else {
          // Fallback for browsers without requestIdleCallback
          setTimeout(async () => {
            const promises = assets.slice(0, 10).map(async (asset) => {
              try {
                await this.preloadImage(asset)
                successful.push(asset)
              } catch (error) {
                failed.push(asset)
              }
            })

            await Promise.allSettled(promises)
            this.emitProgress('background', 100, Math.min(10, assets.length), assets.length, 'Ready to play!')
            resolve({ successful, failed, totalTime: Date.now() - startTime })
          }, 1000)
        }
      }

      loadInIdle()
    })
  }

  /**
   * Complete preloading sequence with real progress coordination
   */
  async preloadAll(userPrefs: {
    selectedPieceSet?: keyof typeof PIECE_SETS
    audioEnabled?: boolean
    currentTheme?: string
    lastVisited?: Date
  }): Promise<{
    critical: LoadingResults
    important: LoadingResults
    background: LoadingResults
    totalTime: number
  }> {
    this.loadingStartTime = Date.now()
    
    const assets = this.getAssetsToPreload(userPrefs)
    
    // Stage 1: Critical assets (blocks app)
    this.emitProgress('initialization', 0, 0, 1, 'Restoring preferences...')
    await new Promise(resolve => setTimeout(resolve, 100)) // Simulate store rehydration
    
    this.emitProgress('initialization', 20, 1, 1, 'Preferences restored')
    
    // Stage 2: Critical asset loading
    const critical = await this.preloadCritical(assets.critical)
    
    // Stage 3: Important assets (parallel)
    const important = await this.preloadImportant(assets.important)
    
    // Stage 4: Background assets (idle time)
    const background = this.preloadBackground(assets.background)
    
    return {
      critical,
      important,
      background: await background,
      totalTime: Date.now() - this.loadingStartTime
    }
  }

  /**
   * Emit progress updates to subscribers
   */
  private emitProgress(stage: string, progress: number, loaded: number, total: number, status: string) {
    if (this.progressCallback) {
      this.progressCallback({
        stage,
        progress: Math.min(100, Math.max(0, progress)),
        loaded,
        total,
        status
      })
    }
  }
}

// Singleton instance for app-wide use
export const preloadingService = new PreloadingService()