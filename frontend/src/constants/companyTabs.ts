export const COMPANY_TABS = [
  { value: 'checklist', label: 'Checklist' },
  { value: 'financials', label: 'Financials' },
] as const

export type CompanyTab = (typeof COMPANY_TABS)[number]['value']
