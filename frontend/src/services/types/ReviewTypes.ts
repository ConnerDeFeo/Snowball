// A filing section the user @-mentioned. quarter is omitted for a 10-K.
export interface Mention {
  form: string
  year: string
  quarter?: string
  section: string
}

export interface ReviewRequest {
  start_year: number
  end_year: number
  user_text: string
  session_id?: string
  mentions?: Mention[]
}

export type ReviewFrame =
  | { type: 'start' }
  | { type: 'token'; text: string }
  | { type: 'progress'; tool: string; args: Record<string, unknown> }
  | { type: 'result'; answer: string; session_id?: string }
  | { type: 'error'; detail: string }
