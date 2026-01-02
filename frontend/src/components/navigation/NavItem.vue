<script setup lang="ts">
import type { NavItem } from '@/types'

defineProps<{
  item: NavItem
  collapsed?: boolean
  active?: boolean
}>()

defineEmits<{
  click: []
}>()
</script>

<template>
  <button
    class="nav-item"
    :class="{ collapsed, active }"
    @click="$emit('click')"
  >
    <span class="nav-icon" v-html="item.icon"></span>
    <Transition name="slide">
      <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
    </Transition>
    <Transition name="fade">
      <span v-if="!collapsed && item.shortcut" class="nav-shortcut">
        {{ item.shortcut }}
      </span>
    </Transition>
    <Transition name="fade">
      <span v-if="item.badge && item.badge > 0" class="nav-badge">
        {{ item.badge > 99 ? '99+' : item.badge }}
      </span>
    </Transition>
  </button>
</template>

<style scoped>
.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  text-align: left;
  transition: all var(--transition-fast);
  position: relative;
}

.nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.collapsed {
  justify-content: center;
  padding: var(--space-3);
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon :deep(svg) {
  width: 20px;
  height: 20px;
}

.nav-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-shortcut {
  font-size: var(--text-xs);
  color: var(--text-muted);
  padding: var(--space-1) var(--space-2);
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
}

.nav-badge {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  min-width: 20px;
  height: 20px;
  padding: 0 var(--space-1);
  background: var(--lumina-lime);
  color: var(--lumina-black);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapsed .nav-badge {
  position: absolute;
  right: 4px;
  top: 4px;
  transform: none;
  min-width: 16px;
  height: 16px;
  font-size: 10px;
}

.slide-enter-active,
.slide-leave-active {
  transition: all var(--transition-fast);
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
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
