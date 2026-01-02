<script setup lang="ts">
defineProps<{
  competitors: string[]
}>()
</script>

<template>
  <div class="competitors-section">
    <h4 class="section-title">Competitors Identified</h4>
    <div class="competitors-list">
      <span
        v-for="competitor in competitors"
        :key="competitor"
        class="competitor-tag"
      >
        {{ competitor }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.competitors-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.competitors-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.competitor-tag {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--text-dark);
  transition: all var(--transition-fast);
}

.competitor-tag:hover {
  border-color: var(--lumina-gray);
  background: rgba(0, 0, 0, 0.02);
}
</style>
