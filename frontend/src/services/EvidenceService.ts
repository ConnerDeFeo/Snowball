import { get, stream } from './API'
import type { YearRange } from '../constants/yearRange'
import type { EvidenceCategory, EvidenceRunFrame } from './types/EvidenceTypes'

// Narrows a read or run to one category and/or one question. Empty = whole checklist.
export interface EvidenceScope {
  categoryId?: string
  questionId?: string
}

function query(range: YearRange, scope: EvidenceScope): string {
  const params = new URLSearchParams({ start_year: String(range.start), end_year: String(range.end) })
  if (scope.categoryId) params.set('category_id', scope.categoryId)
  if (scope.questionId) params.set('question_id', scope.questionId)
  return params.toString()
}

export function getEvidence(tckr: string, range: YearRange, scope: EvidenceScope = {}): Promise<EvidenceCategory[]> {
  return get<EvidenceCategory[]>(`/evidence/${tckr}?${query(range, scope)}`)
}

export function streamEvidenceRun(
  tckr: string,
  range: YearRange,
  scope: EvidenceScope,
  onFrame: (frame: EvidenceRunFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  return stream(`/evidence/run/${tckr}?${query(range, scope)}`, {
    method: 'GET',
    signal,
    onFrame: (frame) => onFrame(frame as EvidenceRunFrame),
  })
}
