export const COMPANY_VIEWS = [
  { value: 'chat', label: 'Chat' },
  { value: 'checklist', label: 'Checklist' },
  { value: 'financials', label: 'Financials' },
  { value: 'proxies', label: 'Proxies' },
  { value: 'events', label: 'Events' },
  { value: 'insiders', label: 'Insiders' },
] as const

// Not a tab in COMPANY_VIEWS: reached from the sidebar's "Edit checklist" button.
export const EDIT_CHECKLIST_VIEW = 'edit-checklist'

export type CompanyView = (typeof COMPANY_VIEWS)[number]['value'] | typeof EDIT_CHECKLIST_VIEW

export const DEFAULT_VIEW: CompanyView = 'chat'
