import { useState } from 'react'
import TextArea from '../../../../shared/TextArea'
import Button from '../../../../shared/Button'
import Spinner from '../../../../shared/Spinner'
import MentionPicker from './MentionPicker'
import { displayMention } from '../../../../constants/categories'
import type { YearRange } from '../../../../constants/yearRange'
import type { Mention } from '../../../../services/types/ReviewTypes'

interface ChatComposerProps {
  busy: boolean
  range: YearRange
  onSend: (text: string, mentions: Mention[]) => void
}

function ChatComposer({ busy, range, onSend }: ChatComposerProps) {
  const [text, setText] = useState('')
  const [mentions, setMentions] = useState<Mention[]>([])
  const [pickerOpen, setPickerOpen] = useState(false)

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || busy) return
    onSend(trimmed, mentions)
    setText('')
    setMentions([])
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  // Typing "@" opens the section picker instead of inserting the character.
  function handleChange(value: string) {
    if (value.endsWith('@') && !text.endsWith('@')) {
      setText(value.slice(0, -1))
      setPickerOpen(true)
    } else {
      setText(value)
    }
  }

  return (
    <div className="flex flex-col gap-2 border-t border-secondary-ice p-3">
      {pickerOpen && (
        <MentionPicker
          range={range}
          onAdd={(m) => setMentions((prev) => [...prev, m])}
          onClose={() => setPickerOpen(false)}
        />
      )}

      {mentions.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {mentions.map((m, i) => (
            <span
              key={i}
              className="inline-flex items-center gap-1 rounded-full border border-secondary-ice bg-secondary-ice/50 px-2.5 py-1 text-xs text-slate-600"
            >
              {displayMention(m)}
              <button
                onClick={() => setMentions((prev) => prev.filter((_, j) => j !== i))}
                className="cursor-pointer text-slate-400 hover:text-slate-700"
                aria-label="Remove mention"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}

      <div className="flex items-end gap-2">
        <div className="flex-1">
          <TextArea value={text} onChange={handleChange} placeholder="Ask Snowball... (type @ to add a filing section)" rows={2} onKeyDown={handleKeyDown} disabled={busy} />
        </div>
        <Button variant="ghost" onClick={() => setPickerOpen(true)} disabled={busy || pickerOpen}>
          @
        </Button>
        <Button onClick={submit} disabled={busy || !text.trim()}>
          {busy ? <Spinner /> : 'Send'}
        </Button>
      </div>
    </div>
  )
}

export default ChatComposer
