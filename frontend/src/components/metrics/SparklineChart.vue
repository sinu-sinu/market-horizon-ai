<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  data: number[]
  trend: 'up' | 'down' | 'neutral'
  width?: number
  height?: number
}>()

const width = props.width ?? 80
const height = props.height ?? 32

const pathD = computed(() => {
  if (!props.data || props.data.length < 2) return ''

  const min = Math.min(...props.data)
  const max = Math.max(...props.data)
  const range = max - min || 1
  const padding = 2

  const points = props.data.map((value, index) => {
    const x = (index / (props.data.length - 1)) * (width - padding * 2) + padding
    const y = height - padding - ((value - min) / range) * (height - padding * 2)
    return { x, y }
  })

  // Create smooth curve using quadratic bezier
  let d = `M ${points[0].x} ${points[0].y}`

  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1]
    const curr = points[i]
    const cpX = (prev.x + curr.x) / 2
    d += ` Q ${prev.x + (cpX - prev.x) * 0.5} ${prev.y} ${cpX} ${(prev.y + curr.y) / 2}`
    d += ` Q ${cpX + (curr.x - cpX) * 0.5} ${curr.y} ${curr.x} ${curr.y}`
  }

  return d
})

const strokeColor = computed(() => {
  switch (props.trend) {
    case 'up':
      return 'var(--color-success)'
    case 'down':
      return 'var(--color-error)'
    default:
      return 'var(--text-muted)'
  }
})

const gradientId = computed(() => `sparkline-gradient-${Math.random().toString(36).substr(2, 9)}`)
</script>

<template>
  <svg :width="width" :height="height" class="sparkline">
    <defs>
      <linearGradient :id="gradientId" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" :stop-color="strokeColor" stop-opacity="0.3" />
        <stop offset="100%" :stop-color="strokeColor" stop-opacity="0" />
      </linearGradient>
    </defs>
    <!-- Area fill -->
    <path
      v-if="pathD"
      :d="pathD + ` L ${width - 2} ${height} L 2 ${height} Z`"
      :fill="`url(#${gradientId})`"
    />
    <!-- Line -->
    <path
      v-if="pathD"
      :d="pathD"
      fill="none"
      :stroke="strokeColor"
      stroke-width="1.5"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>

<style scoped>
.sparkline {
  display: block;
}
</style>
