<script setup lang="ts">
import type { QualityFlag } from '@/types'

defineProps<{
  flags: QualityFlag[]
}>()

function getIcon(type: string): string {
  switch (type) {
    case 'error':
      return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 5v3M8 10h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`
    case 'warning':
      return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2l6 10H2L8 2z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M8 6v2M8 10h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`
    default:
      return `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 7v3M8 5h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`
  }
}

function getColorClass(type: string): string {
  switch (type) {
    case 'error':
      return 'type-error'
    case 'warning':
      return 'type-warning'
    default:
      return 'type-info'
  }
}
</script>

<template>
  <div v-if="flags.length > 0" class="quality-flags-section">
    <h4 class="section-title">Quality Insights</h4>
    <div class="flags-list">
      <div
        v-for="(flag, index) in flags"
        :key="index"
        class="flag-item"
        :class="getColorClass(flag.type)"
      >
        <span class="flag-icon" v-html="getIcon(flag.type)"></span>
        <div class="flag-content">
          <span class="flag-message">{{ flag.message }}</span>
          <span class="flag-agent">{{ flag.agent }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quality-flags-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.flags-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.flag-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
}

.flag-item.type-error {
  background: var(--color-error-bg);
  color: var(--color-error);
}

.flag-item.type-warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.flag-item.type-info {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.flag-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 2px;
}

.flag-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.flag-message {
  font-size: var(--text-sm);
  color: var(--text-dark);
}

.flag-agent {
  font-size: var(--text-xs);
  opacity: 0.7;
  text-transform: capitalize;
}
</style>
