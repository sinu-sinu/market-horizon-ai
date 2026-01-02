<script setup lang="ts">
import { ref } from 'vue'
import { useUIStore } from '@/stores'
import { cacheService } from '@/services'

const uiStore = useUIStore()
const isClearing = ref(false)
const clearMessage = ref('')

async function clearAllCache() {
  isClearing.value = true
  try {
    const result = await cacheService.clearAll()
    clearMessage.value = result.message
    uiStore.addToast({
      type: 'success',
      message: result.message,
    })
  } catch (e) {
    clearMessage.value = 'Failed to clear cache'
    uiStore.addToast({
      type: 'error',
      message: 'Failed to clear cache',
    })
  } finally {
    isClearing.value = false
  }
}

async function cleanupExpired() {
  isClearing.value = true
  try {
    const result = await cacheService.cleanup()
    clearMessage.value = result.message
    uiStore.addToast({
      type: 'success',
      message: result.message,
    })
  } catch (e) {
    clearMessage.value = 'Failed to cleanup cache'
    uiStore.addToast({
      type: 'error',
      message: 'Failed to cleanup cache',
    })
  } finally {
    isClearing.value = false
  }
}
</script>

<template>
  <div class="settings-view">
    <header class="view-header">
      <h1 class="view-title">Settings</h1>
      <p class="view-subtitle">Configure your Lumina experience</p>
    </header>

    <section class="settings-section">
      <h2 class="section-title">Appearance</h2>
      <div class="setting-item">
        <div class="setting-info">
          <span class="setting-label">Right Sidebar</span>
          <span class="setting-description">Show financial metrics panel</span>
        </div>
        <button
          class="toggle-btn"
          :class="{ active: uiStore.rightSidebarVisible }"
          @click="uiStore.toggleRightSidebar"
        >
          <span class="toggle-track">
            <span class="toggle-thumb"></span>
          </span>
        </button>
      </div>
    </section>

    <section class="settings-section">
      <h2 class="section-title">Cache Management</h2>
      <div class="setting-item">
        <div class="setting-info">
          <span class="setting-label">Clear All Cache</span>
          <span class="setting-description">Remove all cached analysis results</span>
        </div>
        <button
          class="action-btn danger"
          :disabled="isClearing"
          @click="clearAllCache"
        >
          {{ isClearing ? 'Clearing...' : 'Clear Cache' }}
        </button>
      </div>
      <div class="setting-item">
        <div class="setting-info">
          <span class="setting-label">Cleanup Expired</span>
          <span class="setting-description">Remove only expired cache entries</span>
        </div>
        <button
          class="action-btn"
          :disabled="isClearing"
          @click="cleanupExpired"
        >
          {{ isClearing ? 'Cleaning...' : 'Cleanup' }}
        </button>
      </div>
      <p v-if="clearMessage" class="clear-message">{{ clearMessage }}</p>
    </section>

    <section class="settings-section">
      <h2 class="section-title">About</h2>
      <div class="about-info">
        <p><strong>Lumina</strong> - Market Intelligence Platform</p>
        <p>Version 1.0.0</p>
        <p class="about-description">
          Powered by AI agents for competitive analysis, market research, and strategic recommendations.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.settings-view {
  padding: var(--space-8);
  max-width: 600px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--space-8);
}

.view-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-dark);
  margin-bottom: var(--space-2);
}

.view-subtitle {
  font-size: var(--text-base);
  color: var(--text-dark-secondary);
}

.settings-section {
  margin-bottom: var(--space-8);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--lumina-mist);
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.setting-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-dark);
}

.setting-description {
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
}

.toggle-btn {
  padding: 0;
}

.toggle-track {
  display: block;
  width: 44px;
  height: 24px;
  background: var(--lumina-mist);
  border-radius: var(--radius-full);
  position: relative;
  transition: background var(--transition-fast);
}

.toggle-btn.active .toggle-track {
  background: var(--lumina-lime);
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: var(--radius-full);
  transition: transform var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.toggle-btn.active .toggle-thumb {
  transform: translateX(20px);
}

.action-btn {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-lg);
  color: var(--text-dark);
  transition: all var(--transition-fast);
}

.action-btn:hover:not(:disabled) {
  border-color: var(--lumina-gray);
}

.action-btn.danger {
  border-color: var(--color-error);
  color: var(--color-error);
}

.action-btn.danger:hover:not(:disabled) {
  background: var(--color-error-bg);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.clear-message {
  font-size: var(--text-sm);
  color: var(--color-success);
  margin-top: var(--space-3);
}

.about-info {
  font-size: var(--text-sm);
  color: var(--text-dark);
  line-height: var(--leading-relaxed);
}

.about-info p {
  margin-bottom: var(--space-1);
}

.about-description {
  color: var(--text-dark-secondary);
  margin-top: var(--space-2);
}
</style>
