<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <main class="main-content">
    <RouterView :key="route.path" />
  </main>
</template>

<style scoped>
.main-content {
  flex: 1;
  background: var(--bg-chat);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  min-width: 0;
  min-height: 0;
}

/* Ensure RouterView and its children fill the space */
.main-content :deep(> *) {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
</style>
