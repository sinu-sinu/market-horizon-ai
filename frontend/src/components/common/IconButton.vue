<script setup lang="ts">
defineProps<{
  variant?: 'ghost' | 'filled' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  active?: boolean
  disabled?: boolean
}>()
</script>

<template>
  <button
    class="icon-button"
    :class="[
      `variant-${variant ?? 'ghost'}`,
      `size-${size ?? 'md'}`,
      { active, disabled },
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<style scoped>
.icon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  cursor: pointer;
}

.icon-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sizes */
.size-sm {
  width: 32px;
  height: 32px;
}

.size-md {
  width: 40px;
  height: 40px;
}

.size-lg {
  width: 48px;
  height: 48px;
}

/* Variants */
.variant-ghost {
  background: transparent;
  color: var(--text-secondary);
}

.variant-ghost:hover:not(:disabled) {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.variant-ghost.active {
  background: var(--bg-tertiary);
  color: var(--lumina-lime);
}

.variant-filled {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.variant-filled:hover:not(:disabled) {
  background: var(--bg-elevated);
}

.variant-filled.active {
  background: var(--lumina-lime);
  color: var(--lumina-black);
}

.variant-outline {
  background: transparent;
  border: 1px solid var(--lumina-graphite);
  color: var(--text-secondary);
}

.variant-outline:hover:not(:disabled) {
  border-color: var(--lumina-gray);
  color: var(--text-primary);
}
</style>
