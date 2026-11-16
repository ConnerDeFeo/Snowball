import type { InsiderFiling } from '../../services/types/InsidersTypes'

interface FilingListProps {
  filings: InsiderFiling[]
  selectedId: string | null
  onSelect: (id: string) => void
}

function FilingList({ filings, selectedId, onSelect }: FilingListProps) {
  if (filings.length === 0) return <p className="px-3 text-sm text-slate-500">No filings for this form.</p>

  return (
    <div className="flex max-h-[32rem] flex-col gap-1 overflow-y-auto">
      {filings.map((f) => (
        <button
          key={f.id}
          onClick={() => onSelect(f.id)}
          className={`cursor-pointer rounded-lg px-3 py-2 text-left transition-colors ${
            f.id === selectedId ? 'bg-white shadow-sm' : 'hover:bg-white/60'
          }`}
        >
          <p className="text-sm font-semibold text-slate-800">{f.filing_date}</p>
          <div className="mt-1 flex flex-wrap items-center gap-1">
            <span className="rounded-full bg-secondary-ice px-2 py-0.5 text-xs text-secondary-deep">{f.form}</span>
            {f.filer && <span className="truncate text-xs text-slate-500">{f.filer}</span>}
          </div>
        </button>
      ))}
    </div>
  )
}

export default FilingList
