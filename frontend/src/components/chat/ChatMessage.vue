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
              stroke-width="1.8"
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
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
      </div>
  
      <div class="message-content">
        <header class="message-header">
          <span class="sender-name">{{ message.role === 'user' ? 'You' : 'Panorama' }}</span>
        </header>
  
        <div class="body-wrapper">
          <template v-if="message.isLoading">
            <TypingIndicator />
          </template>
  
          <template v-else-if="message.result">
            <p class="message-text intro-text">{{ message.content }}</p>
            
            <div class="analysis-container">
              <AnalysisResult :result="message.result" />
            </div>
          </template>
  
          <template v-else>
            <p class="message-text">{{ message.content }}</p>
          </template>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .chat-message {
    display: flex;
    gap: 20px;
    padding: 24px 0; /* More vertical breathing room between messages */
    animation: messageSlideIn 0.4s cubic-bezier(0.075, 0.82, 0.165, 1);
  }
  
  .message-avatar {
    flex-shrink: 0;
  }
  
  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease;
  }
  
  .user-avatar {
    background: #f8f9fa;
    color: #1a1a1a;
    border: 1px solid #eee;
  }
  
  .assistant-avatar {
    background: #000;
    color: #fff;
  }
  
  .message-content {
    flex: 1;
    min-width: 0;
  }
  
  .message-header {
    margin-bottom: 8px;
    display: flex;
    align-items: center;
  }
  
  .sender-name {
    font-size: 13px;
    font-weight: 700;
    color: #111;
    letter-spacing: -0.01em;
  }
  
  .message-text {
    font-size: 15px;
    line-height: 1.65;
    color: #374151;
    white-space: pre-wrap;
  }
  
  /* THE FIX: Spacious Analysis Area */
  .analysis-container {
    margin-top: 24px;
    /* Instead of a tight border, we use a very soft shadow or 
       no border at all to make it feel like part of the flow */
    border-top: 1px solid #f3f4f6; 
    padding-top: 24px;
    width: 100%;
  }
  
  .intro-text {
    color: #6b7280; /* Make the user's prompt text slightly softer when a result exists */
    font-style: italic;
  }
  
  @keyframes messageSlideIn {
    from {
      opacity: 0;
      transform: translateY(16px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>