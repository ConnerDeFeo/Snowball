import ChatTranscript from './ChatTranscript'
import ChatComposer from './ChatComposer'
import Button from '../../../../shared/Button'
import type { useChat } from '../../../../hooks/useChat'
import type { YearRange } from '../../../../constants/yearRange'
import type { ChatEffort, ChatModel } from '../../../../constants/chatModels'

interface ChatViewProps {
  tckr: string
  range: YearRange
  chat: ReturnType<typeof useChat>
  inputRef: React.RefObject<HTMLTextAreaElement | null>
  model: ChatModel
  onModelChange: (model: ChatModel) => void
  effort: ChatEffort
  onEffortChange: (effort: ChatEffort) => void
}

function ChatView({ tckr, range, chat, inputRef, model, onModelChange, effort, onEffortChange }: ChatViewProps) {
  return (
    <div className="flex h-full flex-col">
      {chat.messages.length > 0 && (
        <div className="mx-auto flex w-full max-w-3xl justify-end px-3 pt-2">
          <Button variant="subtle" size="xs" onClick={chat.reset} disabled={chat.busy}>
            New chat
          </Button>
        </div>
      )}
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
        effort={effort}
        onEffortChange={onEffortChange}
      />
    </div>
  )
}

export default ChatView
