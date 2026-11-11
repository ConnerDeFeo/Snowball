import { useEffect } from 'react'
import ChatMessage from './ChatMessage'
import { useStickToBottom } from '../../../../hooks/useStickToBottom'
import { CHAT_SUGGESTIONS } from '../../../../constants/chatSuggestions'
import type { ChatMessage as ChatMessageType, ChatPart } from '../../../../hooks/useChat'

interface ChatTranscriptProps {
  tckr: string
  messages: ChatMessageType[]
  live: ChatPart[]
  busy: boolean
  onSuggest: (text: string) => void
}

function ChatTranscript({ tckr, messages, live, busy, onSuggest }: ChatTranscriptProps) {
  const { scrollRef, contentRef, onScroll, pin } = useStickToBottom()

  // Sending a message resumes following the bottom.
  const lastRole = messages[messages.length - 1]?.role
  useEffect(() => {
    if (lastRole === 'user') pin()
  }, [messages.length, lastRole, pin])

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

  // Waiting: nothing has streamed yet, or the last thing was a tool call still running.
  const waiting = busy && (live.length === 0 || live[live.length - 1].kind === 'tool')

  return (
    <div ref={scrollRef} onScroll={onScroll} className="flex-1 overflow-y-auto">
      <div ref={contentRef} className="mx-auto flex w-full max-w-3xl flex-col gap-5 p-4">
        {messages.map((m, i) => (
          <ChatMessage key={i} {...m} />
        ))}
        {busy && live.length > 0 && <ChatMessage role="assistant" text="" parts={live} streaming />}
        {waiting && <p className="animate-pulse text-sm text-slate-400">Thinking…</p>}
      </div>
    </div>
  )
}

export default ChatTranscript
