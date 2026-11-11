import { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import ToolCallChip from './ToolCallChip'
import { CHAT_SUGGESTIONS } from '../../../../constants/chatSuggestions'
import type { ChatMessage as ChatMessageType, ToolCall } from '../../../../hooks/useChat'

interface ChatTranscriptProps {
  tckr: string
  messages: ChatMessageType[]
  pendingTools: ToolCall[]
  draft: string
  busy: boolean
  onSuggest: (text: string) => void
}

function ChatTranscript({ tckr, messages, pendingTools, draft, busy, onSuggest }: ChatTranscriptProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'auto' })
  }, [messages, pendingTools, draft])

  if (messages.length === 0 && !busy) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-6 overflow-y-auto p-6">
        <div className="text-center">
          <span className="text-4xl text-secondary-deep">❄</span>
          <h2 className="mt-2 text-2xl font-semibold text-slate-800">Ask about {tckr}</h2>
        </div>
        <div className="flex w-full max-w-xl flex-col gap-2">
          {CHAT_SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => onSuggest(s)}
              className="cursor-pointer rounded-xl border border-secondary-ice px-4 py-2.5 text-left text-sm text-slate-600 transition-colors hover:bg-secondary-ice"
            >
              {s}
            </button>
          ))}
        </div>
        <p className="text-xs text-slate-400">Type @ to attach a filing section</p>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-5 p-4">
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
        {busy && draft && <ChatMessage role="assistant" text={draft} streaming />}
        {busy && !draft && <p className="animate-pulse text-sm text-slate-400">Thinking…</p>}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

export default ChatTranscript
