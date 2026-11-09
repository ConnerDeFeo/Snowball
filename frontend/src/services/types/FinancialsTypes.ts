export interface StatementRow {
  label: string
  level: number
  abstract: boolean
  unit: string | null
  values: (number | string | null)[]
}

export interface Statement {
  columns: string[]
  rows: StatementRow[]
}

export type StatementKey = 'income' | 'balance' | 'cashflow'

// One filing's statements. quarter is null for a 10-K. A statement the filing
// doesn't have is missing.
export interface FilingStatements {
  form: string
  year: string
  quarter: string | null
  statements: Partial<Record<StatementKey, Statement>>
}
