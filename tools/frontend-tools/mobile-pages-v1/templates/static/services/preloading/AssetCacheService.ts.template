/**
 * Asset Cache Service for persistent caching between app restarts
 * Uses IndexedDB for large binary assets and localStorage for metadata
 */

interface CacheEntry {
  url: string
  data: Blob
  timestamp: number
  contentType: string
  size: number
}

interface CacheMetadata {
  version: string
  totalSize: number
  lastCleanup: number
  entries: Record<string, {
    timestamp: number
    size: number
    contentType: string
  }>
}

export class AssetCacheService {
  private dbName = 'chess-asset-cache'
  private dbVersion = 1
  private storeName = 'assets'
  private metadataKey = 'asset-cache-metadata'
  private maxCacheSize = 50 * 1024 * 1024 // 50MB max cache size
  private maxAge = 7 * 24 * 60 * 60 * 1000 // 7 days max age
  private db: IDBDatabase | null = null

  /**
   * Initialize the IndexedDB cache
   */
  async initialize(): Promise<void> {
    if (this.db) return

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion)
      
      request.onerror = () => reject(new Error('Failed to open IndexedDB'))
      
      request.onsuccess = () => {
        this.db = request.result
        resolve()
      }
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        
        if (!db.objectStoreNames.contains(this.storeName)) {
          const store = db.createObjectStore(this.storeName, { keyPath: 'url' })
          store.createIndex('timestamp', 'timestamp', { unique: false })
        }
      }
    })
  }

  /**
   * Get cached asset or return null if not found/expired
   */
  async getCachedAsset(url: string): Promise<Blob | null> {
    if (!this.db) await this.initialize()
    
    return new Promise((resolve) => {
      if (!this.db) {
        resolve(null)
        return
      }

      const transaction = this.db.transaction([this.storeName], 'readonly')
      const store = transaction.objectStore(this.storeName)
      const request = store.get(url)
      
      request.onsuccess = () => {
        const entry: CacheEntry | undefined = request.result
        
        if (!entry) {
          resolve(null)
          return
        }
        
        // Check if entry is expired
        const isExpired = Date.now() - entry.timestamp > this.maxAge
        if (isExpired) {
          // Cleanup expired entry
          this.removeFromCache(url)
          resolve(null)
          return
        }
        
        resolve(entry.data)
      }
      
      request.onerror = () => resolve(null)
    })
  }

  /**
   * Cache asset with metadata tracking
   */
  async cacheAsset(url: string, data: Blob, contentType: string): Promise<void> {
    if (!this.db) await this.initialize()
    
    const entry: CacheEntry = {
      url,
      data,
      timestamp: Date.now(),
      contentType,
      size: data.size
    }

    // Check cache size limits before adding
    await this.enforeCacheLimits(entry.size)

    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'))
        return
      }

      const transaction = this.db.transaction([this.storeName], 'readwrite')
      const store = transaction.objectStore(this.storeName)
      const request = store.put(entry)
      
      request.onsuccess = () => {
        this.updateMetadata(url, entry)
        resolve()
      }
      
      request.onerror = () => reject(new Error(`Failed to cache ${url}`))
    })
  }

  /**
   * Remove asset from cache
   */
  private async removeFromCache(url: string): Promise<void> {
    if (!this.db) return

    return new Promise((resolve) => {
      if (!this.db) {
        resolve()
        return
      }

      const transaction = this.db.transaction([this.storeName], 'readwrite')
      const store = transaction.objectStore(this.storeName)
      const request = store.delete(url)
      
      request.onsuccess = () => {
        this.removeFromMetadata(url)
        resolve()
      }
      
      request.onerror = () => resolve() // Fail silently for cleanup operations
    })
  }

  /**
   * Enforce cache size limits by removing oldest entries
   */
  private async enforeCacheLimits(newEntrySize: number): Promise<void> {
    const metadata = this.getMetadata()
    
    // Check if adding new entry would exceed limits
    if (metadata.totalSize + newEntrySize <= this.maxCacheSize) {
      return
    }


    // Get all entries sorted by age (oldest first)
    const entries = Object.entries(metadata.entries)
      .sort(([, a], [, b]) => a.timestamp - b.timestamp)

    // Remove entries until we have enough space
    let spaceFreed = 0
    for (const [url] of entries) {
      if (spaceFreed >= newEntrySize) break
      
      const entrySize = metadata.entries[url]?.size || 0
      await this.removeFromCache(url)
      spaceFreed += entrySize
      
    }
  }

  /**
   * Fetch asset with caching
   */
  async fetchWithCache(url: string): Promise<Blob> {
    // Try to get from cache first
    const cached = await this.getCachedAsset(url)
    if (cached) {
      return cached
    }

    
    // Fetch from network
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.status}`)
    }

    const data = await response.blob()
    const contentType = response.headers.get('content-type') || 'application/octet-stream'
    
    // Cache for next time (don't await to avoid blocking)
    this.cacheAsset(url, data, contentType).catch(error => {
      console.warn(`⚠️ Failed to cache ${url}:`, error)
    })

    return data
  }

  /**
   * Preload multiple assets with caching
   */
  async preloadAssets(urls: string[]): Promise<{
    cached: string[]
    fetched: string[]
    failed: string[]
  }> {
    const cached: string[] = []
    const fetched: string[] = []
    const failed: string[] = []

    const promises = urls.map(async (url) => {
      try {
        const cachedAsset = await this.getCachedAsset(url)
        if (cachedAsset) {
          cached.push(url)
          return
        }

        // Fetch and cache
        await this.fetchWithCache(url)
        fetched.push(url)
      } catch (error) {
        console.error(`❌ Failed to preload ${url}:`, error)
        failed.push(url)
      }
    })

    await Promise.allSettled(promises)
    
    
    return { cached, fetched, failed }
  }

  /**
   * Clear all cached assets
   */
  async clearCache(): Promise<void> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'))
        return
      }

      const transaction = this.db.transaction([this.storeName], 'readwrite')
      const store = transaction.objectStore(this.storeName)
      const request = store.clear()
      
      request.onsuccess = () => {
        localStorage.removeItem(this.metadataKey)
        resolve()
      }
      
      request.onerror = () => reject(new Error('Failed to clear cache'))
    })
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    totalSize: number
    entryCount: number
    sizeFormatted: string
    maxSizeFormatted: string
    utilization: number
  } {
    const metadata = this.getMetadata()
    const totalSize = metadata.totalSize
    const entryCount = Object.keys(metadata.entries).length
    
    return {
      totalSize,
      entryCount,
      sizeFormatted: this.formatBytes(totalSize),
      maxSizeFormatted: this.formatBytes(this.maxCacheSize),
      utilization: (totalSize / this.maxCacheSize) * 100
    }
  }

  /**
   * Update metadata in localStorage
   */
  private updateMetadata(url: string, entry: CacheEntry): void {
    const metadata = this.getMetadata()
    
    // Remove old entry size if it existed
    const oldSize = metadata.entries[url]?.size || 0
    metadata.totalSize -= oldSize
    
    // Add new entry
    metadata.entries[url] = {
      timestamp: entry.timestamp,
      size: entry.size,
      contentType: entry.contentType
    }
    metadata.totalSize += entry.size
    
    localStorage.setItem(this.metadataKey, JSON.stringify(metadata))
  }

  /**
   * Remove entry from metadata
   */
  private removeFromMetadata(url: string): void {
    const metadata = this.getMetadata()
    const entrySize = metadata.entries[url]?.size || 0
    
    delete metadata.entries[url]
    metadata.totalSize -= entrySize
    
    localStorage.setItem(this.metadataKey, JSON.stringify(metadata))
  }

  /**
   * Get metadata from localStorage
   */
  private getMetadata(): CacheMetadata {
    const stored = localStorage.getItem(this.metadataKey)
    
    if (stored) {
      try {
        return JSON.parse(stored)
      } catch (error) {
        console.warn('Failed to parse cache metadata, resetting')
      }
    }

    // Return default metadata
    const defaultMetadata: CacheMetadata = {
      version: '1.0.0',
      totalSize: 0,
      lastCleanup: Date.now(),
      entries: {}
    }
    
    localStorage.setItem(this.metadataKey, JSON.stringify(defaultMetadata))
    return defaultMetadata
  }

  /**
   * Format bytes for human-readable display
   */
  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B'
    
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }
}

// Singleton instance for app-wide use
export const assetCacheService = new AssetCacheService()