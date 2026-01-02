<script setup lang="ts">
import { useAnalysisStore } from '@/stores'
import type { QuickAction } from '@/types'

const analysisStore = useAnalysisStore()

const quickActions: QuickAction[] = [
  {
    id: 'competitor-analysis',
    label: 'Analyze top competitors in the CRM space',
    icon: 'chart',
    query: 'What are the top CRM tools for real estate?',
  },
  {
    id: 'market-positioning',
    label: 'Compare positioning of project management tools',
    icon: 'variance',
    query: 'Compare positioning of project management software',
  },
  {
    id: 'content-gaps',
    label: 'Discover content gaps in AI analytics market',
    icon: 'doc',
    query: 'What are the content gaps in AI-powered analytics tools?',
  },
  {
    id: 'niche-exploration',
    label: 'Explore niches in email marketing platforms',
    icon: 'edit',
    query: 'What niches exist in the email marketing software market?',
  },
  {
    id: 'strategic-insights',
    label: 'Get strategic insights for productivity apps',
    icon: 'dashboard',
    query: 'Strategic analysis of productivity and task management apps',
  },
  {
    id: 'pricing-comparison',
    label: 'Compare pricing strategies of SaaS tools',
    icon: 'bank',
    query: 'Analyze pricing strategies of top SaaS collaboration tools',
  },
  {
    id: 'market-trends',
    label: 'Identify emerging trends in fintech',
    icon: 'forecast',
    query: 'What are the emerging trends in fintech applications?',
  },
  {
    id: 'opportunity-analysis',
    label: 'Find market opportunities in e-commerce',
    icon: 'doc',
    query: 'What market opportunities exist in e-commerce platforms?',
  },
]

function handleAction(action: QuickAction) {
  if (analysisStore.isLoading) return
  analysisStore.analyze(action.query)
}

const iconMap: Record<string, string> = {
  chart: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 14V6l4 4 4-6 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  doc: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="3" y="2" width="10" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M6 5h4M6 8h4M6 11h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  bank: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 6l6-4 6 4M3 6v7M13 6v7M6 6v7M10 6v7M2 13h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  edit: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M11.5 2.5l2 2L5 13H3v-2l8.5-8.5z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  forecast: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 4v4l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  variance: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M8 3v10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M5 5l-2 3 2 3M11 5l2 3-2 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  dashboard: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="2" width="5" height="3" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="7" width="5" height="7" rx="1" stroke="currentColor" stroke-width="1.5"/></svg>`,
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
