// Parses a `data: {json}\n\n` SSE stream (no `event:` field, no end
// sentinel — stream closure is the only signal that it's done).
export async function parseSSE(
  body: ReadableStream<Uint8Array>,
  onFrame: (frame: unknown) => void,
): Promise<void> {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  const consumeEvent = (rawEvent: string) => {
    for (const line of rawEvent.split('\n')) {
      if (!line.startsWith('data:')) continue
      const payload = line.slice(5).trimStart()
      if (!payload) continue
      onFrame(JSON.parse(payload))
    }
  }

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    buffer = buffer.replaceAll('\r\n', '\n')

    let boundary: number
    while ((boundary = buffer.indexOf('\n\n')) !== -1) {
      const rawEvent = buffer.slice(0, boundary)
      buffer = buffer.slice(boundary + 2)
      if (rawEvent) consumeEvent(rawEvent)
    }
  }

  buffer += decoder.decode()
  const trailing = buffer.trim()
  if (trailing) consumeEvent(trailing)
}
