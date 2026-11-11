import { Link } from 'react-router-dom'
import { useRecents } from '../../hooks/useRecents'

function RecentList() {
  const { recents, loading } = useRecents()

  if (loading || recents.length === 0) return null

  return (
    <div>
      <p className="mb-1 px-3 text-xs font-semibold tracking-wide text-slate-400 uppercase">Recent</p>
      <ul className="flex flex-col">
        {recents.map((r) => (
          <li key={r.ticker}>
            <Link
              to={`/company/${r.ticker}?start=${r.start_year}&end=${r.end_year}`}
              className="flex items-center justify-between rounded-lg px-3 py-1.5 text-sm text-slate-600 transition-colors hover:bg-white/60"
            >
              <span className="font-medium">{r.ticker}</span>
              <span className="text-xs text-slate-400">
                {r.start_year}–{r.end_year}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default RecentList
