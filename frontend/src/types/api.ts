// API request/response types

import type { AnalysisResult } from './analysis'

// Request types
export interface AnalyzeRequest {
  query: string
  parameters?: Record<string, unknown>
}

export interface ClearCacheRequest {
  cache_type?: string
  query?: string
}

// Response types
export interface QueryHistoryItem {
  id: number
  query: string
  timestamp: string
  confidence_score: number | null
  num_competitors: number | null
}

export interface CacheTypeStats {
  type: string
  count: number
  hits: number
}

export interface CacheStatsResponse {
  stats: Record<string, number>
  hit_rate: string
  total_entries_valid: number
  total_entries_all: number
  total_size_bytes: number
  total_size_mb: number
  by_type: CacheTypeStats[]
}

export interface ClearCacheResponse {
  deleted: number
  message: string
}

export interface ApiHealthResponse {
  name: string
  version: string
  status: string
}

// Error response
export interface ApiError {
  detail: string
}

// Re-export AnalysisResult for convenience
export type { AnalysisResult }
