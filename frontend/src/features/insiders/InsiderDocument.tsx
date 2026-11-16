import Card from '../../shared/Card'
import Markdown from '../../shared/Markdown'
import { useInsiderDoc } from '../../hooks/useInsiderDoc'

function InsiderDocument({ tckr, id }: { tckr: string; id: string }) {
  const { markdown, error, loading } = useInsiderDoc(tckr, id)

  return (
    <Card className="min-w-0">
      {loading && <div className="h-64 animate-pulse rounded-xl bg-secondary-ice" />}
      {error && <p className="text-sm text-red-600">{error}</p>}
      {!loading && !error && (markdown ? <Markdown>{markdown}</Markdown> : <p className="text-sm text-slate-500">This filing has no text.</p>)}
    </Card>
  )
}

export default InsiderDocument
