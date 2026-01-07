<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUIStore, useAnalysisStore } from '@/stores'
import type { NavItem } from '@/types'
import PanoramaLogo from '@/components/common/PanoramaLogo.vue'
import NavItemComponent from '@/components/navigation/NavItem.vue'
import RecentQueriesList from '@/components/history/RecentQueriesList.vue'

const uiStore = useUIStore()
const router = useRouter()
const route = useRoute()
const analysisStore = useAnalysisStore()

const collapsed = computed(() => !uiStore.leftSidebarExpanded)

const secondaryNavItems: NavItem[] = [
  {
    id: 'history',
    label: 'History',
    icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2.5a7.5 7.5 0 1 0 0 15 7.5 7.5 0 0 0 0-15ZM10 5v5l3.75 2.25" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    path: '/history',
  },
]

function handleNewChat() {
  analysisStore.clearMessages()
  router.push('/')
}

function handleNavClick(item: NavItem) {
  if (item.path) router.push(item.path)
}

function isActive(path?: string): boolean {
  return path ? route.path === path : false
}
</script>

<template>
  <aside class="left-sidebar" :class="{ collapsed }">
    <div class="sidebar-header">
      <div class="logo-container">
        <PanoramaLogo :collapsed="collapsed" />
      </div>
      
      <button
        v-if="!collapsed"
        class="main-toggle-btn"
        @click="uiStore.toggleLeftSidebar"
        title="Collapse"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <button
      v-if="collapsed"
      class="expand-overlay-btn"
      @click="uiStore.toggleLeftSidebar"
      title="Expand"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div class="sidebar-content">
      <div class="cta-container">
        <button class="new-chat-btn" @click="handleNewChat" :class="{ icon_only: collapsed }">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
          <span v-if="!collapsed" class="btn-text">New Chat</span>
        </button>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-group">
          <NavItemComponent
            v-for="item in secondaryNavItems"
            :key="item.id"
            :item="item"
            :collapsed="collapsed"
            :active="isActive(item.path)"
            @click="handleNavClick(item)"
          />
        </div>

        <div class="section-label" v-if="!collapsed">
          <span>Recent Analysis</span>
        </div>

        <RecentQueriesList :collapsed="collapsed" />
      </nav>
    </div>

    <div class="sidebar-footer">
      <a
        href="https://github.com/sinu-sinu"
        target="_blank"
        class="profile-card"
        :class="{ centered: collapsed }"
      >
        <div class="user-avatar">S</div>
        <div v-if="!collapsed" class="user-info">
          <span class="username">Sinu</span>
          <span class="role">AI Engineer - view profile</span>
        </div>
      </a>
    </div>
  </aside>
</template>

<style scoped>
.left-sidebar {
  --sidebar-inner-padding: 12px;
  width: var(--sidebar-width);
  height: 100vh;
  background: #0d0d0f;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.left-sidebar.collapsed {
  width: var(--sidebar-collapsed);
}

/* Header & Logo */
.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--sidebar-inner-padding);
}

.collapsed .sidebar-header {
  justify-content: center;
  padding: 0;
}

.logo-container {
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

/* Toggle Buttons */
.main-toggle-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
}

.main-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

/* The small toggle that appears when collapsed */
.expand-overlay-btn {
  position: absolute;
  top: 60px; /* Positioned below logo */
  right: -12px;
  width: 24px;
  height: 24px;
  background: #1a1a1c;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

/* CTA */
.cta-container {
  padding: 8px var(--sidebar-inner-padding);
  margin-bottom: 16px;
}

.new-chat-btn {
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  background: #1a1a1c;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  color: #fff;
  font-weight: 400;
  transition: all 0.2s ease;
}

.new-chat-btn.icon_only {
  justify-content: center;
  padding: 0;
  height: 42px;
  width: 42px;
  margin: 0 auto;
}

/* Sidebar Navigation */
.sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 0 var(--sidebar-inner-padding);
}

.section-label {
  margin: 24px 12px 10px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  color: #55555a;
  letter-spacing: 0.12em;
}

/* Footer Card */
.sidebar-footer {
  padding: 16px var(--sidebar-inner-padding);
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 12px;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.02);
}

.profile-card.centered {
  justify-content: center;
  padding: 8px 0;
  background: transparent;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  color: #fff;
  font-size: 13px;
  font-weight: 600;
}

.role {
  color: #6b6b72;
  font-size: 10px;
}
</style>