<script setup lang="ts">
// Static data sources section for credibility
const dataSources = [
  { name: 'LinkedIn', icon: 'linkedin' },
  { name: 'G2', icon: 'g2' },
  { name: 'Capterra', icon: 'capterra' },
  { name: 'Reddit', icon: 'reddit' },
]
</script>

<template>
  <div class="data-sources-section">
    <h4 class="section-title">Data Sources</h4>
    <div class="sources-grid">
      <div
        v-for="source in dataSources"
        :key="source.name"
        class="source-item"
      >
        <span class="source-name">{{ source.name }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.data-sources-section {
  margin-bottom: var(--space-4);
}

.section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-dark);
  margin-bottom: var(--space-3);
}

.sources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: var(--space-2);
  background: var(--bg-chat-elevated);
  border: 1px solid var(--lumina-mist);
  border-radius: var(--radius-xl);
  padding: var(--space-3);
}

.source-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2);
  background: var(--bg-primary);
  border-radius: var(--radius-md);
}

.source-name {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-dark-secondary);
}
</style>
