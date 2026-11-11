import { Link } from 'react-router-dom'
import { useRecents } from '../../hooks/useRecents'

function RecentCompanies() {
  const { recents, loading } = useRecents()

  if (loading || recents.length === 0) return null

  return (
    <div className="flex max-w-xl flex-wrap justify-center gap-2">
      {recents.map((r) => (
        <Link
          key={r.ticker}
          to={`/company/${r.ticker}?start=${r.start_year}&end=${r.end_year}`}
          className="rounded-full border border-secondary-ice px-4 py-1.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-secondary-ice"
        >
          {r.ticker}
        </Link>
      ))}
    </div>
  )
}

export default RecentCompanies
