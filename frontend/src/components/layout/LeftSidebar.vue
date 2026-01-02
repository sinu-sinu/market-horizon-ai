<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUIStore } from '@/stores'
import type { NavItem } from '@/types'
import LuminaLogo from '@/components/common/LuminaLogo.vue'
import NavItemComponent from '@/components/navigation/NavItem.vue'
// import UserProfile from '@/components/navigation/UserProfile.vue'
// import TrialBanner from '@/components/navigation/TrialBanner.vue'
import RecentQueriesList from '@/components/history/RecentQueriesList.vue'

const uiStore = useUIStore()
const router = useRouter()
const route = useRoute()

const collapsed = computed(() => !uiStore.leftSidebarExpanded)

const mainNavItems: NavItem[] = [
  {
    id: 'new-chat',
    label: 'New Chat',
    icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
    shortcut: '⌘ N',
  },
  {
    id: 'history',
    label: 'History',
    icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2.5a7.5 7.5 0 1 0 0 15 7.5 7.5 0 0 0 0-15ZM10 5v5l3.75 2.25" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    path: '/history',
  },
]

function handleNavClick(item: NavItem) {
  if (item.id === 'new-chat') {
    // Clear current analysis and start new chat
    window.location.reload()
  } else if (item.path) {
    router.push(item.path)
  }
}

function isActive(item: NavItem): boolean {
  if (item.path) {
    return route.path === item.path
  }
  return false
}
</script>

<template>
  <aside class="left-sidebar" :class="{ collapsed }">
    <div class="sidebar-header">
      <LuminaLogo :collapsed="collapsed" />
      <button
        class="collapse-btn"
        @click="uiStore.toggleLeftSidebar"
        :title="collapsed ? 'Expand' : 'Collapse'"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path
            v-if="collapsed"
            d="M6 4l4 4-4 4"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            v-else
            d="M10 4L6 8l4 4"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-group">
        <NavItemComponent
          v-for="item in mainNavItems"
          :key="item.id"
          :item="item"
          :collapsed="collapsed"
          :active="isActive(item)"
          @click="handleNavClick(item)"
        />
      </div>

      <div class="nav-divider"></div>

      <RecentQueriesList :collapsed="collapsed" />
    </nav>

    <div class="sidebar-footer">
      <a
        v-if="!collapsed"
        href="https://github.com/sinu-sinu"
        target="_blank"
        rel="noopener noreferrer"
        class="author-credit"
      >
        Made by Sinu
      </a>
    </div>
  </aside>
</template>

<style scoped>
.left-sidebar {
  width: var(--sidebar-width);
  height: 100%;
  background: var(--bg-primary);
  border-right: 1px solid var(--lumina-charcoal);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-base);
  overflow: hidden;
}

.left-sidebar.collapsed {
  width: var(--sidebar-collapsed);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: var(--space-3);
  border-bottom: 1px solid var(--lumina-charcoal);
}

.collapsed .sidebar-header {
  padding-right: 0;
  justify-content: center;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.collapse-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.collapsed .collapse-btn {
  display: none;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3) var(--space-2);
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.nav-divider {
  height: 1px;
  background: var(--lumina-charcoal);
  margin: var(--space-4) var(--space-2);
}

.sidebar-footer {
  margin-top: auto;
  border-top: 1px solid var(--lumina-charcoal);
  padding: var(--space-4);
}

.author-credit {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-muted);
  text-align: center;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.author-credit:hover {
  color: var(--text-primary);
}
</style>
