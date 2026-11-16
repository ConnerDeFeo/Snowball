// Form filter for the filings list. 'all' shows every form.
export const INSIDER_FORM_OPTIONS = [
  { value: 'all', label: 'All' },
  { value: '4', label: 'Form 4' },
  { value: '13D', label: '13D' },
] as const

export type InsiderFormFilter = (typeof INSIDER_FORM_OPTIONS)[number]['value']

// Filter for the transactions table: every row, or only open-market buys and sells.
export const TRADE_FILTER_OPTIONS = [
  { value: 'all', label: 'All' },
  { value: 'trades', label: 'Buys / Sells' },
] as const

export type TradeFilter = (typeof TRADE_FILTER_OPTIONS)[number]['value']

export const TRADE_CODES = ['P', 'S']

// SEC Form 4 transaction codes.
export const TRANSACTION_CODES: Record<string, string> = {
  P: 'Purchase',
  S: 'Sale',
  A: 'Grant',
  M: 'Exercise',
  F: 'Tax withheld',
  G: 'Gift',
  D: 'Disposed to issuer',
  C: 'Conversion',
  X: 'Option exercise',
  W: 'Will / inheritance',
  J: 'Other',
}

export function codeLabel(code: string): string {
  return TRANSACTION_CODES[code] ? `${code} · ${TRANSACTION_CODES[code]}` : code
}
