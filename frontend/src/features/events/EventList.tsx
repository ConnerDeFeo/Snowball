import { itemLabel } from '../../constants/eightKItems'
import type { EventMeta } from '../../services/types/EventsTypes'

interface EventListProps {
  events: EventMeta[]
  selectedId: string
  onSelect: (id: string) => void
}

function EventList({ events, selectedId, onSelect }: EventListProps) {
  return (
    <div className="flex flex-col gap-1">
      {events.map((e) => (
        <button
          key={e.id}
          onClick={() => onSelect(e.id)}
          className={`cursor-pointer rounded-lg px-3 py-2 text-left transition-colors ${
            e.id === selectedId ? 'bg-white shadow-sm' : 'hover:bg-white/60'
          }`}
        >
          <p className="text-sm font-semibold text-slate-800">{e.filing_date}</p>
          <div className="mt-1 flex flex-wrap gap-1">
            {e.items.map((item) => (
              <span key={item} className="rounded-full bg-secondary-ice px-2 py-0.5 text-xs text-secondary-deep">
                {itemLabel(item)}
              </span>
            ))}
          </div>
        </button>
      ))}
    </div>
  )
}

export default EventList
