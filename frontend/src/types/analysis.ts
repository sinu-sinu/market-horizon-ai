// Analysis-related TypeScript interfaces
// Matches Python data structures from quality_agent.py

export interface ContentTheme {
  theme: string
  frequency: number
  sentiment: number
  key_phrases?: string[]
}

export interface CompanyPosition {
  x: number
  y: number
  rationale?: string
}

export interface OpportunityZone {
  coordinates: { x: number; y: number }
  description?: string
  rationale?: string
  opportunity_score?: number
}

export interface PositioningMap {
  dimensions?: {
    x_axis: string
    y_axis: string
  }
  companies?: Record<string, CompanyPosition>
  opportunity_zones?: OpportunityZone[]
}

export interface ContentRecommendation {
  topic: string
  priority: 'high' | 'medium' | 'low'
  opportunity_score: number
  search_volume_monthly?: number
  competitor_coverage?: string
  recommended_format?: string
  effort_level?: 'low' | 'medium' | 'high'
}

export interface QualityFlag {
  type: 'warning' | 'info' | 'error'
  message: string
  agent: string
}

export interface AgentError {
  agent: string
  error: string
  timestamp: string
  fallback_used: boolean
}

export interface ReportMetadata {
  query: string
  timestamp: string
  total_sources: number
  processing_time_seconds: number
  confidence_score: number
  api_calls?: number
  total_tokens?: number
  errors?: AgentError[]
}

export interface ValidatedInsights {
  competitors: string[]
  content_themes: ContentTheme[]
  positioning_map?: PositioningMap
  content_recommendations: ContentRecommendation[]
  strategic_recommendations: string[]
}

export interface SourceAttribution {
  total_sources?: number
  source_breakdown?: Record<string, number>
  date_range?: string
  trends_data_available?: boolean
  discussions_available?: boolean
}

export interface AnalysisResult {
  report_metadata: ReportMetadata
  validated_insights: ValidatedInsights
  quality_flags: QualityFlag[]
  source_attribution?: SourceAttribution
  query_text?: string
}
