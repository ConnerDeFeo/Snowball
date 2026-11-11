import ChatTranscript from './ChatTranscript'
import ChatComposer from './ChatComposer'
import type { useChat } from '../../../../hooks/useChat'
import type { YearRange } from '../../../../constants/yearRange'

interface ChatViewProps {
  tckr: string
  range: YearRange
  chat: ReturnType<typeof useChat>
  inputRef: React.RefObject<HTMLTextAreaElement | null>
}

function ChatView({ tckr, range, chat, inputRef }: ChatViewProps) {
  return (
    <div className="flex h-full flex-col">
      <ChatTranscript
        tckr={tckr}
        messages={chat.messages}
        live={chat.live}
        busy={chat.busy}
        onSuggest={chat.send}
      />
      <ChatComposer busy={chat.busy} range={range} onSend={chat.send} inputRef={inputRef} />
    </div>
  )
}

export default ChatView
