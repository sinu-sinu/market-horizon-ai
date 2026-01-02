<script setup lang="ts">
import type { AnalysisResult } from '@/types'
import MetadataCard from './MetadataCard.vue'
import CompetitorsList from './CompetitorsList.vue'
import ThemesList from './ThemesList.vue'
import PositioningMap from './PositioningMap.vue'
import RecommendationsList from './RecommendationsList.vue'
import QualityFlags from './QualityFlags.vue'
import DataSources from './DataSources.vue'

defineProps<{
  result: AnalysisResult
}>()

function downloadReport(result: AnalysisResult) {
  const report = generateMarkdownReport(result)
  const blob = new Blob([report], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `market-analysis-${new Date().toISOString().split('T')[0]}.md`
  a.click()
  URL.revokeObjectURL(url)
}

function generateMarkdownReport(result: AnalysisResult): string {
  const { report_metadata, validated_insights, quality_flags } = result
  let md = `# Market Analysis Report\n\n`
  md += `**Query:** ${report_metadata.query}\n\n`
  md += `**Generated:** ${new Date(report_metadata.timestamp).toLocaleString()}\n\n`
  md += `**Confidence Score:** ${Math.round(report_metadata.confidence_score * 100)}%\n\n`
  md += `---\n\n`

  md += `## Competitors Identified\n\n`
  validated_insights.competitors.forEach((c) => {
    md += `- ${c}\n`
  })
  md += `\n`

  md += `## Content Themes\n\n`
  validated_insights.content_themes.forEach((t) => {
    md += `- **${t.theme}** (${t.frequency} mentions, sentiment: ${t.sentiment.toFixed(2)})\n`
  })
  md += `\n`

  if (validated_insights.content_recommendations.length > 0) {
    md += `## Content Recommendations\n\n`
    validated_insights.content_recommendations.forEach((r) => {
      md += `### ${r.topic}\n`
      md += `- Priority: ${r.priority}\n`
      md += `- Opportunity Score: ${r.opportunity_score.toFixed(1)}\n`
      if (r.recommended_format) md += `- Format: ${r.recommended_format}\n`
      md += `\n`
    })
  }

  if (quality_flags.length > 0) {
    md += `## Quality Notes\n\n`
    quality_flags.forEach((f) => {
      md += `- [${f.type.toUpperCase()}] ${f.message} (${f.agent})\n`
    })
  }

  return md
}
</script>

<template>
  <div class="analysis-result stagger-children">
    <MetadataCard :metadata="result.report_metadata" />

    <CompetitorsList
      v-if="result.validated_insights.competitors.length > 0"
      :competitors="result.validated_insights.competitors"
    />

    <ThemesList
      v-if="result.validated_insights.content_themes.length > 0"
      :themes="result.validated_insights.content_themes"
    />

    <PositioningMap
      v-if="result.validated_insights.positioning_map?.companies"
      :positioning-map="result.validated_insights.positioning_map"
    />

    <RecommendationsList
      v-if="result.validated_insights.content_recommendations.length > 0"
      :recommendations="result.validated_insights.content_recommendations"
    />

    <DataSources />

    <QualityFlags :flags="result.quality_flags" />

    <div class="result-actions">
      <button class="action-btn primary" @click="downloadReport(result)">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path
            d="M8 2v8M5 7l3 3 3-3M3 12v1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        Download Report
      </button>
    </div>
  </div>
</template>

<style scoped>
.analysis-result {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.result-actions {
  display: flex;
  gap: var(--space-3);
  padding-top: var(--space-2);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  border-radius: var(--radius-lg);
  transition: all var(--transition-fast);
}

.action-btn.primary {
  background: var(--lumina-black);
  color: var(--lumina-white);
}

.action-btn.primary:hover {
  background: var(--lumina-charcoal);
  transform: translateY(-1px);
}
</style>
