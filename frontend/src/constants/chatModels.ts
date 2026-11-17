export const CHAT_MODELS = [
  { value: 'claude-haiku-5-5', label: 'Haiku 5.5' },
  { value: 'claude-sonnet-5-5', label: 'Sonnet 5.5' },
  { value: 'claude-opus-5-5', label: 'Opus 5.5' },
] as const

export type ChatModel = (typeof CHAT_MODELS)[number]['value']

export const DEFAULT_CHAT_MODEL: ChatModel = 'claude-haiku-5-5'

export const CHAT_EFFORTS = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
] as const

export type ChatEffort = (typeof CHAT_EFFORTS)[number]['value']

export const DEFAULT_CHAT_EFFORT: ChatEffort = 'low'
