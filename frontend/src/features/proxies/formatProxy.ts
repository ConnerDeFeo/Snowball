import type { ColumnKind } from '../../constants/proxies'

const EMPTY = '—'

// Full dollars with thousands separators; negatives go in parentheses.
export function formatUsd(value: number | null | undefined): string {
  if (value == null) return EMPTY
  const text = `$${Math.abs(value).toLocaleString('en-US', { maximumFractionDigits: 0 })}`
  return value < 0 ? `(${text})` : text
}

export function formatCell(value: string | number | boolean | null | undefined, kind: ColumnKind): string {
  if (value == null) return EMPTY
  if (typeof value !== 'number') return String(value)
  return kind === 'usd' ? formatUsd(value) : value.toLocaleString('en-US', { maximumFractionDigits: 2 })
}
