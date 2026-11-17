import { useState } from 'react'
import { CHAT_EFFORTS, CHAT_MODELS, DEFAULT_CHAT_EFFORT, DEFAULT_CHAT_MODEL } from '../constants/chatModels'
import type { ChatEffort, ChatModel } from '../constants/chatModels'
import { CHAT_EFFORT_KEY, CHAT_MODEL_KEY } from '../constants/storageKeys'

function load<T extends string>(key: string, options: readonly { value: T }[], fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    return options.find((o) => o.value === raw)?.value ?? fallback
  } catch {
    return fallback
  }
}

function save(key: string, value: string) {
  try {
    localStorage.setItem(key, value)
  } catch {
    // storage unavailable; the pick just won't persist
  }
}

// The chat model and thinking-effort picks, remembered in localStorage across reloads.
export function useChatModel() {
  const [model, setModelState] = useState<ChatModel>(() => load(CHAT_MODEL_KEY, CHAT_MODELS, DEFAULT_CHAT_MODEL))
  const [effort, setEffortState] = useState<ChatEffort>(() => load(CHAT_EFFORT_KEY, CHAT_EFFORTS, DEFAULT_CHAT_EFFORT))

  function setModel(next: ChatModel) {
    setModelState(next)
    save(CHAT_MODEL_KEY, next)
  }

  function setEffort(next: ChatEffort) {
    setEffortState(next)
    save(CHAT_EFFORT_KEY, next)
  }

  return { model, setModel, effort, setEffort }
}
