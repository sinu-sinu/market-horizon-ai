import api from './api'
import type { CacheStatsResponse, ClearCacheRequest, ClearCacheResponse } from '@/types'

/**
 * Cache API service
 */
export const cacheService = {
  /**
   * Get cache statistics
   */
  async getStats(): Promise<CacheStatsResponse> {
    const response = await api.get<CacheStatsResponse>('/cache/stats')
    return response.data
  },

  /**
   * Clear cache entries
   */
  async clear(request: ClearCacheRequest = {}): Promise<ClearCacheResponse> {
    const response = await api.post<ClearCacheResponse>('/cache/clear', request)
    return response.data
  },

  /**
   * Clear cache by type
   */
  async clearByType(cacheType: string): Promise<ClearCacheResponse> {
    return this.clear({ cache_type: cacheType })
  },

  /**
   * Clear cache for a specific query
   */
  async clearByQuery(query: string): Promise<ClearCacheResponse> {
    return this.clear({ query })
  },

  /**
   * Clear all cache
   */
  async clearAll(): Promise<ClearCacheResponse> {
    return this.clear({})
  },

  /**
   * Cleanup expired entries
   */
  async cleanup(): Promise<ClearCacheResponse> {
    const response = await api.post<ClearCacheResponse>('/cache/cleanup')
    return response.data
  },
}

export default cacheService
