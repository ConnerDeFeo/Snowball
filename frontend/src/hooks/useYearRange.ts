import { useSearchParams } from 'react-router-dom'
import { defaultRange, isValidRange } from '../constants/yearRange'
import type { YearRange } from '../constants/yearRange'

export function useYearRange() {
  const [searchParams, setSearchParams] = useSearchParams()
  const fallback = defaultRange()

  const paramStart = Number(searchParams.get('start'))
  const paramEnd = Number(searchParams.get('end'))
  const valid = paramStart && paramEnd && isValidRange(paramStart, paramEnd)

  const range: YearRange = valid ? { start: paramStart, end: paramEnd } : fallback

  function setRange(next: YearRange) {
    setSearchParams((prev) => {
      const params = new URLSearchParams(prev)
      params.set('start', String(next.start))
      params.set('end', String(next.end))
      return params
    })
  }

  return { range, setRange }
}
