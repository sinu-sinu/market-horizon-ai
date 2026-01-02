import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Theme, ToastMessage } from '@/types'

export const useUIStore = defineStore('ui', () => {
  // State
  const leftSidebarExpanded = ref(true)
  const rightSidebarVisible = ref(true)
  const activeModal = ref<string | null>(null)
  const theme = ref<Theme>('dark')
  const toasts = ref<ToastMessage[]>([])

  // Actions
  function toggleLeftSidebar() {
    leftSidebarExpanded.value = !leftSidebarExpanded.value
  }

  function toggleRightSidebar() {
    rightSidebarVisible.value = !rightSidebarVisible.value
  }

  function openModal(modalId: string) {
    activeModal.value = modalId
  }

  function closeModal() {
    activeModal.value = null
  }

  function setTheme(newTheme: Theme) {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  function addToast(toast: Omit<ToastMessage, 'id'>) {
    const id = `toast-${Date.now()}`
    const newToast: ToastMessage = {
      ...toast,
      id,
      duration: toast.duration ?? 5000,
    }
    toasts.value.push(newToast)

    // Auto remove after duration
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }
  }

  function removeToast(id: string) {
    const index = toasts.value.findIndex((t) => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    // State
    leftSidebarExpanded,
    rightSidebarVisible,
    activeModal,
    theme,
    toasts,
    // Actions
    toggleLeftSidebar,
    toggleRightSidebar,
    openModal,
    closeModal,
    setTheme,
    addToast,
    removeToast,
  }
})
