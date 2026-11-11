import { useEffect, useRef, useState } from 'react'

// Reveals `target` at an even pace instead of in the bursts it arrives in.
// Each frame shows a fraction of the backlog, so it flows and always catches up.
export function useSmoothText(target: string, animate: boolean): string {
  const [shown, setShown] = useState(0)
  const targetRef = useRef(target)

  useEffect(() => {
    targetRef.current = target
  }, [target])

  useEffect(() => {
    if (!animate) return
    let raf = requestAnimationFrame(function tick() {
      setShown((n) => {
        const backlog = targetRef.current.length - n
        return backlog > 0 ? n + Math.max(1, Math.ceil(backlog / 10)) : n
      })
      raf = requestAnimationFrame(tick)
    })
    return () => cancelAnimationFrame(raf)
  }, [animate])

  return animate ? target.slice(0, shown) : target
}
