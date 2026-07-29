import { parseSSE } from './sseParser'

const BASE = '/api'

export class ApiError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.status = status
    this.detail = detail
  }
}

interface FastApiValidationItem {
  msg?: string
}

async function normalizeDetail(res: Response): Promise<string> {
  try {
    const body = await res.json()
    const detail = body?.detail
    if (Array.isArray(detail)) {
      return detail
        .map((item: FastApiValidationItem) => item?.msg)
        .filter(Boolean)
        .join('; ') || res.statusText
    }
    if (typeof detail === 'string') return detail
    return res.statusText
  } catch {
    return res.statusText
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(BASE + path, init)
  if (!res.ok) {
    throw new ApiError(res.status, await normalizeDetail(res))
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

function jsonInit(method: string, body?: unknown): RequestInit {
  return {
    method,
    headers: body !== undefined ? { 'Content-Type': 'application/json' } : undefined,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  }
}

export function get<T>(path: string): Promise<T> {
  return request<T>(path, { method: 'GET' })
}

export function post<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, jsonInit('POST', body))
}

export function patch<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, jsonInit('PATCH', body))
}

export function del<T>(path: string): Promise<T> {
  return request<T>(path, { method: 'DELETE' })
}

interface StreamOptions {
  method?: 'GET' | 'POST'
  body?: unknown
  signal?: AbortSignal
  onFrame: (frame: unknown) => void
}

export async function stream(path: string, opts: StreamOptions): Promise<void> {
  const { method = 'GET', body, signal, onFrame } = opts
  try {
    const res = await fetch(BASE + path, {
      method,
      headers: {
        Accept: 'text/event-stream',
        ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal,
    })
    if (!res.ok) {
      throw new ApiError(res.status, await normalizeDetail(res))
    }
    if (!res.body) return
    await parseSSE(res.body, onFrame)
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') return
    throw err
  }
}
