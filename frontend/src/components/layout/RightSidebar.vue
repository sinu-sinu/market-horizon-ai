<script setup lang="ts">
import { useUIStore } from '@/stores'
import MetricsGrid from '@/components/metrics/MetricsGrid.vue'

const uiStore = useUIStore()
</script>

<template>
  <Transition name="slide-right">
    <aside v-if="uiStore.rightSidebarVisible" class="right-sidebar">
      <div class="sidebar-header">
        <button class="close-btn" @click="uiStore.toggleRightSidebar">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M12 4L4 12M4 4l8 8"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </div>

      <div class="sidebar-content">
        <MetricsGrid />
      </div>

      <div class="sidebar-footer">
        <button class="footer-btn">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M8 14A6 6 0 1 0 8 2a6 6 0 0 0 0 12z"
              stroke="currentColor"
              stroke-width="1.5"
            />
            <path
              d="M8 5v3M8 11h.01"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
            />
          </svg>
          Benchmark
        </button>
        <button class="footer-btn">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <rect x="2" y="3" width="12" height="10" rx="2" stroke="currentColor" stroke-width="1.5" />
            <path d="M2 6h12" stroke="currentColor" stroke-width="1.5" />
          </svg>
          Period
        </button>
      </div>
    </aside>
  </Transition>
</template>

<style scoped>
.right-sidebar {
  width: var(--right-sidebar-width);
  height: 100%;
  background: var(--bg-primary);
  border-left: 1px solid var(--lumina-charcoal);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  justify-content: flex-end;
  padding: var(--space-3);
  border-bottom: 1px solid var(--lumina-charcoal);
}

.close-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.close-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.sidebar-footer {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-3);
  border-top: 1px solid var(--lumina-charcoal);
}

.footer-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.footer-btn:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

/* Slide animation */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform var(--transition-base), opacity var(--transition-base);
}

.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
