import type { ChatMessage as ChatMessageType } from '../../../../hooks/useChat'

function ChatMessage({ role, text, isError }: ChatMessageType) {
  const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${
          isUser
            ? 'bg-secondary-ice text-slate-800'
            : isError
              ? 'border border-rose-200 bg-rose-50 text-rose-700'
              : 'border border-secondary-ice bg-white/70 text-slate-800'
        }`}
      >
        {text}
      </div>
    </div>
  )
}

export default ChatMessage
