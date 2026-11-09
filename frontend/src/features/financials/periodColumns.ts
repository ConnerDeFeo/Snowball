import { PERIOD_COLUMN } from '../../constants/statements'
import type { Statement } from '../../services/types/FinancialsTypes'

// Keeps only the period (date) columns, along with each row's matching values.
export function periodColumns(statement: Statement): Statement {
  const keep = statement.columns.flatMap((c, i) => (PERIOD_COLUMN.test(c) ? [i] : []))
  return {
    columns: keep.map((i) => statement.columns[i]),
    rows: statement.rows.map((row) => ({ ...row, values: keep.map((i) => row.values[i]) })),
  }
}
