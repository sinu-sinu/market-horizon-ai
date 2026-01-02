<script setup lang="ts">
import { ref } from 'vue'
import { useAnalysisStore } from '@/stores'

const analysisStore = useAnalysisStore()
const inputValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

async function handleSubmit() {
  const query = inputValue.value.trim()
  if (!query || analysisStore.isLoading) return

  inputValue.value = ''
  await analysisStore.analyze(query)
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}

function focusInput() {
  inputRef.value?.focus()
}

defineExpose({ focusInput })
</script>

<template>
  <div class="chat-input-wrapper">
    <div class="chat-input-container" :class="{ loading: analysisStore.isLoading }">
      <input
        ref="inputRef"
        v-model="inputValue"
        type="text"
        class="chat-input"
        placeholder="Ask about a competitor, a market niche, or a content gap..."
        :disabled="analysisStore.isLoading"
        @keydown="handleKeydown"
      />

      <div class="input-actions">
        <button
          class="send-btn"
          :disabled="!inputValue.trim() || analysisStore.isLoading"
          @click="handleSubmit"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M14 8H2M14 8L9 3M14 8L9 13"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-input-wrapper {
  padding: var(--space-4) var(--space-6);
  padding-top: 0;
}

.chat-input-container {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-2xl);
  padding: var(--space-2) var(--space-3);
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.chat-input-container:focus-within {
  border-color: var(--lumina-gray);
  box-shadow: var(--shadow-md);
}

.chat-input-container.loading {
  opacity: 0.7;
}

.attach-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  color: var(--text-dark-secondary);
  border-radius: var(--radius-lg);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.attach-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: var(--text-dark);
}

.btn-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.chat-input {
  flex: 1;
  padding: var(--space-2) 0;
  background: transparent;
  border: none;
  color: var(--text-dark);
  font-size: var(--text-base);
  outline: none;
}

.chat-input::placeholder {
  color: var(--lumina-gray);
}

.input-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.shortcut-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: var(--radius-sm);
  color: var(--text-dark-secondary);
}

.send-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--lumina-black);
  color: var(--lumina-white);
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
}

.send-btn:hover:not(:disabled) {
  background: var(--lumina-charcoal);
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
