import StreamingText from './StreamingText'
import ToolCallChip from './ToolCallChip'
import type { ChatMessage as ChatMessageType, ChatPart } from '../../../../hooks/useChat'

interface ChatMessageProps extends Omit<ChatMessageType, 'role'> {
  role: ChatMessageType['role']
  streaming?: boolean
}

const CARET = <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-secondary align-middle" />

// Groups consecutive tool parts so they render as one wrapped row of chips.
function groupParts(parts: ChatPart[]): ChatPart[][] {
  const groups: ChatPart[][] = []
  for (const part of parts) {
    const last = groups[groups.length - 1]
    if (part.kind === 'tool' && last?.[0].kind === 'tool') last.push(part)
    else groups.push([part])
  }
  return groups
}

function ChatMessage({ role, text, parts, isError, streaming }: ChatMessageProps) {
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

  const groups = groupParts(parts ?? [{ kind: 'text', text }])

  return (
    <div className="flex flex-col gap-3 text-sm text-slate-800">
      {groups.map((group, i) => {
        const isLast = i === groups.length - 1
        if (group[0].kind === 'tool') {
          return (
            <div key={i} className="flex flex-wrap gap-2">
              {group.map((p, j) => p.kind === 'tool' && <ToolCallChip key={j} tool={p.tool} args={p.args} />)}
            </div>
          )
        }
        const part = group[0] as { kind: 'text'; text: string }
        return (
          <div key={i}>
            <StreamingText text={part.text} streaming={!!streaming && isLast} />
            {streaming && isLast && CARET}
          </div>
        )
      })}
    </div>
  )
}

export default ChatMessage
