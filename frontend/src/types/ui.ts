// UI-related TypeScript interfaces

import type { AnalysisResult } from './analysis'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  result?: AnalysisResult
  isLoading?: boolean
}

export interface FinancialMetric {
  id: string
  label: string
  value: string
  change: number
  changeLabel: string
  trend: 'up' | 'down' | 'neutral'
  sparklineData: number[]
}

export interface QuickAction {
  id: string
  label: string
  icon?: string
  query: string
}

export interface NavItem {
  id: string
  label: string
  icon: string
  path?: string
  badge?: number
  shortcut?: string
}

export interface NavGroup {
  id: string
  label?: string
  items: NavItem[]
}

export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  isTrialUser: boolean
  trialDaysRemaining: number
}

export type Theme = 'dark' | 'light'

export interface ToastMessage {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}
