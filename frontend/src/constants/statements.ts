import type { StatementKey } from '../services/types/FinancialsTypes'

export const STATEMENTS: { value: StatementKey; label: string }[] = [
  { value: 'income', label: 'Income statement' },
  { value: 'balance', label: 'Balance sheet' },
  { value: 'cashflow', label: 'Cash flow' },
]

// Period columns are named by end date, e.g. "2024-09-28 (FY)". Every other
// column the backend may have stored (dimension_*, parent_*, ...) is a word.
export const PERIOD_COLUMN = /^\d{4}-\d{2}-\d{2}/

// USD values are shown in millions, like most 10-Ks.
export const USD_DIVISOR = 1_000_000
