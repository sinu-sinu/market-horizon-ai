<script setup lang="ts">
import type { ContentTheme } from '@/types'

defineProps<{
  themes: ContentTheme[]
}>()

function getSentimentColor(sentiment: number): string {
  if (sentiment > 0.2) return 'var(--color-success)'
  if (sentiment < -0.2) return 'var(--color-error)'
  return 'var(--text-dark-secondary)'
}

function getSentimentLabel(sentiment: number): string {
  if (sentiment > 0.2) return 'Positive'
  if (sentiment < -0.2) return 'Negative'
  return 'Neutral'
}
</script>

<template>
  <div class="themes-section">
    <h4 class="section-title">Content Themes</h4>
    <div class="themes-list">
      <div v-for="theme in themes" :key="theme.theme" class="theme-item">
        <div class="theme-header">
          <span class="theme-name">{{ theme.theme }}</span>
          <span class="theme-frequency">{{ theme.frequency }} mentions</span>
        </div>
        <div class="theme-sentiment">
          <div class="sentiment-bar">
            <div
              class="sentiment-fill"
              :style="{
                width: `${Math.abs(theme.sentiment) * 100}%`,
                background: getSentimentColor(theme.sentiment),
              }"
            ></div>
          </div>
          <span
            class="sentiment-label"
            :style="{ color: getSentimentColor(theme.sentiment) }"
          >
            {{ getSentimentLabel(theme.sentiment) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.themes-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.themes-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.theme-item {
  padding: var(--space-3);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-lg);
}

.theme-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.theme-name {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-dark);
  text-transform: capitalize;
}

.theme-frequency {
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
}

.theme-sentiment {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.sentiment-bar {
  flex: 1;
  height: 4px;
  background: var(--lumina-mist);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.sentiment-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--transition-base);
}

.sentiment-label {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  min-width: 60px;
  text-align: right;
}
</style>
