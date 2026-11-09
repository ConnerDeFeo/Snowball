import { stream } from './API'
import type { YearRange } from '../constants/yearRange'
import type { DocumentsFrame } from './types/EvidenceTypes'

function rangeQuery(range: YearRange): string {
  return `start_year=${range.start}&end_year=${range.end}`
}

export function streamDocuments(
  tckr: string,
  range: YearRange,
  onFrame: (frame: DocumentsFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  return stream(`/documents/${tckr}?${rangeQuery(range)}`, {
    method: 'GET',
    signal,
    onFrame: (frame) => onFrame(frame as DocumentsFrame),
  })
}
