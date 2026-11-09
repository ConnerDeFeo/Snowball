import { get } from './API'
import type { YearRange } from '../constants/yearRange'
import type { FilingStatements } from './types/FinancialsTypes'

export function getFinancials(tckr: string, range: YearRange): Promise<FilingStatements[]> {
  return get<FilingStatements[]>(`/financials/${tckr}?start_year=${range.start}&end_year=${range.end}`)
}
