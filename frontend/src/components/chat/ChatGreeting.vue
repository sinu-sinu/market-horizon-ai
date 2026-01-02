<script setup lang="ts">
import { useUserStore } from '@/stores'

const userStore = useUserStore()
</script>

<template>
  <div class="chat-greeting animate-fade-in-up">
    <h1 class="greeting-title">
      Hi, {{ userStore.displayName }}
      <br />
      <span class="greeting-subtitle">What can I help you with?</span>
    </h1>
  </div>
</template>

<style scoped>
.chat-greeting {
  text-align: center;
  padding: var(--space-8) var(--space-4);
}

.greeting-title {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: var(--font-black);
  color: var(--text-dark);
  line-height: 1.2;
  letter-spacing: -0.03em;
}

.greeting-subtitle {
  font-weight: var(--font-bold);
  background: linear-gradient(135deg, var(--text-dark) 0%, var(--text-dark-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
