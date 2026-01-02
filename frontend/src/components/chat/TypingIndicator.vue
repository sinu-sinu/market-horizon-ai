<script setup lang="ts">
</script>

<template>
  <div class="typing-indicator">
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  </div>
</template>

<style scoped>
.typing-indicator {
  display: flex;
  gap: var(--space-1);
  align-items: center;
  padding: var(--space-3) var(--space-4);
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: var(--lumina-lime);
  border-radius: 50%;
  animation: typingDot 1.4s ease-in-out infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingDot {
  0%, 60%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  30% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
