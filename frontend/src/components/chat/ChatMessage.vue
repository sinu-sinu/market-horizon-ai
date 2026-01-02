<script setup lang="ts">
import type { ChatMessage } from '@/types'
import TypingIndicator from './TypingIndicator.vue'
import AnalysisResult from '@/components/analysis/AnalysisResult.vue'

defineProps<{
  message: ChatMessage
}>()
</script>

<template>
  <div class="chat-message" :class="[`role-${message.role}`]">
    <div class="message-avatar">
      <div v-if="message.role === 'user'" class="avatar user-avatar">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path
            d="M15 15.75v-1.5A3 3 0 0 0 12 11.25H6a3 3 0 0 0-3 3v1.5M9 8.25a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
      <div v-else class="avatar assistant-avatar">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path
            d="M4.5 13.5V7.5L9 4.5l4.5 3v6M7.5 13.5V10.5h3v3"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    </div>

    <div class="message-content">
      <template v-if="message.isLoading">
        <TypingIndicator />
      </template>
      <template v-else-if="message.result">
        <p class="message-text">{{ message.content }}</p>
        <AnalysisResult :result="message.result" />
      </template>
      <template v-else>
        <p class="message-text">{{ message.content }}</p>
      </template>
    </div>
  </div>
</template>

<style scoped>
.chat-message {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6);
  animation: fadeInUp 0.3s ease forwards;
}

.chat-message.role-assistant {
  background: rgba(0, 0, 0, 0.02);
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar {
  background: var(--lumina-black);
  color: var(--lumina-white);
}

.assistant-avatar {
  background: var(--lumina-lime);
  color: var(--lumina-black);
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-text {
  color: var(--text-dark);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  margin-bottom: var(--space-3);
}

.role-assistant .message-text {
  margin-bottom: var(--space-4);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
