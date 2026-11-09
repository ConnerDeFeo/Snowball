export interface Finding {
  field: string
  value: string
  snippet: string
  status: string
}

// One filing's worth of evidence from one sub-agent. quarter is null for a 10-K.
export interface EvidenceItem {
  form: string
  year: string
  quarter: string | null
  section: string
  findings: Finding[]
}

export interface EvidenceSubAgent {
  id: string
  form: string
  section: string
  evidence: EvidenceItem[]
}

export interface EvidenceQuestion {
  id: string
  text: string
  latest_only: boolean
  sub_agents: EvidenceSubAgent[]
}

export interface EvidenceCategory {
  id: string
  name: string
  questions: EvidenceQuestion[]
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

export type EvidenceRunFrame =
  | { type: 'start'; total: number; cached: number }
  | {
      type: 'progress'
      completed: number
      total: number
      form: string
      year: string
      section: string
      quarter: string | null
      question_id: string
      sub_agent_id: string
    }
  | { type: 'result'; categories: EvidenceCategory[] }
  | ErrorFrame
