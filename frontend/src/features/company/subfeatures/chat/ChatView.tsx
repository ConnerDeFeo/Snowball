import ChatTranscript from './ChatTranscript'
import ChatComposer from './ChatComposer'
import type { useChat } from '../../../../hooks/useChat'
import type { useChatDraft } from '../../../../hooks/useChatDraft'
import type { YearRange } from '../../../../constants/yearRange'
import type { ChatEffort, ChatModel } from '../../../../constants/chatModels'

interface ChatViewProps {
  tckr: string
  range: YearRange
  chat: ReturnType<typeof useChat>
  draft: ReturnType<typeof useChatDraft>
  inputRef: React.RefObject<HTMLTextAreaElement | null>
  model: ChatModel
  onModelChange: (model: ChatModel) => void
  effort: ChatEffort
  onEffortChange: (effort: ChatEffort) => void
}

function ChatView({ tckr, range, chat, draft, inputRef, model, onModelChange, effort, onEffortChange }: ChatViewProps) {
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
        draft={draft}
        range={range}
        onSend={chat.send}
        onStop={chat.stop}
        inputRef={inputRef}
        model={model}
        onModelChange={onModelChange}
        effort={effort}
        onEffortChange={onEffortChange}
        onNewChat={chat.messages.length > 0 ? chat.reset : undefined}
      />
    </div>
  )
}

export default ChatView
