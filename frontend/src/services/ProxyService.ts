import { get } from './API'
import type { YearRange } from '../constants/yearRange'
import type { ProxyFiling } from './types/ProxyTypes'

export function getProxies(tckr: string, range: YearRange): Promise<ProxyFiling[]> {
  return get<ProxyFiling[]>(`/proxies/${tckr}?start_year=${range.start}&end_year=${range.end}`)
}
