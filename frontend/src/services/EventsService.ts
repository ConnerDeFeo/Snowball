import { get } from './API'
import type { YearRange } from '../constants/yearRange'
import type { EventBody, EventMeta } from './types/EventsTypes'

export function getEvents(tckr: string, range: YearRange): Promise<EventMeta[]> {
  return get<EventMeta[]>(`/events/${tckr}?start_year=${range.start}&end_year=${range.end}`)
}

export function getEvent(tckr: string, id: string): Promise<EventBody> {
  return get<EventBody>(`/events/${tckr}/${encodeURIComponent(id)}`)
}
