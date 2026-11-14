export const RECENTS_KEY = 'snowball:recents'
export const CHAT_MODEL_KEY = 'snowball:chat-model'
export function reviewSessionKey(tckr: string, start: number, end: number): string {
  return `snowball:review-session:${tckr}:${start}-${end}`
}
