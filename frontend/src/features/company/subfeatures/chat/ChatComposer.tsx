import { useEffect, useState } from 'react'
import MentionPicker from './MentionPicker'
import { displayMention } from '../../../../constants/categories'
import type { YearRange } from '../../../../constants/yearRange'
import type { Mention } from '../../../../services/types/ReviewTypes'

interface ChatComposerProps {
  busy: boolean
  range: YearRange
  onSend: (text: string, mentions: Mention[]) => void
  inputRef: React.RefObject<HTMLTextAreaElement | null>
}

function ChatComposer({ busy, range, onSend, inputRef }: ChatComposerProps) {
  const [text, setText] = useState('')
  const [mentions, setMentions] = useState<Mention[]>([])
  const [pickerOpen, setPickerOpen] = useState(false)

  // Auto-grow the textarea up to a cap.
  useEffect(() => {
    const el = inputRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`
  }, [text, inputRef])

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
    <div className="relative mx-auto w-full max-w-3xl p-3 pb-5">
      {pickerOpen && (
        <div className="absolute right-3 bottom-full left-3 mb-1">
          <MentionPicker range={range} onAdd={(m) => setMentions((prev) => [...prev, m])} onClose={() => setPickerOpen(false)} />
        </div>
      )}

      <div className="rounded-2xl border border-secondary-ice bg-primary px-3 py-2 focus-within:border-secondary focus-within:ring-2 focus-within:ring-secondary/30">
        {mentions.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-1.5">
            {mentions.map((m, i) => (
              <span key={i} className="inline-flex items-center gap-1 rounded-full bg-secondary-ice px-2.5 py-0.5 text-xs text-slate-600">
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
          <textarea
            ref={inputRef}
            value={text}
            onChange={(e) => handleChange(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder="Ask Snowball…  ( / to focus )"
            className="max-h-40 flex-1 resize-none bg-transparent py-1 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
          />
          <button
            onClick={() => setPickerOpen(true)}
            disabled={pickerOpen}
            title="Attach a filing section"
            className="h-8 w-8 cursor-pointer rounded-full text-secondary-deep hover:bg-secondary-ice disabled:opacity-40"
          >
            @
          </button>
          <button
            onClick={submit}
            disabled={busy || !text.trim()}
            title="Send"
            className="h-8 w-8 cursor-pointer rounded-full bg-secondary text-white hover:bg-secondary-deep disabled:cursor-not-allowed disabled:opacity-40"
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatComposer
