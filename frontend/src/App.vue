<script setup lang="ts">
import { onMounted } from 'vue'
import { useHistoryStore } from '@/stores'
import AppShell from '@/components/layout/AppShell.vue'

const historyStore = useHistoryStore()

onMounted(() => {
  // Fetch recent queries on mount
  historyStore.fetchRecent(5)
})
</script>

<template>
  <AppShell />
</template>

<style scoped>
/* App-level styles if needed */
</style>
