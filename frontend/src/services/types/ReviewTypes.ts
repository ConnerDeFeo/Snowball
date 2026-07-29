export interface ReviewRequest {
  start_year: number
  end_year: number
  user_text: string
  session_id?: string
}

export type ReviewFrame =
  | { type: 'start' }
  | { type: 'progress'; tool: string; args: Record<string, unknown> }
  | { type: 'result'; answer: string; session_id?: string }
  | { type: 'error'; detail: string }
