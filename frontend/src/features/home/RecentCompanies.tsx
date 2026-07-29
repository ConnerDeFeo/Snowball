import { Link } from 'react-router-dom'
import { useRecents } from '../../hooks/useRecents'

function RecentCompanies() {
  const { recents, loading } = useRecents()

  if (loading || recents.length === 0) return null

  return (
    <div className="w-full max-w-xl">
      <p className="mb-2 text-sm font-medium text-slate-500">Recently graded</p>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {recents.map((r) => (
          <Link
            key={r.ticker}
            to={`/company/${r.ticker}?start=${r.start_year}&end=${r.end_year}`}
            className="rounded-xl border border-secondary-ice bg-white/70 px-4 py-3 text-center shadow-sm shadow-secondary/10 transition-colors hover:bg-secondary-ice/40"
          >
            <p className="font-semibold text-slate-800">{r.ticker}</p>
            <p className="text-xs text-slate-500">
              {r.start_year}–{r.end_year}
            </p>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default RecentCompanies
