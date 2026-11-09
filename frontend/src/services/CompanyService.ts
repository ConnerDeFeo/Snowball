import { get } from './API'

export interface RecentCompany {
  ticker: string
  start_year: number
  end_year: number
}

// Proposed backend route — not implemented yet. Callers should catch
// ApiError(404) and fall back to localStorage.
export function getCompanies(): Promise<RecentCompany[]> {
  return get<RecentCompany[]>('/companies')
}
