<script setup lang="ts">
import { onMounted } from 'vue'
import { useHistoryStore, useAnalysisStore } from '@/stores'
import { useRouter, useRoute } from 'vue-router'

const historyStore = useHistoryStore()
const analysisStore = useAnalysisStore()
const router = useRouter()
const route = useRoute()

onMounted(() => {
  console.log('HistoryView mounted, route:', route.path)
  historyStore.fetchRecent(20)
})

async function loadQuery(queryId: number) {
  const result = await historyStore.fetchQueryById(queryId)
  if (result) {
    analysisStore.setResult(result)
    router.push('/')
  }
}

function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleString()
}

function formatConfidence(score: number | null): string {
  if (score === null) return '-'
  return `${Math.round(score * 100)}%`
}
</script>

<template>
  <div class="history-view">
    <header class="view-header">
      <h1 class="view-title">Query History</h1>
      <p class="view-subtitle">View and reload your previous market analyses</p>
    </header>

    <div class="history-list">
      <div
        v-for="query in historyStore.recentQueries"
        :key="query.id"
        class="history-item"
        @click="loadQuery(query.id)"
      >
        <div class="item-main">
          <span class="item-query">{{ query.query }}</span>
          <span class="item-time">{{ formatTimestamp(query.timestamp) }}</span>
        </div>
        <div class="item-meta">
          <span class="meta-item">
            <strong>{{ formatConfidence(query.confidence_score) }}</strong>
            confidence
          </span>
          <span class="meta-item">
            <strong>{{ query.num_competitors || 0 }}</strong>
            competitors
          </span>
        </div>
      </div>

      <div v-if="historyStore.recentQueries.length === 0" class="empty-state">
        <p>No queries yet. Run your first analysis to see history here.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-view {
  padding: var(--space-8);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
  background: var(--bg-chat);
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
}

.view-header {
  margin-bottom: var(--space-8);
}

.view-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-dark);
  margin-bottom: var(--space-2);
}

.view-subtitle {
  font-size: var(--text-base);
  color: var(--text-dark-secondary);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.history-item {
  padding: var(--space-4);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.history-item:hover {
  border-color: var(--lumina-gray);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.item-main {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

.item-query {
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--text-dark);
  flex: 1;
}

.item-time {
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
  white-space: nowrap;
}

.item-meta {
  display: flex;
  gap: var(--space-4);
}

.meta-item {
  font-size: var(--text-sm);
  color: var(--text-dark-secondary);
}

.meta-item strong {
  color: var(--text-dark);
  font-weight: var(--font-semibold);
}

.empty-state {
  text-align: center;
  padding: var(--space-12);
  color: var(--text-dark-secondary);
}
</style>
