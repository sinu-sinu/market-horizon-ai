<script setup lang="ts">
  // Data Sources with status to add credibility
  const dataSources = [
    { name: 'LinkedIn', icon: 'linkedin', color: '#0077b5', status: 'Live' },
    { name: 'G2', icon: 'g2', color: '#ff492c', status: 'Verified' },
    { name: 'Capterra', icon: 'capterra', color: '#003666', status: 'Verified' },
    { name: 'Reddit', icon: 'reddit', color: '#ff4500', status: 'Live' },
  ]
  </script>
  
  <template>
    <div class="data-sources-section">
      <div class="section-header">
        <h4 class="section-title">Data Sources</h4>
        
      </div>
  
      <div class="sources-container">
        <div
          v-for="source in dataSources"
          :key="source.name"
          class="source-card"
        >
          <div class="source-icon-box" :style="{ '--brand-color': source.color }">
            <div class="icon-placeholder"></div>
          </div>
          
          <div class="source-info">
            <span class="source-name">{{ source.name }}</span>
            <span class="source-status">{{ source.status }}</span>
          </div>
  
          <div class="verify-check">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M13.3334 4L6.00008 11.3333L2.66675 8" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .data-sources-section {
    margin: 24px 0;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  
  .section-title {
    font-size: 13px;
    font-weight: 700;
    color: #111827;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .pulse-indicator {
    font-size: 11px;
    color: #6b7280;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
    animation: pulse 2s infinite;
  }
  
  .sources-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
  }
  
  .source-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: 12px;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  
  .source-card:hover {
    border-color: #e5e7eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  }
  
  .source-icon-box {
    width: 32px;
    height: 32px;
    background: #f9fafb;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #f3f4f6;
  }
  
  .icon-placeholder {
    width: 16px;
    height: 16px;
    background: var(--brand-color);
    border-radius: 3px;
    opacity: 0.8;
  }
  
  .source-info {
    display: flex;
    flex-direction: column;
  }
  
  .source-name {
    font-size: 13px;
    font-weight: 600;
    color: #111827;
  }
  
  .source-status {
    font-size: 10px;
    color: #9ca3af;
    font-weight: 500;
  }
  
  .verify-check {
    margin-left: auto;
    opacity: 0.6;
  }
  
  @keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
  }
  </style>