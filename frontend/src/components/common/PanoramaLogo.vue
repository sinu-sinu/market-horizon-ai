<script setup lang="ts">
defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <div class="logo" :class="{ collapsed }">
    <img src="/panorama.svg" alt="Panorama Logo" class="logo-icon" />
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
