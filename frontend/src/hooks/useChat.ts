import { useCallback, useEffect, useRef, useState } from 'react'
import * as ReviewService from '../services/ReviewService'
import { ApiError } from '../services/API'
import { reviewSessionKey } from '../constants/storageKeys'
import type { YearRange } from '../constants/yearRange'
import type { Mention } from '../services/types/ReviewTypes'

// One piece of an assistant turn, in the order it happened.
export type ChatPart =
  | { kind: 'text'; text: string }
  | { kind: 'tool'; tool: string; args: Record<string, unknown> }

export interface ChatMessage {
  role: 'user' | 'assistant'
  text: string
  parts?: ChatPart[]
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
  const [live, setLive] = useState<ChatPart[]>([])
  const liveRef = useRef<ChatPart[]>([]) // latest live parts, readable from the stream callback
  const [busy, setBusy] = useState(false)

  const updateLive = useCallback((next: ChatPart[]) => {
    liveRef.current = next
    setLive(next)
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- resets the transcript when ticker/range changes
    setMessages([])
    updateLive([])
  }, [tckr, range.start, range.end, updateLive])

  const send = useCallback(
    async (text: string, mentions: Mention[] = []) => {
      setMessages((prev) => [...prev, { role: 'user', text }])
      updateLive([])
      setBusy(true)

      const key = reviewSessionKey(tckr, range.start, range.end)
      const sessionId = sessionStorage.getItem(key) ?? undefined

      // Commits the in-flight turn as a message and clears it.
      const commit = (answer: string, extra?: ChatMessage) => {
        const parts = liveRef.current
        setMessages((prev) => [
          ...prev,
          ...(parts.length > 0 || answer ? [{ role: 'assistant' as const, text: answer, parts }] : []),
          ...(extra ? [extra] : []),
        ])
        updateLive([])
      }

      try {
        await ReviewService.streamReview(tckr, {
          start_year: range.start,
          end_year: range.end,
          user_text: text,
          ...(sessionId && { session_id: sessionId }),
          ...(mentions.length > 0 && { mentions }),
        }, (frame) => {
          if (frame.type === 'token') {
            const parts = liveRef.current
            const last = parts[parts.length - 1]
            updateLive(
              last?.kind === 'text'
                ? [...parts.slice(0, -1), { kind: 'text', text: last.text + frame.text }]
                : [...parts, { kind: 'text', text: frame.text }],
            )
          } else if (frame.type === 'progress') {
            updateLive([...liveRef.current, { kind: 'tool', tool: frame.tool, args: frame.args }])
          } else if (frame.type === 'result') {
            if (frame.session_id) sessionStorage.setItem(key, frame.session_id)
            if (liveRef.current.length === 0) updateLive([{ kind: 'text', text: frame.answer }])
            commit(frame.answer)
          } else if (frame.type === 'error') {
            commit('', { role: 'assistant', text: frame.detail, isError: true })
          }
        })
      } catch (err) {
        const detail = err instanceof ApiError ? err.detail : 'Failed to reach the review agent'
        commit('', { role: 'assistant', text: detail, isError: true })
      } finally {
        setBusy(false)
      }
    },
    [tckr, range.start, range.end, updateLive],
  )

  return { messages, live, busy, send }
}
