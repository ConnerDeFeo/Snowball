import type { RubricCategory } from '../../enums/RubricCategory'

export interface GradedTimePeriod {
  category: RubricCategory
  start: number
  end: number
  grade: number
  reasoning: string
  quotes: string[]
}

export interface ErrorFrame {
  type: 'error'
  detail: string
}

export type DocumentsFrame =
  | { type: 'start'; total: number; counts: Record<string, number> }
  | { type: 'progress'; completed: number; total: number; form: string; filing_date: string }
  | { type: 'done'; ticker: string }
  | ErrorFrame

export type GradeSectionFrame =
  | { type: 'start'; total: number }
  | {
      type: 'progress'
      completed: number
      total: number
      form: string
      year: number
      section: string
      quarter: number | null
    }
  | { type: 'result'; graded: GradedTimePeriod }
  | ErrorFrame

export type GradeAllFrame =
  | { type: 'categories'; total: number; cached: number }
  | {
      type: 'progress'
      completed: number
      total: number
      form: string
      year: number
      section: string
      quarter: number | null
      category: string
    }
  | { type: 'result'; graded: GradedTimePeriod[] }
  | ErrorFrame
