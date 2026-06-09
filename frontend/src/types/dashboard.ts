export interface SummaryCard {
  title: string
  value: string
  detail: string
  tone: 'info' | 'success' | 'warn'
}

export interface HealthRow {
  id: number
  domain: string
  status: 'Healthy' | 'Pending' | 'Planned'
  mode: string
  note: string
}

export interface QuickFilterValues {
  ownerEmail: string
  keyword: string
}
