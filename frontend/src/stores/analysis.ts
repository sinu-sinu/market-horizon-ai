import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AnalysisResult, ChatMessage } from '@/types'
import { analysisService } from '@/services'
import { useHistoryStore } from './history'

export const useAnalysisStore = defineStore('analysis', () => {
  // State
  const isLoading = ref(false)
  const currentQuery = ref<string | null>(null)
  const currentResult = ref<AnalysisResult | null>(null)
  const error = ref<string | null>(null)
  const messages = ref<ChatMessage[]>([])

  // Getters
  const hasResult = computed(() => currentResult.value !== null)

  const confidenceScore = computed(() => {
    return currentResult.value?.report_metadata.confidence_score ?? 0
  })

  const competitors = computed(() => {
    return currentResult.value?.validated_insights.competitors ?? []
  })

  const contentThemes = computed(() => {
    return currentResult.value?.validated_insights.content_themes ?? []
  })

  const positioningMap = computed(() => {
    return currentResult.value?.validated_insights.positioning_map
  })

  const recommendations = computed(() => {
    return currentResult.value?.validated_insights.content_recommendations ?? []
  })

  const qualityFlags = computed(() => {
    return currentResult.value?.quality_flags ?? []
  })

  // Actions
  async function analyze(query: string) {
    if (isLoading.value) return

    isLoading.value = true
    currentQuery.value = query
    error.value = null

    // Add user message
    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: query,
      timestamp: new Date(),
    }
    messages.value.push(userMessage)

    // Add loading assistant message
    const assistantMessage: ChatMessage = {
      id: `msg-${Date.now()}-assistant`,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isLoading: true,
    }
    messages.value.push(assistantMessage)

    try {
      const result = await analysisService.analyze({ query })
      currentResult.value = result

      // Update assistant message with result
      const lastIndex = messages.value.length - 1
      messages.value[lastIndex] = {
        ...assistantMessage,
        content: `Analysis complete for "${query}"`,
        result,
        isLoading: false,
      }

      // Add to history store
      const historyStore = useHistoryStore()
      historyStore.addToHistory({
        id: Date.now(),
        query,
        timestamp: result.report_metadata.timestamp,
        confidence_score: result.report_metadata.confidence_score,
        num_competitors: result.validated_insights.competitors.length,
      })

      return result
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Analysis failed'

      // Update assistant message with error
      const lastIndex = messages.value.length - 1
      messages.value[lastIndex] = {
        ...assistantMessage,
        content: `Analysis failed: ${error.value}`,
        isLoading: false,
      }

      console.error('Analysis failed:', e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  function setResult(result: AnalysisResult) {
    const query = result.query_text ?? result.report_metadata.query
    currentResult.value = result
    currentQuery.value = query

    // Clear existing messages and add the loaded result as messages
    messages.value = [
      {
        id: `msg-${Date.now()}-user`,
        role: 'user',
        content: query,
        timestamp: new Date(result.report_metadata.timestamp),
      },
      {
        id: `msg-${Date.now()}-assistant`,
        role: 'assistant',
        content: `Analysis complete for "${query}"`,
        timestamp: new Date(result.report_metadata.timestamp),
        result,
        isLoading: false,
      },
    ]
  }

  function clearResult() {
    currentResult.value = null
    currentQuery.value = null
    error.value = null
  }

  function clearMessages() {
    messages.value = []
    currentResult.value = null
    currentQuery.value = null
    error.value = null
  }

  return {
    // State
    isLoading,
    currentQuery,
    currentResult,
    error,
    messages,
    // Getters
    hasResult,
    confidenceScore,
    competitors,
    contentThemes,
    positioningMap,
    recommendations,
    qualityFlags,
    // Actions
    analyze,
    setResult,
    clearResult,
    clearMessages,
  }
})
