<script setup lang="ts">
import type { ContentRecommendation } from '@/types'

defineProps<{
  recommendations: ContentRecommendation[]
}>()

function getPriorityColor(priority: string): string {
  switch (priority) {
    case 'high':
      return 'var(--color-error)'
    case 'medium':
      return 'var(--color-warning)'
    default:
      return 'var(--text-dark-secondary)'
  }
}

function getScoreWidth(score: number): string {
  return `${Math.min(score * 10, 100)}%`
}
</script>

<template>
  <div class="recommendations-section">
    <h4 class="section-title">Content Recommendations</h4>
    <div class="recommendations-list">
      <div
        v-for="rec in recommendations"
        :key="rec.topic"
        class="recommendation-item"
      >
        <div class="rec-header">
          <span class="rec-topic">{{ rec.topic }}</span>
          <span
            class="rec-priority"
            :style="{ color: getPriorityColor(rec.priority) }"
          >
            {{ rec.priority }}
          </span>
        </div>

        <div class="rec-meta">
          <span v-if="rec.recommended_format" class="rec-format">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <rect x="2" y="2" width="10" height="10" rx="1" stroke="currentColor" stroke-width="1.2" />
              <path d="M5 5h4M5 7h4M5 9h2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
            </svg>
            {{ rec.recommended_format }}
          </span>
          <span v-if="rec.effort_level" class="rec-effort">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.2" />
              <path d="M7 4v3l2 1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
            </svg>
            {{ rec.effort_level }} effort
          </span>
        </div>

        <div class="rec-score">
          <span class="score-label">Opportunity</span>
          <div class="score-bar">
            <div
              class="score-fill"
              :style="{ width: getScoreWidth(rec.opportunity_score) }"
            ></div>
          </div>
          <span class="score-value">{{ rec.opportunity_score.toFixed(1) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recommendations-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.recommendation-item {
  padding: var(--space-3);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-lg);
}

.rec-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.rec-topic {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-dark);
}

.rec-priority {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rec-meta {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

.rec-format,
.rec-effort {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
}

.rec-score {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.score-label {
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
  min-width: 70px;
}

.score-bar {
  flex: 1;
  height: 6px;
  background: var(--lumina-mist);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: var(--lumina-lime);
  border-radius: var(--radius-full);
  transition: width var(--transition-base);
}

.score-value {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  color: var(--text-dark);
  min-width: 30px;
  text-align: right;
}
</style>
