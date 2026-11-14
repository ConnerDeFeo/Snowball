import ChatTranscript from './ChatTranscript'
import ChatComposer from './ChatComposer'
import type { useChat } from '../../../../hooks/useChat'
import type { YearRange } from '../../../../constants/yearRange'
import type { ChatModel } from '../../../../constants/chatModels'

interface ChatViewProps {
  tckr: string
  range: YearRange
  chat: ReturnType<typeof useChat>
  inputRef: React.RefObject<HTMLTextAreaElement | null>
  model: ChatModel
  onModelChange: (model: ChatModel) => void
}

function ChatView({ tckr, range, chat, inputRef, model, onModelChange }: ChatViewProps) {
  return (
    <div className="flex h-full flex-col">
      <ChatTranscript
        tckr={tckr}
        messages={chat.messages}
        live={chat.live}
        busy={chat.busy}
        onSuggest={chat.send}
      />
      <ChatComposer
        busy={chat.busy}
        range={range}
        onSend={chat.send}
        inputRef={inputRef}
        model={model}
        onModelChange={onModelChange}
      />
    </div>
  )
}

export default ChatView
