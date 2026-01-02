import api from './api'
import type { QueryHistoryItem, AnalysisResult } from '@/types'

/**
 * History API service
 */
export const historyService = {
  /**
   * Get recent query history
   */
  async getRecent(limit: number = 5): Promise<QueryHistoryItem[]> {
    const response = await api.get<QueryHistoryItem[]>('/history/recent', {
      params: { limit },
    })
    return response.data
  },

  /**
   * Get a specific query result by ID
   */
  async getById(queryId: number): Promise<AnalysisResult> {
    const response = await api.get<AnalysisResult>(`/history/${queryId}`)
    return response.data
  },

  /**
   * Get the most recent query result
   */
  async getLatest(): Promise<AnalysisResult> {
    const response = await api.get<AnalysisResult>('/history/latest')
    return response.data
  },
}

export default historyService
