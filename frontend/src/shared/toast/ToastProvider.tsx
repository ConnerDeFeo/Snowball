import { useCallback, useRef, useState } from 'react'
import { ToastContext, type Toast } from './ToastContext'

const AUTO_DISMISS_MS = 5000

const KIND_CLASSES: Record<Toast['kind'], string> = {
  error: 'border-rose-200 bg-rose-50 text-rose-700',
  info: 'border-secondary-ice bg-white text-slate-800',
}

function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toast, setToast] = useState<Toast | null>(null)
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const showToast = useCallback((next: Toast) => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
    setToast(next)
    timeoutRef.current = setTimeout(() => setToast(null), AUTO_DISMISS_MS)
  }, [])

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && (
        <div
          className={`fixed bottom-6 right-6 z-50 max-w-sm rounded-xl border px-4 py-3 shadow-lg ${KIND_CLASSES[toast.kind]}`}
        >
          {toast.message}
        </div>
      )}
    </ToastContext.Provider>
  )
}

export default ToastProvider
