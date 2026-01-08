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
    ToolboxComponent,
    DataZoomComponent,
    DataZoomInsideComponent,
    DataZoomSliderComponent,
  } from 'echarts/components'
  import type { PositioningMap, CompanyPosition } from '@/types'
  
  use([
    CanvasRenderer,
    ScatterChart,
    GridComponent,
    TooltipComponent,
    LegendComponent,
    ToolboxComponent,
    DataZoomComponent,
    DataZoomInsideComponent,
    DataZoomSliderComponent,
  ])
  
  const props = defineProps<{
    positioningMap: PositioningMap
  }>()
  
  const chartRef = ref()
  const showModal = ref(false)
  const selectedCompany = ref<{ name: string; position: CompanyPosition } | null>(null)
  const selectedQuadrant = ref<string>('all')
  const showOpportunityZones = ref(true)
  const searchQuery = ref('')
  
  // Get quadrant name based on coordinates
  const getQuadrant = (x: number, y: number): string => {
    if (x >= 5 && y >= 5) return 'premium-enterprise'
    if (x < 5 && y >= 5) return 'budget-enterprise'
    if (x >= 5 && y < 5) return 'premium-smb'
    return 'budget-smb'
  }

  // Get human-readable quadrant name
  const getQuadrantName = (x: number, y: number): string => {
    const quadrant = getQuadrant(x, y)
    const names = {
      'premium-enterprise': 'Premium Enterprise',
      'budget-enterprise': 'Budget Enterprise',
      'premium-smb': 'Premium SMB',
      'budget-smb': 'Budget SMB',
    }
    return names[quadrant as keyof typeof names]
  }

  // Filter companies based on search and quadrant
  const filteredCompanies = computed(() => {
    const companies = props.positioningMap?.companies || {}
    let filtered = Object.entries(companies)

    // Filter by search query
    if (searchQuery.value) {
      filtered = filtered.filter(([name]) =>
        name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    }

    // Filter by quadrant
    if (selectedQuadrant.value !== 'all') {
      filtered = filtered.filter(([, pos]) => {
        const quadrant = getQuadrant(pos.x, pos.y)
        return quadrant === selectedQuadrant.value
      })
    }

    return Object.fromEntries(filtered)
  })

  // Download chart as image
  const downloadChart = (format: 'png' | 'svg' = 'png') => {
    if (chartRef.value) {
      const chart = chartRef.value.chart
      const url = chart.getDataURL({
        type: format,
        pixelRatio: 3, // High resolution
        backgroundColor: '#ffffff'
      })
      
      const link = document.createElement('a')
      link.download = `positioning-map-${Date.now()}.${format}`
      link.href = url
      link.click()
    }
  }

  // Handle company click
  const handleChartClick = (params: any) => {
    if (params.seriesName === 'Companies') {
      const companies = props.positioningMap?.companies || {}
      const company = companies[params.name]
      if (company) {
        selectedCompany.value = { name: params.name, position: company }
        showModal.value = true
      }
    }
  }

  // Reset zoom
  const resetZoom = () => {
    if (chartRef.value) {
      chartRef.value.chart.dispatchAction({
        type: 'dataZoom',
        start: 0,
        end: 100
      })
    }
  }

  const chartOptions = computed(() => {
    const companies = filteredCompanies.value
    const opportunityZones = props.positioningMap?.opportunity_zones || []
    const dimensions = props.positioningMap?.dimensions || {
      x_axis: 'Price Positioning',
      y_axis: 'Target Company Size',
    }
  
    const companiesArray = Object.entries(companies)
  
    const companyData = companiesArray.map(([name, pos]) => {
      const quadrant = getQuadrant(pos.x, pos.y)
      const colorMap = {
        'premium-enterprise': 'rgba(139, 92, 246, 0.9)', // Purple
        'budget-enterprise': 'rgba(59, 130, 246, 0.9)',  // Blue
        'premium-smb': 'rgba(236, 72, 153, 0.9)',        // Pink
        'budget-smb': 'rgba(34, 197, 94, 0.9)',          // Green
      }
      
      return {
        name,
        value: [pos.x, pos.y],
        symbolSize: 20,
        itemStyle: {
          color: colorMap[quadrant as keyof typeof colorMap],
          borderColor: '#ffffff',
          borderWidth: 2,
          shadowBlur: 8,
          shadowColor: 'rgba(0, 0, 0, 0.15)',
          shadowOffsetY: 2,
        },
        rationale: pos.rationale,
        quadrant,
      }
    })
  
    const zoneData = showOpportunityZones.value
      ? opportunityZones.map((zone) => ({
          name: zone.description || 'Opportunity',
          value: [zone.coordinates.x, zone.coordinates.y],
          symbolSize: 50,
          itemStyle: {
            color: 'rgba(251, 191, 36, 0.15)',
            borderColor: '#f59e0b',
            borderWidth: 2,
            borderType: 'dashed',
          },
          rationale: zone.rationale,
          score: zone.opportunity_score,
        }))
      : []
  
    const quadrantLabels = [
      { name: 'Budget\nEnterprise', x: 2.5, y: 9 },
      { name: 'Premium\nEnterprise', x: 8.5, y: 9 },
      { name: 'Budget\nSMB', x: 2.5, y: 1.5 },
      { name: 'Premium\nSMB', x: 8.5, y: 1.5 },
    ]
  
    return {
      backgroundColor: 'transparent',
      animation: true,
      animationDuration: 800,
      animationEasing: 'cubicOut' as const,
      grid: {
        left: 80,
        right: 160,
        top: 60,
        bottom: 80,
      },
      // Interactive toolbox for download, zoom, etc.
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: false,
            title: { zoom: 'Area Zoom', back: 'Reset Zoom' },
          },
          saveAsImage: {
            title: 'Download PNG',
            name: `positioning-map-${Date.now()}`,
            pixelRatio: 3,
            backgroundColor: '#ffffff',
          },
          restore: {
            title: 'Reset View',
          },
        },
        iconStyle: {
          borderColor: '#6b6b6b',
        },
        emphasis: {
          iconStyle: {
            borderColor: '#2563eb',
          },
        },
      },
      // Data zoom for interactive zoom and pan
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: 0,
          filterMode: 'none',
          zoomOnMouseWheel: 'ctrl',
          moveOnMouseMove: true,
          moveOnMouseWheel: true,
        },
        {
          type: 'inside',
          yAxisIndex: 0,
          filterMode: 'none',
          zoomOnMouseWheel: 'ctrl',
          moveOnMouseMove: true,
          moveOnMouseWheel: true,
        },
        {
          type: 'slider',
          show: false,
          xAxisIndex: 0,
          filterMode: 'none',
          bottom: 10,
        },
        {
          type: 'slider',
          show: false,
          yAxisIndex: 0,
          filterMode: 'none',
          right: 10,
        },
      ],
      xAxis: {
        type: 'value',
        name: dimensions.x_axis,
        nameLocation: 'middle',
        nameGap: 40,
        nameTextStyle: { 
          color: '#374151', 
          fontSize: 13, 
          fontWeight: 600,
        },
        min: 0,
        max: 10,
        axisLine: { lineStyle: { color: '#d1d5db', width: 2 } },
        axisTick: { show: false },
        axisLabel: { 
          color: '#6b7280',
          fontSize: 11,
        },
        splitLine: { 
          show: true, 
          lineStyle: { color: '#f3f4f6', width: 1 } 
        },
      },
      yAxis: {
        type: 'value',
        name: dimensions.y_axis,
        nameLocation: 'middle',
        nameGap: 55,
        nameTextStyle: { 
          color: '#374151', 
          fontSize: 13, 
          fontWeight: 600,
        },
        min: 0,
        max: 10,
        axisLine: { lineStyle: { color: '#d1d5db', width: 2 } },
        axisTick: { show: false },
        axisLabel: { 
          color: '#6b7280',
          fontSize: 11,
        },
        splitLine: { 
          show: true, 
          lineStyle: { color: '#f3f4f6', width: 1 } 
        },
      },
      // Enhanced tooltip with rich information
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.98)',
        borderColor: '#e5e7eb',
        borderWidth: 1,
        padding: 16,
        textStyle: {
          color: '#111827',
          fontSize: 13,
        },
        extraCssText: 'box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); border-radius: 8px;',
        formatter: (params: any) => {
          if (params.seriesName === 'Companies') {
            const quadrantNames = {
              'premium-enterprise': 'Premium Enterprise',
              'budget-enterprise': 'Budget Enterprise',
              'premium-smb': 'Premium SMB',
              'budget-smb': 'Budget SMB',
            }
            const quadrantName = quadrantNames[params.data.quadrant as keyof typeof quadrantNames]
            
            let tooltip = `<div style="font-weight: 600; font-size: 14px; margin-bottom: 8px; color: #111827;">${params.name}</div>`
            tooltip += `<div style="margin-bottom: 6px; color: #6b7280; font-size: 12px;">${quadrantName}</div>`
            tooltip += `<div style="color: #374151; margin-bottom: 4px;"><strong>${dimensions.x_axis}:</strong> ${params.value[0].toFixed(1)}/10</div>`
            tooltip += `<div style="color: #374151; margin-bottom: 8px;"><strong>${dimensions.y_axis}:</strong> ${params.value[1].toFixed(1)}/10</div>`
            
            if (params.data.rationale) {
              tooltip += `<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 12px; font-style: italic;">${params.data.rationale}</div>`
            }
            
            tooltip += `<div style="margin-top: 10px; color: #2563eb; font-size: 11px;">💡 Click for detailed view</div>`
            return tooltip
          } else if (params.seriesName === 'Opportunity Zones') {
            let tooltip = `<div style="font-weight: 600; font-size: 14px; margin-bottom: 8px; color: #f59e0b;">${params.name}</div>`
            tooltip += `<div style="color: #374151; margin-bottom: 4px;"><strong>Position:</strong> (${params.value[0].toFixed(1)}, ${params.value[1].toFixed(1)})</div>`
            
            if (params.data.score !== undefined) {
              tooltip += `<div style="color: #374151; margin-bottom: 4px;"><strong>Opportunity Score:</strong> ${params.data.score.toFixed(1)}/10</div>`
            }
            
            if (params.data.rationale) {
              tooltip += `<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 12px;">${params.data.rationale}</div>`
            }
            
            return tooltip
          }
          return params.name
        },
      },
      series: [
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
            fontSize: 12,
            color: '#9ca3af',
            fontWeight: 600,
            lineHeight: 18,
          },
          z: 0,
          silent: true,
        },
        {
          name: 'Opportunity Zones',
          type: 'scatter',
          data: zoneData,
          z: 1,
          animationDelay: (idx: number) => idx * 100,
          emphasis: {
            scale: true,
            scaleSize: 10,
            itemStyle: {
              borderWidth: 3,
              shadowBlur: 20,
              shadowColor: 'rgba(245, 158, 11, 0.5)',
            },
          },
        },
        {
          name: 'Companies',
          type: 'scatter',
          data: companyData,
          z: 10,
          animationDelay: (idx: number) => idx * 50 + 200,
          label: {
            show: true,
            position: 'right',
            distance: 15,
            formatter: '{b}',
            fontSize: 12,
            fontWeight: 500,
            color: '#1f2937',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            padding: [4, 8],
            borderRadius: 4,
            shadowBlur: 4,
            shadowColor: 'rgba(0, 0, 0, 0.05)',
            shadowOffsetY: 1,
          },
          labelLayout: {
            hideOverlap: false,
            moveOverlap: 'shiftY',
            draggable: true,
          },
          labelLine: {
            show: true,
            length2: 10,
            lineStyle: {
              color: '#d1d5db',
              width: 1.5,
              type: 'solid',
            },
          },
          emphasis: {
            focus: 'self',
            scale: true,
            scaleSize: 8,
            label: {
              fontWeight: 'bold',
              fontSize: 14,
              color: '#111827',
              backgroundColor: 'rgba(255, 255, 255, 1)',
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.15)',
            },
            itemStyle: {
              borderWidth: 3,
              shadowBlur: 15,
              shadowOffsetY: 5,
            },
          },
        },
      ],
    }
  })

  // Chart event handlers
  onMounted(() => {
    if (chartRef.value) {
      // Setup resize observer
      const resizeObserver = new ResizeObserver(() => {
        chartRef.value?.resize()
      })
      resizeObserver.observe(chartRef.value.$el)

      // Add click event listener
      const chart = chartRef.value.chart
      chart.on('click', handleChartClick)
      
      // Add double-click to reset zoom
      chart.on('dblclick', () => {
        resetZoom()
      })
    }
  })
  
</script>

<template>
  <div class="positioning-map-section">
    <div class="header">
      <h4 class="section-title">Interactive Positioning Map</h4>
      <div class="header-actions">
        <button @click="downloadChart('png')" class="btn-action" title="Download PNG">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          PNG
        </button>
        <button @click="downloadChart('svg')" class="btn-action" title="Download SVG">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          SVG
        </button>
        <button @click="resetZoom" class="btn-action" title="Reset Zoom">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          Reset
        </button>
      </div>
    </div>

    <div class="controls-bar">
      <div class="search-box">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search companies..."
          class="search-input"
        />
      </div>

      <div class="filter-group">
        <label class="filter-label">Quadrant:</label>
        <select v-model="selectedQuadrant" class="filter-select">
          <option value="all">All Quadrants</option>
          <option value="premium-enterprise">Premium Enterprise</option>
          <option value="budget-enterprise">Budget Enterprise</option>
          <option value="premium-smb">Premium SMB</option>
          <option value="budget-smb">Budget SMB</option>
        </select>
      </div>

      <label class="toggle-label">
        <input type="checkbox" v-model="showOpportunityZones" class="toggle-checkbox" />
        <span class="toggle-text">Show Opportunity Zones</span>
      </label>
    </div>

    <div class="chart-container">
      <VChart
        ref="chartRef"
        :option="chartOptions"
        autoresize
        class="positioning-chart"
      />
      <div class="interaction-hint">
        <p>💡 <strong>Tip:</strong> Hover for details • Click for full info • Ctrl+Scroll to zoom • Drag to pan • Double-click to reset</p>
      </div>
    </div>

    <!-- Company Details Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="modal-overlay" @click="showModal = false">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h3 class="modal-title">{{ selectedCompany?.name }}</h3>
              <button @click="showModal = false" class="modal-close">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>
            
            <div v-if="selectedCompany" class="modal-body">
              <div class="detail-grid">
                <div class="detail-item">
                  <label class="detail-label">Quadrant</label>
                  <div class="detail-value quadrant-badge" :class="getQuadrant(selectedCompany.position.x, selectedCompany.position.y)">
                    {{ getQuadrantName(selectedCompany.position.x, selectedCompany.position.y) }}
                  </div>
                </div>

                <div class="detail-item">
                  <label class="detail-label">{{ positioningMap?.dimensions?.x_axis || 'X Position' }}</label>
                  <div class="detail-value">
                    <div class="score-bar">
                      <div class="score-fill" :style="{ width: `${selectedCompany.position.x * 10}%` }"></div>
                    </div>
                    <span class="score-text">{{ selectedCompany.position.x.toFixed(1) }}/10</span>
                  </div>
                </div>

                <div class="detail-item">
                  <label class="detail-label">{{ positioningMap?.dimensions?.y_axis || 'Y Position' }}</label>
                  <div class="detail-value">
                    <div class="score-bar">
                      <div class="score-fill" :style="{ width: `${selectedCompany.position.y * 10}%` }"></div>
                    </div>
                    <span class="score-text">{{ selectedCompany.position.y.toFixed(1) }}/10</span>
                  </div>
                </div>

                <div v-if="selectedCompany.position.rationale" class="detail-item full-width">
                  <label class="detail-label">Positioning Rationale</label>
                  <div class="detail-value rationale-text">
                    {{ selectedCompany.position.rationale }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
  
  <style scoped>
.positioning-map-section {
  margin-bottom: var(--space-6);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  gap: var(--space-3);
  flex-wrap: wrap;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.02em;
}

.header-actions {
  display: flex;
  gap: var(--space-2);
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  background: white;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: #f9fafb;
  border-color: #2563eb;
  color: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
}

.btn-action:active {
  transform: translateY(0);
}

.controls-bar {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: white;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  flex: 1;
  min-width: 200px;
  transition: all 0.2s ease;
}

.search-box:focus-within {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-box svg {
  color: #9ca3af;
  flex-shrink: 0;
}

.search-input {
  border: none;
  outline: none;
  font-size: 14px;
  color: #111827;
  background: transparent;
  width: 100%;
}

.search-input::placeholder {
  color: #9ca3af;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  white-space: nowrap;
}

.filter-select {
  padding: 10px 14px;
  font-size: 14px;
  color: #374151;
  background: white;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 180px;
}

.filter-select:hover {
  border-color: #2563eb;
}

.filter-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.toggle-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #2563eb;
}

.toggle-text {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  white-space: nowrap;
}

.chart-container {
  background: white;
  border: 1.5px solid #e5e7eb;
  border-radius: 16px;
  padding: var(--space-5);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  position: relative;
}

.positioning-chart {
  width: 100%;
  height: 600px;
}

.interaction-hint {
  margin-top: var(--space-4);
  padding: 12px 16px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-radius: 8px;
  border-left: 3px solid #2563eb;
}

.interaction-hint p {
  margin: 0;
  font-size: 13px;
  color: #1e40af;
  line-height: 1.5;
}

.interaction-hint strong {
  font-weight: 600;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-4);
}

.modal-content {
  background: white;
  border-radius: 20px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5);
  border-bottom: 1.5px solid #e5e7eb;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
}

.modal-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
}

.modal-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-body {
  padding: var(--space-5);
  overflow-y: auto;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  font-size: 15px;
  color: #111827;
}

.quadrant-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  width: fit-content;
}

.quadrant-badge.premium-enterprise {
  background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
  color: #6b21a8;
  border: 1.5px solid #c4b5fd;
}

.quadrant-badge.budget-enterprise {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border: 1.5px solid #93c5fd;
}

.quadrant-badge.premium-smb {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
  color: #9f1239;
  border: 1.5px solid #f9a8d4;
}

.quadrant-badge.budget-smb {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #166534;
  border: 1.5px solid #86efac;
}

.score-bar {
  position: relative;
  width: 100%;
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
  border-radius: 4px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.score-text {
  font-size: 14px;
  font-weight: 600;
  color: #2563eb;
  margin-top: 4px;
  display: block;
}

.rationale-text {
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #2563eb;
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  font-style: italic;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(20px);
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .controls-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: auto;
  }

  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    width: 100%;
  }

  .positioning-chart {
    height: 450px;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>