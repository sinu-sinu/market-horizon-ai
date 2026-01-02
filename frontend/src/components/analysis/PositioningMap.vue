<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { ScatterChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components'
import type { PositioningMap } from '@/types'

use([CanvasRenderer, ScatterChart, GridComponent, TooltipComponent, LegendComponent])

const props = defineProps<{
  positioningMap: PositioningMap
}>()

const chartRef = ref()

const chartOptions = computed(() => {
  const companies = props.positioningMap?.companies || {}
  const opportunityZones = props.positioningMap?.opportunity_zones || []
  const dimensions = props.positioningMap?.dimensions || {
    x_axis: 'Price Positioning',
    y_axis: 'Target Company Size',
  }

  // Company data points - all visible with labels
  const companiesArray = Object.entries(companies)

  const companyData = companiesArray.map(([name, pos]) => {
    return {
      name,
      value: [pos.x, pos.y],
      symbolSize: 18,
      itemStyle: {
        color: '#c8ff00',
        borderColor: '#0a0a0a',
        borderWidth: 2,
      },
    }
  })

  // Opportunity zone data
  const zoneData = opportunityZones.map((zone) => ({
    name: zone.description || 'Opportunity',
    value: [zone.coordinates.x, zone.coordinates.y],
    symbolSize: 40,
    itemStyle: {
      color: 'rgba(200, 255, 0, 0.2)',
      borderColor: '#c8ff00',
      borderWidth: 2,
    },
  }))

  // Quadrant labels
  const quadrantLabels = [
    { name: 'Budget\nEnterprise', x: 2.5, y: 9 },
    { name: 'Premium\nEnterprise', x: 8.5, y: 9 },
    { name: 'Budget\nSMB', x: 2.5, y: 2 },
    { name: 'Premium\nSMB', x: 8.5, y: 2 },
  ]

  return {
    backgroundColor: 'transparent',
    grid: {
      left: 70,
      right: 100,
      top: 40,
      bottom: 60,
    },
    xAxis: {
      type: 'value',
      name: dimensions.x_axis,
      nameLocation: 'middle',
      nameGap: 35,
      nameTextStyle: {
        color: '#6b6b6b',
        fontSize: 12,
        fontWeight: 600,
      },
      min: 0,
      max: 11,
      axisLine: { lineStyle: { color: '#d4d4d4' } },
      axisTick: { show: false },
      axisLabel: { color: '#6b6b6b' },
      splitLine: {
        show: true,
        lineStyle: { color: '#f0f0f0' }
      },
    },
    yAxis: {
      type: 'value',
      name: dimensions.y_axis,
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: '#6b6b6b',
        fontSize: 12,
        fontWeight: 600,
      },
      min: 0,
      max: 11,
      axisLine: { lineStyle: { color: '#d4d4d4' } },
      axisTick: { show: false },
      axisLabel: { color: '#6b6b6b' },
      splitLine: {
        show: true,
        lineStyle: { color: '#f0f0f0' }
      },
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: { name: string; value: number[] }) => {
        return `<strong>${params.name}</strong><br/>
          ${dimensions.x_axis}: ${params.value[0].toFixed(1)}<br/>
          ${dimensions.y_axis}: ${params.value[1].toFixed(1)}`
      },
    },
    series: [
      // Quadrant background regions
      {
        name: 'Quadrants',
        type: 'scatter',
        data: [
          { value: [2.75, 8.25], symbolSize: 1, itemStyle: { opacity: 0 } },
          { value: [8.25, 8.25], symbolSize: 1, itemStyle: { opacity: 0 } },
          { value: [2.75, 2.75], symbolSize: 1, itemStyle: { opacity: 0 } },
          { value: [8.25, 2.75], symbolSize: 1, itemStyle: { opacity: 0 } },
        ],
        z: 0,
        silent: true,
        tooltip: { show: false },
      },
      // Quadrant labels
      {
        name: 'Labels',
        type: 'scatter',
        data: quadrantLabels.map(label => ({
          name: label.name,
          value: [label.x, label.y],
          symbolSize: 1,
          itemStyle: { opacity: 0 },
        })),
        label: {
          show: true,
          formatter: '{b}',
          fontSize: 11,
          color: '#9b9b9b',
          fontWeight: 600,
          lineHeight: 16,
        },
        z: 0,
        silent: true,
        tooltip: { show: false },
      },
      {
        name: 'Opportunity Zones',
        type: 'scatter',
        data: zoneData,
        z: 1,
      },
      {
        name: 'Companies',
        type: 'scatter',
        data: companyData,
        z: 2,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          fontSize: 12,
          fontWeight: 500,
          color: '#2a2a2a',
        },
      },
    ],
  }
})

onMounted(() => {
  // Resize observer for responsive chart
  if (chartRef.value) {
    const resizeObserver = new ResizeObserver(() => {
      chartRef.value?.resize()
    })
    resizeObserver.observe(chartRef.value.$el)
  }
})
</script>

<template>
  <div class="positioning-map-section">
    <h4 class="section-title">Competitive Positioning Map</h4>
    <div class="chart-container">
      <VChart
        ref="chartRef"
        :option="chartOptions"
        autoresize
        class="positioning-chart"
      />
    </div>
  </div>
</template>

<style scoped>
.positioning-map-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.chart-container {
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
}

.positioning-chart {
  width: 100%;
  height: 350px;
}
</style>
