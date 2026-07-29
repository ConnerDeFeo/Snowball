export const RECENTS_KEY = 'snowball:recents'

export function reviewSessionKey(tckr: string, start: number, end: number): string {
  return `snowball:review-session:${tckr}:${start}-${end}`
}
