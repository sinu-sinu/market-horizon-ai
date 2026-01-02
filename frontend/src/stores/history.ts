import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { QueryHistoryItem, AnalysisResult } from '@/types'
import { historyService } from '@/services'

export const useHistoryStore = defineStore('history', () => {
  // State
  const recentQueries = ref<QueryHistoryItem[]>([])
  const isLoading = ref(false)
  const selectedQueryId = ref<number | null>(null)
  const error = ref<string | null>(null)

  // Actions
  async function fetchRecent(limit: number = 5) {
    isLoading.value = true
    error.value = null
    try {
      recentQueries.value = await historyService.getRecent(limit)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch history'
      console.error('Failed to fetch recent queries:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchQueryById(queryId: number): Promise<AnalysisResult | null> {
    isLoading.value = true
    error.value = null
    try {
      const result = await historyService.getById(queryId)
      selectedQueryId.value = queryId
      return result
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch query'
      console.error('Failed to fetch query:', e)
      return null
    } finally {
      isLoading.value = false
    }
  }

  function selectQuery(queryId: number | null) {
    selectedQueryId.value = queryId
  }

  function addToHistory(item: QueryHistoryItem) {
    // Add to the beginning of the list
    recentQueries.value.unshift(item)
    // Keep only the most recent 10
    if (recentQueries.value.length > 10) {
      recentQueries.value.pop()
    }
  }

  return {
    // State
    recentQueries,
    isLoading,
    selectedQueryId,
    error,
    // Actions
    fetchRecent,
    fetchQueryById,
    selectQuery,
    addToHistory,
  }
})
