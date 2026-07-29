import { stream } from './API'
import type { RubricCategory } from '../enums/RubricCategory'
import type { YearRange } from '../constants/yearRange'
import type { DocumentsFrame, GradeSectionFrame, GradeAllFrame } from './types/GradingTypes'

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

export function streamGradeSection(
  tckr: string,
  range: YearRange,
  category: RubricCategory,
  onFrame: (frame: GradeSectionFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  return stream(`/grade_section/${tckr}?${rangeQuery(range)}&rubric_category=${category}`, {
    method: 'GET',
    signal,
    onFrame: (frame) => onFrame(frame as GradeSectionFrame),
  })
}

export function streamGradeAll(
  tckr: string,
  range: YearRange,
  onFrame: (frame: GradeAllFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  return stream(`/grade_all/${tckr}?${rangeQuery(range)}`, {
    method: 'GET',
    signal,
    onFrame: (frame) => onFrame(frame as GradeAllFrame),
  })
}
