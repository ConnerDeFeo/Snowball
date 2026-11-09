import type { StatementKey } from '../services/types/FinancialsTypes'

export const STATEMENTS: { value: StatementKey; label: string }[] = [
  { value: 'income', label: 'Income statement' },
  { value: 'balance', label: 'Balance sheet' },
  { value: 'cashflow', label: 'Cash flow' },
]

// USD values are shown in millions, like most 10-Ks.
export const USD_DIVISOR = 1_000_000
