<script setup lang="ts">
import LeftSidebar from './LeftSidebar.vue'
import MainContent from './MainContent.vue'
// import RightSidebar from './RightSidebar.vue'
</script>

<template>
  <div class="app-shell">
    <LeftSidebar />
    <MainContent />
    <!-- <RightSidebar /> -->
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-primary);
}
</style>
