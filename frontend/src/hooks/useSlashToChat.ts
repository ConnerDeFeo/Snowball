import { useEffect } from 'react'

// Calls onSlash when "/" is pressed anywhere outside a text field.
export function useSlashToChat(onSlash: () => void) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const el = e.target as HTMLElement
      if (e.key !== '/' || el.closest('input, textarea, select, [contenteditable]')) return
      e.preventDefault()
      onSlash()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onSlash])
}
