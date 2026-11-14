import { useState } from 'react'
import { CHAT_MODELS, DEFAULT_CHAT_MODEL } from '../constants/chatModels'
import type { ChatModel } from '../constants/chatModels'
import { CHAT_MODEL_KEY } from '../constants/storageKeys'

function load(): ChatModel {
  try {
    const raw = localStorage.getItem(CHAT_MODEL_KEY)
    return CHAT_MODELS.find((m) => m.value === raw)?.value ?? DEFAULT_CHAT_MODEL
  } catch {
    return DEFAULT_CHAT_MODEL
  }
}

// The chat model pick, remembered in localStorage across reloads.
export function useChatModel() {
  const [model, setModelState] = useState<ChatModel>(load)

  function setModel(next: ChatModel) {
    setModelState(next)
    try {
      localStorage.setItem(CHAT_MODEL_KEY, next)
    } catch {
      // storage unavailable; the pick just won't persist
    }
  }

  return { model, setModel }
}
