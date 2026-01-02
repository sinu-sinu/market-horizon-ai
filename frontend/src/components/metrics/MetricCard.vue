<script setup lang="ts">
import type { FinancialMetric } from '@/types'
import SparklineChart from './SparklineChart.vue'

defineProps<{
  metric: FinancialMetric
}>()
</script>

<template>
  <div class="metric-card">
    <div class="metric-content">
      <span class="metric-value">{{ metric.value }}</span>
      <span class="metric-label">{{ metric.label }}</span>
    </div>
    <div class="metric-chart">
      <SparklineChart
        :data="metric.sparklineData"
        :trend="metric.trend"
        :width="70"
        :height="28"
      />
    </div>
  </div>
</template>

<style scoped>
.metric-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: var(--bg-tertiary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--lumina-graphite);
  transition: all var(--transition-fast);
}

.metric-card:hover {
  border-color: var(--lumina-gray);
}

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.metric-label {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.metric-chart {
  flex-shrink: 0;
}
</style>
