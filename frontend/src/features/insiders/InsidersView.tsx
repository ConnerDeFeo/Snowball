import { useState } from 'react'
import EmptyState from '../../shared/EmptyState'
import Spinner from '../../shared/Spinner'
import Tabs from '../../shared/Tabs'
import TransactionsTable from './TransactionsTable'
import FilingList from './FilingList'
import InsiderDocument from './InsiderDocument'
import { INSIDER_FORM_OPTIONS, type InsiderFormFilter } from '../../constants/insiders'
import type { InsiderFiling } from '../../services/types/InsidersTypes'

interface InsidersViewProps {
  tckr: string
  filings: InsiderFiling[]
  loading: boolean
  error: string | null
  onRetry: () => void
  fetching: boolean
}

function InsidersView({ tckr, filings, loading, error, onRetry, fetching }: InsidersViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [form, setForm] = useState<InsiderFormFilter>('all')

  if (loading && filings.length === 0) {
    return <div className="h-64 animate-pulse rounded-2xl bg-secondary-ice" />
  }
  if (error) {
    return (
      <EmptyState
        title="Couldn't load insider filings"
        description={error}
        action={
          <button onClick={onRetry} className="text-sm font-semibold text-secondary-deep underline">
            Retry
          </button>
        }
      />
    )
  }
  if (filings.length === 0) {
    return (
      <EmptyState
        title="No insider filings yet"
        description="Fetch filings for this year range to see Form 4 and 13D filings here."
        action={fetching && <span className="flex items-center gap-2 text-sm text-slate-500"><Spinner /> Fetching filings…</span>}
      />
    )
  }

  const visible = filings.filter((f) => form === 'all' || f.form === form)
  const selected = visible.find((f) => f.id === selectedId) ?? visible[0]

  return (
    <div className="flex flex-col gap-4">
      <TransactionsTable filings={filings} onSelect={(id) => { setForm('all'); setSelectedId(id) }} />
      <Tabs options={INSIDER_FORM_OPTIONS} value={form} onChange={setForm} />
      <div className="grid gap-4 md:grid-cols-[14rem_minmax(0,1fr)]">
        <FilingList filings={visible} selectedId={selected?.id ?? null} onSelect={setSelectedId} />
        {selected && <InsiderDocument tckr={tckr} id={selected.id} />}
      </div>
    </div>
  )
}

export default InsidersView
