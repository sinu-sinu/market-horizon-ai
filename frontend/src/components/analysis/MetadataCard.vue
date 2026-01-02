<script setup lang="ts">
import type { ReportMetadata } from '@/types'

defineProps<{
  metadata: ReportMetadata
}>()

function formatConfidence(score: number): string {
  return `${Math.round(score * 100)}%`
}

function formatTime(seconds: number): string {
  if (seconds < 60) return `${seconds}s`
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}m ${secs}s`
}
</script>

<template>
  <div class="metadata-card">
    <div class="metadata-item">
      <span class="metadata-value" :class="{ high: metadata.confidence_score >= 0.7, low: metadata.confidence_score < 0.5 }">
        {{ formatConfidence(metadata.confidence_score) }}
      </span>
      <span class="metadata-label">Confidence</span>
    </div>
    <div class="metadata-divider"></div>
    <div class="metadata-item">
      <span class="metadata-value">{{ metadata.total_sources }}</span>
      <span class="metadata-label">Sources</span>
    </div>
    <div class="metadata-divider"></div>
    <div class="metadata-item">
      <span class="metadata-value">{{ formatTime(metadata.processing_time_seconds) }}</span>
      <span class="metadata-label">Processing</span>
    </div>
  </div>
</template>

<style scoped>
.metadata-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-xl);
}

.metadata-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.metadata-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--text-dark);
}

.metadata-value.high {
  color: var(--color-success);
}

.metadata-value.low {
  color: var(--color-error);
}

.metadata-label {
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
}

.metadata-divider {
  width: 1px;
  height: 32px;
  background: var(--lumina-mist);
}
</style>
