import { useCallback, useEffect, useState } from 'react'
import * as ReviewService from '../services/ReviewService'
import { ApiError } from '../services/API'
import { reviewSessionKey } from '../constants/storageKeys'
import type { YearRange } from '../constants/yearRange'

export interface ChatMessage {
  role: 'user' | 'assistant'
  text: string
  isError?: boolean
}

export interface ToolCall {
  tool: string
  args: Record<string, unknown>
}

interface UseChatOptions {
  tckr: string
  range: YearRange
}

export function useChat({ tckr, range }: UseChatOptions) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [pendingTools, setPendingTools] = useState<ToolCall[]>([])
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- resets the transcript when ticker/range changes
    setMessages([])
    setPendingTools([])
  }, [tckr, range.start, range.end])

  const send = useCallback(
    async (text: string) => {
      setMessages((prev) => [...prev, { role: 'user', text }])
      setPendingTools([])
      setBusy(true)

      const key = reviewSessionKey(tckr, range.start, range.end)
      const sessionId = sessionStorage.getItem(key) ?? undefined

      try {
        await ReviewService.streamReview(tckr, {
          start_year: range.start,
          end_year: range.end,
          user_text: text,
          ...(sessionId && { session_id: sessionId }),
        }, (frame) => {
          if (frame.type === 'progress') {
            setPendingTools((prev) => [...prev, { tool: frame.tool, args: frame.args }])
          } else if (frame.type === 'result') {
            if (frame.session_id) sessionStorage.setItem(key, frame.session_id)
            setMessages((prev) => [...prev, { role: 'assistant', text: frame.answer }])
            setPendingTools([])
          } else if (frame.type === 'error') {
            setMessages((prev) => [...prev, { role: 'assistant', text: frame.detail, isError: true }])
            setPendingTools([])
          }
        })
      } catch (err) {
        const detail = err instanceof ApiError ? err.detail : 'Failed to reach the review agent'
        setMessages((prev) => [...prev, { role: 'assistant', text: detail, isError: true }])
      } finally {
        setBusy(false)
      }
    },
    [tckr, range.start, range.end],
  )

  return { messages, pendingTools, busy, send }
}
