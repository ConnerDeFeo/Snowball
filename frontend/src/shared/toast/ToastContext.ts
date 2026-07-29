import { createContext } from 'react'

export interface Toast {
  message: string
  kind: 'error' | 'info'
}

export interface ToastContextValue {
  showToast: (toast: Toast) => void
}

export const ToastContext = createContext<ToastContextValue | null>(null)
