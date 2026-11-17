import { useState } from 'react'
import type { Mention } from '../services/types/ReviewTypes'

// Unsent chat input, held above the chat view so it survives switching tabs.
export function useChatDraft() {
  const [text, setText] = useState('')
  const [mentions, setMentions] = useState<Mention[]>([])
  return { text, setText, mentions, setMentions }
}
