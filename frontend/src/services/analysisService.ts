import api from './api'
import type { AnalyzeRequest, AnalysisResult } from '@/types'

/**
 * Analysis API service
 */
export const analysisService = {
  /**
   * Run market analysis pipeline
   */
  async analyze(request: AnalyzeRequest): Promise<AnalysisResult> {
    const response = await api.post<AnalysisResult>('/analyze', request)
    return response.data
  },
}

export default analysisService
