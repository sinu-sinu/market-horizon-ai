import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User>({
    id: '1',
    name: '',
    email: 'sinu28.sinu@example.com',
    avatar: undefined,
    isTrialUser: true,
    trialDaysRemaining: 14,
  })

  // Getters
  const displayName = computed(() => {
    return user.value.name.split(' ')[0]
  })

  const initials = computed(() => {
    const parts = user.value.name.split(' ')
    return parts.map((p) => p[0]).join('').toUpperCase().slice(0, 2)
  })

  // Actions
  function setUser(newUser: User) {
    user.value = newUser
  }

  function updateTrialDays(days: number) {
    user.value.trialDaysRemaining = days
  }

  return {
    // State
    user,
    // Getters
    displayName,
    initials,
    // Actions
    setUser,
    updateTrialDays,
  }
})
