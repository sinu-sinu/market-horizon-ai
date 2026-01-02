<script setup lang="ts">
import { useUserStore } from '@/stores'

defineProps<{
  collapsed?: boolean
}>()

const userStore = useUserStore()
</script>

<template>
  <div class="user-profile" :class="{ collapsed }">
    <div class="avatar">
      <img v-if="userStore.user.avatar" :src="userStore.user.avatar" :alt="userStore.user.name" />
      <span v-else class="avatar-initials">{{ userStore.initials }}</span>
    </div>
    <Transition name="slide">
      <div v-if="!collapsed" class="user-info">
        <span class="user-name">{{ userStore.user.name }}</span>
        <span class="user-status">
          {{ userStore.user.isTrialUser ? 'Trial' : 'Pro' }}
        </span>
      </div>
    </Transition>
    <Transition name="fade">
      <button v-if="!collapsed" class="expand-btn">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path
            d="M4 6L8 10L12 6"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </Transition>
  </div>
</template>

<style scoped>
.user-profile {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.user-profile:hover {
  background: var(--bg-tertiary);
}

.user-profile.collapsed {
  justify-content: center;
  padding: var(--space-3);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-secondary);
}

.user-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-status {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.expand-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.expand-btn:hover {
  background: var(--bg-elevated);
  color: var(--text-secondary);
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
