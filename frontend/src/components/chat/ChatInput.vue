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
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path
                d="M14 10H6M14 10L10 6M14 10L10 14"
                stroke="white"
                stroke-width="2"
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
    /* Removed extra padding to allow parent centering */
    width: 100%;
    display: flex;
    justify-content: center;
  }
  
  .chat-input-container {
    display: flex;
    align-items: center;
    width: 100%;
    /* Increased gap and refined padding to match screenshot */
    gap: 12px;
    background: #fff;
    border: 1px solid #e5e7eb; /* Light gray border for the pill */
    border-radius: 99px; /* Perfect pill shape */
    padding: 8px 8px 8px 24px; /* More left padding for text */
    transition: all 0.2s ease;
  }
  
  /* Subtle focus effect on the pill itself */
  .chat-input-container:focus-within {
    border-color: #d1d5db;
  }
  
  .chat-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #1a1a1a;
    font-size: 16px;
    outline: none;
    /* Ensures text is vertically centered */
    height: 40px; 
  }
  
  .chat-input::placeholder {
    color: #a0a0a0;
    font-weight: 400;
  }
  
  .input-actions {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }
  
  .send-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    /* Gray background from your screenshot */
    background: #c2c2c2; 
    border-radius: 50%;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
  }
  
  .send-btn:hover:not(:disabled) {
    background: #a3a3a3;
    transform: scale(1.02);
  }
  
  .send-btn:disabled {
    opacity: 0.5;
    background: #e0e0e0;
    cursor: not-allowed;
  }
  
  /* Loading State Animation */
  .loading {
    opacity: 0.6;
    pointer-events: none;
  }
  </style>