import { useState } from 'react'
import TextArea from '../../../../shared/TextArea'
import Button from '../../../../shared/Button'
import Spinner from '../../../../shared/Spinner'

interface ChatComposerProps {
  busy: boolean
  onSend: (text: string) => void
}

function ChatComposer({ busy, onSend }: ChatComposerProps) {
  const [text, setText] = useState('')

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || busy) return
    onSend(trimmed)
    setText('')
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className="flex items-end gap-2 border-t border-secondary-ice p-3">
      <div className="flex-1">
        <TextArea value={text} onChange={setText} placeholder="Ask Snowball..." rows={2} onKeyDown={handleKeyDown} disabled={busy} />
      </div>
      <Button onClick={submit} disabled={busy || !text.trim()}>
        {busy ? <Spinner /> : 'Send'}
      </Button>
    </div>
  )
}

export default ChatComposer
