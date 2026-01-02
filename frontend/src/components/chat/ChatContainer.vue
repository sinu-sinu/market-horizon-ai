<script setup lang="ts">
import { computed, ref, watch, nextTick } from 'vue'
import { useAnalysisStore } from '@/stores'
import ChatGreeting from './ChatGreeting.vue'
import ChatInput from './ChatInput.vue'
import QuickActions from './QuickActions.vue'
import ChatMessage from './ChatMessage.vue'

const analysisStore = useAnalysisStore()
const messagesContainer = ref<HTMLElement | null>(null)

const hasMessages = computed(() => analysisStore.messages.length > 0)

// Auto-scroll to bottom when new messages arrive
watch(
  () => analysisStore.messages.length,
  async () => {
    await nextTick()
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }
)
</script>

<template>
  <div class="chat-container">
    <div ref="messagesContainer" class="messages-area">
      <div class="messages-inner">
        <template v-if="!hasMessages">
          <ChatGreeting />
          <QuickActions />
        </template>
        <template v-else>
          <ChatMessage
            v-for="message in analysisStore.messages"
            :key="message.id"
            :message="message"
          />
        </template>
      </div>
    </div>

    <div class="input-wrapper">
      <ChatInput />
    </div>

    <div class="chat-footer">
      <span class="footer-text">2025 panorama</span>
      <span class="footer-separator">·</span>
      <a href="#" class="footer-link">Privacy Policy</a>
      <span class="footer-separator">·</span>
      <a href="#" class="footer-link">Support</a>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  min-width: 0;
}

/* Full-width scrollable area */
.messages-area {
  flex: 1;
  overflow-y: auto;
  width: 100%;
  min-width: 0;
}

/* Constrained inner content for readability */
.messages-inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  width: 100%;
}

/* Constrained input wrapper */
.input-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.input-wrapper :deep(.chat-input-wrapper) {
  max-width: 900px;
  width: 100%;
}

.chat-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3);
  font-size: var(--text-xs);
  color: var(--text-dark-secondary);
}

.footer-separator {
  color: var(--lumina-mist);
}

.footer-link {
  color: var(--text-dark-secondary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--text-dark);
}
</style>
