import { USD_DIVISOR } from '../../constants/statements'

function format(n: number, maxDecimals: number): string {
  const text = Math.abs(n).toLocaleString('en-US', { maximumFractionDigits: maxDecimals, minimumFractionDigits: 0 })
  return n < 0 ? `(${text})` : text
}

// Dollar amounts are shown in millions; anything else (per-share amounts,
// share counts, text) is shown as it came from the filing.
export function formatValue(value: number | string | null, unit: string | null): string {
  if (value === null) return ''
  if (typeof value === 'string') return value
  if ((unit ?? '').toLowerCase() === 'usd') return format(value / USD_DIVISOR, 1)
  return format(value, 2)
}
