import { get } from './API'
import type { YearRange } from '../constants/yearRange'
import type { InsiderBody, InsiderFiling } from './types/InsidersTypes'

export function getInsiders(tckr: string, range: YearRange): Promise<InsiderFiling[]> {
  return get<InsiderFiling[]>(`/insiders/${tckr}?start_year=${range.start}&end_year=${range.end}`)
}

export function getInsiderDoc(tckr: string, id: string): Promise<InsiderBody> {
  return get<InsiderBody>(`/insiders/${tckr}/${encodeURIComponent(id)}`)
}
