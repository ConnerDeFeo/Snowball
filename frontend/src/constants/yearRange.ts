export const MAX_YEAR_SPAN = 6
export const MIN_YEAR = 2000

export interface YearRange {
  start: number
  end: number
}

export function defaultRange(): YearRange {
  const currentYear = new Date().getFullYear()
  return { start: currentYear - 5, end: currentYear }
}

export function isValidRange(start: number, end: number): boolean {
  return start <= end && end - start + 1 <= MAX_YEAR_SPAN
}

export function yearOptions(): number[] {
  const currentYear = new Date().getFullYear()
  const years: number[] = []
  for (let year = currentYear; year >= MIN_YEAR; year--) years.push(year)
  return years
}
