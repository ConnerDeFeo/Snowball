export const COMPANY_VIEWS = [
  { value: 'chat', label: 'Chat' },
  { value: 'checklist', label: 'Checklist' },
  { value: 'financials', label: 'Financials' },
  { value: 'events', label: 'Events' },
  { value: 'insiders', label: 'Insiders' },
] as const

export type CompanyView = (typeof COMPANY_VIEWS)[number]['value']

export const DEFAULT_VIEW: CompanyView = 'chat'
