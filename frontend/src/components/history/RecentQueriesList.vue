<script setup lang="ts">
import { useHistoryStore, useAnalysisStore } from '@/stores'

defineProps<{
  collapsed?: boolean
}>()

const historyStore = useHistoryStore()
const analysisStore = useAnalysisStore()

async function loadQuery(queryId: number) {
  const result = await historyStore.fetchQueryById(queryId)
  if (result) {
    analysisStore.setResult(result)
  }
}

function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)

  if (hours < 1) return 'Just now'
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString()
}

function truncateQuery(query: string, maxLength: number = 30): string {
  if (query.length <= maxLength) return query
  return query.substring(0, maxLength) + '...'
}
</script>

<template>
  <div class="recent-queries" :class="{ collapsed }">
    <Transition name="fade">
      <div v-if="!collapsed" class="section-header">
        <span class="section-title">Recent</span>
      </div>
    </Transition>

    <div class="queries-list" v-if="historyStore.recentQueries.length > 0">
      <button
        v-for="query in historyStore.recentQueries.slice(0, 5)"
        :key="query.id"
        class="query-item"
        :class="{
          collapsed,
          active: historyStore.selectedQueryId === query.id
        }"
        @click="loadQuery(query.id)"
        :title="collapsed ? query.query : undefined"
      >
        <template v-if="!collapsed">
          <span class="query-text">{{ truncateQuery(query.query) }}</span>
          <span class="query-time">{{ formatTimestamp(query.timestamp) }}</span>
        </template>
        <template v-else>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path
              d="M7.5 3.75h6M7.5 9h6M7.5 14.25h6M4.5 3.75h.008M4.5 9h.008M4.5 14.25h.008"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </template>
      </button>
    </div>

    <div v-else-if="!collapsed" class="empty-state">
      <span>No recent queries</span>
    </div>
  </div>
</template>

<style scoped>
.recent-queries {
  padding: var(--space-2) var(--space-2);
}

.recent-queries.collapsed {
  padding: var(--space-2);
}

.section-header {
  padding: var(--space-2) var(--space-2);
  margin-bottom: var(--space-1);
}

.section-title {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.queries-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.query-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  text-align: left;
  transition: all var(--transition-fast);
  width: 100%;
}

.query-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.query-item.active {
  background: var(--bg-tertiary);
  color: var(--lumina-lime);
}

.query-item.collapsed {
  justify-content: center;
  padding: var(--space-2);
}

.query-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.query-time {
  font-size: var(--text-xs);
  color: var(--text-muted);
  flex-shrink: 0;
  margin-left: var(--space-2);
}

.empty-state {
  padding: var(--space-4);
  text-align: center;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-fast);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
