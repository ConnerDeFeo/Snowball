export const RECENTS_KEY = 'snowball:recents'
export const CHAT_MODEL_KEY = 'snowball:chat-model'
export const CHAT_EFFORT_KEY = 'snowball:chat-effort'
export function reviewSessionKey(tckr: string, start: number, end: number): string {
  return `snowball:review-session:${tckr}:${start}-${end}`
}
