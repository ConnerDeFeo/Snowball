import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import ToolCallChip from './ToolCallChip'
import type { ChatMessage as ChatMessageType, ToolCall } from '../../../../hooks/useChat'

interface ChatTranscriptProps {
  messages: ChatMessageType[]
  pendingTools: ToolCall[]
  busy: boolean
}

function ChatTranscript({ messages, pendingTools, busy }: ChatTranscriptProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, pendingTools])

  if (messages.length === 0) {
    return (
      <div className="flex-1 overflow-y-auto p-4 text-sm text-slate-500">
        <p>Ask about a category's grade, e.g.:</p>
        <ul className="mt-2 list-disc pl-5">
          <li>"Why is revenue durability graded low?"</li>
          <li>"What evidence supports the gross margin score?"</li>
        </ul>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <div className="flex flex-col gap-3">
        {messages.map((m, i) => (
          <ChatMessage key={i} {...m} />
        ))}
        {busy && pendingTools.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {pendingTools.map((t, i) => (
              <ToolCallChip key={i} {...t} />
            ))}
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

export default ChatTranscript
