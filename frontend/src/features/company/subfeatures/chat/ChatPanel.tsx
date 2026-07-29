import Button from '../../../../shared/Button'
import ChatTranscript from './ChatTranscript'
import ChatComposer from './ChatComposer'
import { useChat } from '../../../../hooks/useChat'
import type { YearRange } from '../../../../constants/yearRange'

interface ChatPanelProps {
  tckr: string
  range: YearRange
  open: boolean
  onClose: () => void
}

function ChatPanel({ tckr, range, open, onClose }: ChatPanelProps) {
  const { messages, pendingTools, busy, send } = useChat({ tckr, range })

  return (
    <>
      {open && <div className="fixed inset-0 z-40 bg-slate-900/20" onClick={onClose} />}
      <div
        className={`fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col border-l border-secondary-ice bg-white shadow-xl transition-transform duration-300 ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between border-b border-secondary-ice px-4 py-3">
          <div>
            <p className="font-semibold text-slate-800">Ask Snowball</p>
            <p className="text-xs text-slate-500">
              {tckr} · {range.start}–{range.end}
            </p>
          </div>
          <Button variant="ghost" onClick={onClose}>
            Close
          </Button>
        </div>
        <ChatTranscript messages={messages} pendingTools={pendingTools} busy={busy} />
        <ChatComposer busy={busy} onSend={send} />
      </div>
    </>
  )
}

export default ChatPanel
