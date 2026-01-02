<script setup lang="ts">
import { ref } from 'vue'
import type { FinancialMetric } from '@/types'
import MetricCard from './MetricCard.vue'

// Mock financial metrics data
const metrics = ref<FinancialMetric[]>([
  {
    id: 'revenue',
    label: 'Revenue',
    value: '$7.8M',
    change: 12.4,
    changeLabel: '+12.4%',
    trend: 'up',
    sparklineData: [45, 52, 49, 62, 58, 71, 68, 75, 78],
  },
  {
    id: 'arr',
    label: 'ARR',
    value: '$6.5M',
    change: 8.2,
    changeLabel: '+8.2%',
    trend: 'up',
    sparklineData: [40, 42, 45, 48, 52, 55, 58, 62, 65],
  },
  {
    id: 'operating-expenses',
    label: 'Operating Expenses',
    value: '$4.8M',
    change: 3.1,
    changeLabel: '+3.1%',
    trend: 'up',
    sparklineData: [38, 40, 42, 41, 44, 45, 46, 47, 48],
  },
  {
    id: 'ebitda',
    label: 'EBITDA',
    value: '-$1M',
    change: -15.2,
    changeLabel: '-15.2%',
    trend: 'down',
    sparklineData: [20, 18, 15, 12, 14, 11, 8, 10, 8],
  },
  {
    id: 'churn-rate',
    label: 'Churn rate',
    value: '3%',
    change: -0.5,
    changeLabel: '-0.5%',
    trend: 'up',
    sparklineData: [5, 4.5, 4.2, 4, 3.8, 3.5, 3.2, 3.1, 3],
  },
  {
    id: 'nrr',
    label: 'NRR',
    value: '10%',
    change: 2.1,
    changeLabel: '+2.1%',
    trend: 'up',
    sparklineData: [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10],
  },
  {
    id: 'cash',
    label: 'Cash',
    value: '$5.6M',
    change: 5.3,
    changeLabel: '+5.3%',
    trend: 'up',
    sparklineData: [48, 50, 51, 52, 53, 54, 55, 55.5, 56],
  },
])
</script>

<template>
  <div class="metrics-grid stagger-children">
    <MetricCard v-for="metric in metrics" :key="metric.id" :metric="metric" />
  </div>
</template>

<style scoped>
.metrics-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4);
}
</style>
