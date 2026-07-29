import { get } from './API'
import type { YearRange } from '../constants/yearRange'
import type { GradedTimePeriod } from './types/GradingTypes'

export interface RecentCompany {
  ticker: string
  start_year: number
  end_year: number
}

// Proposed backend route — not implemented yet. Callers should catch
// ApiError(404) and fall back to session/local state.
export function getGrades(tckr: string, range: YearRange): Promise<GradedTimePeriod[]> {
  return get<GradedTimePeriod[]>(`/grades/${tckr}?start_year=${range.start}&end_year=${range.end}`)
}

// Proposed backend route — not implemented yet. Callers should catch
// ApiError(404) and fall back to localStorage.
export function getCompanies(): Promise<RecentCompany[]> {
  return get<RecentCompany[]>('/companies')
}
