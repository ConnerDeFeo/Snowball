export const CHAT_MODELS = [
  { value: 'claude-haiku-5-5', label: 'Haiku 5.5' },
  { value: 'claude-sonnet-5-5', label: 'Sonnet 5.5' },
  { value: 'claude-opus-5-5', label: 'Opus 5.5' },
] as const

export type ChatModel = (typeof CHAT_MODELS)[number]['value']

export const DEFAULT_CHAT_MODEL: ChatModel = 'claude-haiku-5-5'
