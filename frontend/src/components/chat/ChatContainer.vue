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
  
  // Auto-scroll to bottom with smooth motion
  watch(
    () => analysisStore.messages.length,
    async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTo({
          top: messagesContainer.value.scrollHeight,
          behavior: 'smooth'
        })
      }
    }
  )
  </script>
  
  <template>
    <div class="chat-viewport">
      <div ref="messagesContainer" class="messages-area">
        <div class="messages-inner">
          <template v-if="!hasMessages">
            <div class="greeting-layout">
              <ChatGreeting />
              <QuickActions />
            </div>
          </template>
          
          <template v-else>
            <div class="message-feed">
              <ChatMessage
                v-for="message in analysisStore.messages"
                :key="message.id"
                :message="message"
              />
              <div class="bottom-padding"></div>
            </div>
          </template>
        </div>
      </div>
  
      <div class="input-section">
        <div class="input-content-wrapper">
          <div class="input-shadow-box">
            <ChatInput />
          </div>
  
          <footer class="chat-footer">
            <div class="footer-meta">
              <span>© 2026 Panorama</span>
              <span class="sep">·</span>
              <a href="#">Privacy</a>
              <span class="sep">·</span>
              <a href="#">Support</a>
            </div>
            <p class="disclaimer">Lumina may provide inaccurate info. Verify results.</p>
          </footer>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* LIGHT THEME VARIABLES (Local override) */
  .chat-viewport {
    --bg-main: #ffffff;
    --bg-subtle: #f9fafb;
    --border-light: #e5e7eb;
    --text-main: #111827;
    --text-muted: #6b7280;
    --input-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
    
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: var(--bg-main);
    position: relative;
    color: var(--text-main);
  }
  
  /* 1. SCROLL AREA */
  .messages-area {
    flex: 1;
    overflow-y: auto;
    scroll-behavior: smooth;
  }
  
  .messages-inner {
    max-width: 800px; /* Optimized line length for readability */
    margin: 0 auto;
    padding: 40px 20px;
    width: 100%;
  }
  
  .greeting-layout {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 50vh;
  }
  
  .message-feed {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }
  
  .bottom-padding {
    height: 180px; /* Space for the floating input */
  }
  
  /* 2. STICKY INPUT BOX */
  .input-section {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    /* Soft white gradient at top of input area to blend messages */
    background: linear-gradient(to top, var(--bg-main) 70%, rgba(255, 255, 255, 0));
    padding-bottom: 12px;
  }
  
  .input-content-wrapper {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .input-shadow-box {
    background: white;
    border: 1px solid var(--border-light);
    border-radius: 16px;
    box-shadow: var(--input-shadow);
    transition: border-color 0.2s;
  }
  
  .input-shadow-box:focus-within {
    border-color: #d1d5db;
  }
  
  /* 3. FOOTER */
  .chat-footer {
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  
  .footer-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    color: var(--text-muted);
  }
  
  .footer-meta a {
    color: inherit;
    text-decoration: none;
  }
  
  .footer-meta a:hover {
    text-decoration: underline;
  }
  
  .sep {
    opacity: 0.5;
  }
  
  .disclaimer {
    font-size: 10px;
    color: #9ca3af;
  }
  
  /* CUSTOM SCROLLBAR (Clean & Minimal) */
  .messages-area::-webkit-scrollbar {
    width: 8px;
  }
  
  .messages-area::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .messages-area::-webkit-scrollbar-thumb {
    background: #e5e7eb;
    border-radius: 10px;
    border: 2px solid var(--bg-main);
  }
  
  .messages-area::-webkit-scrollbar-thumb:hover {
    background: #d1d5db;
  }
  </style>