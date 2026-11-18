import { useCallback, useRef } from 'react'

// Gives a scroll container a one-shot scrollToBottom. It never follows content growth.
export function useScrollToBottom() {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [])

  return { scrollRef, scrollToBottom }
}
