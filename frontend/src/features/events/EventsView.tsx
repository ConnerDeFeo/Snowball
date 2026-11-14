import { useState } from 'react'
import EmptyState from '../../shared/EmptyState'
import Spinner from '../../shared/Spinner'
import EventList from './EventList'
import EventDocument from './EventDocument'
import type { EventMeta } from '../../services/types/EventsTypes'

interface EventsViewProps {
  tckr: string
  events: EventMeta[]
  loading: boolean
  error: string | null
  onRetry: () => void
  fetching: boolean
}

function EventsView({ tckr, events, loading, error, onRetry, fetching }: EventsViewProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)

  if (loading && events.length === 0) {
    return <div className="h-64 animate-pulse rounded-2xl bg-secondary-ice" />
  }
  if (error) {
    return (
      <EmptyState
        title="Couldn't load events"
        description={error}
        action={
          <button onClick={onRetry} className="text-sm font-semibold text-secondary-deep underline">
            Retry
          </button>
        }
      />
    )
  }
  if (events.length === 0) {
    return (
      <EmptyState
        title="No events yet"
        description="Fetch filings for this year range to see 8-Ks here."
        action={fetching && <span className="flex items-center gap-2 text-sm text-slate-500"><Spinner /> Fetching filings…</span>}
      />
    )
  }

  const selected = events.find((e) => e.id === selectedId) ?? events[0]

  return (
    <div className="grid gap-4 md:grid-cols-[12rem_minmax(0,1fr)]">
      <EventList events={events} selectedId={selected.id} onSelect={setSelectedId} />
      <EventDocument tckr={tckr} id={selected.id} />
    </div>
  )
}

export default EventsView
