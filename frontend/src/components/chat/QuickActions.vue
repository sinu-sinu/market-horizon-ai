<script setup lang="ts">
import { useAnalysisStore } from '@/stores'
import type { QuickAction } from '@/types'

const analysisStore = useAnalysisStore()

const quickActions: QuickAction[] = [
  {
    id: 'competitor-analysis',
    label: 'Analyze top competitors in the CRM space',
    icon: 'chart',
    query: 'What are the top CRM tools for real estate? Show competitor positioning and market share.',
  },
  {
    id: 'content-gaps',
    label: 'Discover content gaps in AI analytics market',
    icon: 'doc',
    query: 'What are the content gaps in AI-powered analytics tools? Identify high-opportunity topics.',
  },
  {
    id: 'market-positioning',
    label: 'Map competitive landscape for project management tools',
    icon: 'variance',
    query: 'Create a 2D positioning map for project management software. Who competes with whom?',
  },
  {
    id: 'theme-extraction',
    label: 'Extract themes from fintech discussions',
    icon: 'forum',
    query: 'What themes and topics are people discussing about fintech applications? Analyze Reddit and web discussions.',
  },
  {
    id: 'strategic-recommendations',
    label: 'Get content strategy for productivity apps',
    icon: 'dashboard',
    query: 'Generate specific content recommendations for productivity and task management apps with opportunity scores.',
  },
  {
    id: 'trend-analysis',
    label: 'Identify emerging trends in marketing technology',
    icon: 'forecast',
    query: 'What are the emerging trends in marketing technology? Include web search and Google Trends data.',
  },
  {
    id: 'opportunity-scoring',
    label: 'Find market opportunities in e-commerce platforms',
    icon: 'opportunity',
    query: 'What market opportunities exist in e-commerce platforms? Score each by potential impact.',
  },
  {
    id: 'competitor-intel',
    label: 'Get competitive intelligence for SaaS tools',
    icon: 'radar',
    query: 'Provide comprehensive competitive intelligence for SaaS collaboration tools including gaps and positioning.',
  },
]

function handleAction(action: QuickAction) {
  if (analysisStore.isLoading) return
  analysisStore.analyze(action.query)
}

const iconMap: Record<string, string> = {
  chart: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 14V6l4 4 4-6 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  doc: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="3" y="2" width="10" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M6 5h4M6 8h4M6 11h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  forum: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 3h12l-2 4H6l-2 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8" cy="9" r="2" stroke="currentColor" stroke-width="1.5"/></svg>`,
  opportunity: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 5v6l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  radar: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  variance: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M8 3v10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M5 5l-2 3 2 3M11 5l2 3-2 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  dashboard: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="2" width="5" height="3" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="7" width="5" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>`,
  forecast: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 4v4l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
}
</script>

<template>
  <div class="quick-actions">
    <p class="actions-hint">Choose a request below or type your own</p>
    <div class="actions-grid stagger-children">
      <button
        v-for="action in quickActions"
        :key="action.id"
        class="action-btn"
        :disabled="analysisStore.isLoading"
        @click="handleAction(action)"
      >
        <span class="action-icon" v-html="iconMap[action.icon || 'doc']"></span>
        <span class="action-label">{{ action.label }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.quick-actions {
  padding: var(--space-4) var(--space-6);
}

.actions-hint {
  font-size: var(--text-sm);
  color: var(--text-dark-secondary);
  margin-bottom: var(--space-4);
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
  max-width: 700px;
  margin: 0 auto;
}

.action-btn {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-xl);
  text-align: left;
  transition: all var(--transition-fast);
}

.action-btn:hover:not(:disabled) {
  border-color: var(--lumina-gray);
  box-shadow: var(--shadow-sm);
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--text-dark-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
}

.action-icon :deep(svg) {
  width: 16px;
  height: 16px;
}

.action-label {
  font-size: var(--text-sm);
  color: var(--text-dark);
  line-height: var(--leading-snug);
}
</style>
