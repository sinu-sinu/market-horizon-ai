<script setup lang="ts">
import ChatContainer from '@/components/chat/ChatContainer.vue'
</script>

<template>
  <div class="dashboard-view">
    <ChatContainer />
  </div>
</template>

<style scoped>
.dashboard-view {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}
</style>
