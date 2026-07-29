import { useCallback, useEffect, useState } from 'react'
import * as CompanyService from '../services/CompanyService'
import { ApiError } from '../services/API'
import { RECENTS_KEY } from '../constants/storageKeys'
import type { RecentCompany } from '../services/CompanyService'

const MAX_RECENTS = 8

function readLocalRecents(): RecentCompany[] {
  try {
    const raw = localStorage.getItem(RECENTS_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function writeLocalRecents(recents: RecentCompany[]) {
  localStorage.setItem(RECENTS_KEY, JSON.stringify(recents.slice(0, MAX_RECENTS)))
}

export function recordRecent(ticker: string, start: number, end: number) {
  const existing = readLocalRecents().filter((r) => r.ticker !== ticker)
  writeLocalRecents([{ ticker, start_year: start, end_year: end }, ...existing])
}

export function useRecents() {
  const [recents, setRecents] = useState<RecentCompany[]>([])
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    try {
      const companies = await CompanyService.getCompanies()
      setRecents(companies)
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setRecents(readLocalRecents())
      } else {
        setRecents(readLocalRecents())
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- fetches the recents list on mount
    refresh()
  }, [refresh])

  return { recents, loading }
}
