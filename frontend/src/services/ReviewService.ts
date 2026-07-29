import { stream } from './API'
import type { ReviewRequest, ReviewFrame } from './types/ReviewTypes'

export function streamReview(
  tckr: string,
  body: ReviewRequest,
  onFrame: (frame: ReviewFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  return stream(`/review/${tckr}`, {
    method: 'POST',
    body,
    signal,
    onFrame: (frame) => onFrame(frame as ReviewFrame),
  })
}
