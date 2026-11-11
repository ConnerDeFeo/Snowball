import { useCallback, useEffect, useRef } from 'react'

const NEAR_BOTTOM_PX = 40

// Keeps a scroll container pinned to the bottom while its content grows, until the
// user scrolls away. Scrolling back to the bottom (or calling pin) resumes following.
export function useStickToBottom() {
  const scrollRef = useRef<HTMLDivElement>(null)
  const contentRef = useRef<HTMLDivElement>(null)
  const pinned = useRef(true)

  const scrollToBottom = useCallback(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [])

  const onScroll = useCallback(() => {
    const el = scrollRef.current
    if (el) pinned.current = el.scrollHeight - el.scrollTop - el.clientHeight < NEAR_BOTTOM_PX
  }, [])

  const pin = useCallback(() => {
    pinned.current = true
    scrollToBottom()
  }, [scrollToBottom])

  useEffect(() => {
    const content = contentRef.current
    if (!content) return
    const observer = new ResizeObserver(() => {
      if (pinned.current) scrollToBottom()
    })
    observer.observe(content)
    return () => observer.disconnect()
  })

  return { scrollRef, contentRef, onScroll, pin }
}
