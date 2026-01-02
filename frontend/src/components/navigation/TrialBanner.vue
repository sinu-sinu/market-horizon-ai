<script setup lang="ts">
import { useUserStore } from '@/stores'

defineProps<{
  collapsed?: boolean
}>()

const userStore = useUserStore()
</script>

<template>
  <div v-if="userStore.user.isTrialUser" class="trial-banner" :class="{ collapsed }">
    <template v-if="!collapsed">
      <div class="trial-header">
        <span class="trial-title">Your trial ends in {{ userStore.user.trialDaysRemaining }} days</span>
      </div>
      <p class="trial-description">
        Enjoy working with reports, extract data, advanced search experience and much more.
      </p>
      <button class="upgrade-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path
            d="M3 8h10M10 5l3 3-3 3"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        View Case Study
      </button>
    </template>
    <template v-else>
      <div class="trial-collapsed">
        <span class="trial-days">{{ userStore.user.trialDaysRemaining }}</span>
      </div>
    </template>
  </div>
</template>

<style scoped>
.trial-banner {
  margin: var(--space-4);
  padding: var(--space-4);
  background: var(--bg-tertiary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--lumina-graphite);
}

.trial-banner.collapsed {
  margin: var(--space-2);
  padding: var(--space-3);
  display: flex;
  justify-content: center;
}

.trial-header {
  margin-bottom: var(--space-2);
}

.trial-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.trial-description {
  font-size: var(--text-xs);
  color: var(--text-muted);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-4);
}

.upgrade-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--lumina-lime);
  color: var(--lumina-black);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-lg);
  transition: all var(--transition-fast);
}

.upgrade-btn:hover {
  background: var(--lumina-lime-soft);
  transform: translateY(-1px);
}

.trial-collapsed {
  display: flex;
  align-items: center;
  justify-content: center;
}

.trial-days {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--lumina-lime);
  color: var(--lumina-black);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  border-radius: var(--radius-full);
}
</style>
