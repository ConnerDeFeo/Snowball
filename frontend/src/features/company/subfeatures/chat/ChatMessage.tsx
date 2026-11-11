import Markdown from '../../../../shared/Markdown'
import type { ChatMessage as ChatMessageType } from '../../../../hooks/useChat'

interface ChatMessageProps extends ChatMessageType {
  streaming?: boolean
}

function ChatMessage({ role, text, isError, streaming }: ChatMessageProps) {
  if (role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl bg-secondary-ice px-3.5 py-2 text-sm text-slate-800">{text}</div>
      </div>
    )
  }

  if (isError) {
    return <p className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">{text}</p>
  }

  return (
    <div className="text-sm text-slate-800">
      <Markdown>{text}</Markdown>
      {streaming && <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-secondary align-middle" />}
    </div>
  )
}

export default ChatMessage
