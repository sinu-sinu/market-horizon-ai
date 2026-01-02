<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <div class="logo" :class="{ collapsed }">
    <div class="logo-icon">
      <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="6" fill="var(--lumina-charcoal)" />
        <path
          d="M10 24V8h7c2 0 3.5.5 4.5 1.5s1.5 2.3 1.5 4c0 1.7-.5 3-1.5 4s-2.5 1.5-4.5 1.5h-4v5h-3zm3-8h3.5c1 0 1.8-.3 2.3-.8s.7-1.2.7-2.2c0-1-.2-1.7-.7-2.2s-1.3-.8-2.3-.8H13v6z"
          fill="var(--lumina-lime)"
        />
      </svg>
    </div>
    <Transition name="fade">
      <span v-if="!collapsed" class="logo-text">Panorama</span>
    </Transition>
  </div>
</template>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-4);
  transition: padding var(--transition-base);
}

.logo.collapsed {
  padding: var(--space-4) var(--space-2);
  justify-content: center;
}

.logo-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  letter-spacing: -0.02em;
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
