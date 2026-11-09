import { useCallback, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import YearRangePicker from '../features/company/YearRangePicker';
import CompanyActions from '../features/company/CompanyActions';
import RunBanner from '../features/company/RunBanner';
import CategoryGrid from '../features/company/CategoryGrid';
import CategoryDetail from '../features/company/CategoryDetail';
import { mergeEvidence } from '../features/company/mergeEvidence';
import ChatPanel from '../features/company/subfeatures/chat/ChatPanel';
import EmptyState from '../shared/EmptyState';
import { useYearRange } from '../hooks/useYearRange';
import { useEvidenceRun } from '../hooks/useEvidenceRun';
import { useEvidence } from '../hooks/useEvidence';
import { recordRecent } from '../hooks/useRecents';
import type { EvidenceCategory } from '../services/types/EvidenceTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const [sessionEvidence, setSessionEvidence] = useState<EvidenceCategory[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [chatOpen, setChatOpen] = useState(false)

  const { serverEvidence, error, loading, refresh } = useEvidence(tckr, range)

  const onResult = useCallback(
    (categories: EvidenceCategory[]) => setSessionEvidence((prev) => [...prev, ...categories]),
    [],
  )
  const { state, start, cancel } = useEvidenceRun({ tckr, range, onResult })

  useEffect(() => {
    if (tckr) recordRecent(tckr, range.start, range.end)
    // eslint-disable-next-line react-hooks/set-state-in-effect -- drops this tab's run results when ticker/range changes
    setSessionEvidence([])
  }, [tckr, range.start, range.end])

  const categories = mergeEvidence(serverEvidence, sessionEvidence)
  const selected = categories.find((c) => c.id === selectedId)
  const active = state.phase === 'fetching-docs' || state.phase === 'running'
  const hasAny = categories.length > 0

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-6 py-10">
      <h1 className="text-3xl font-bold text-slate-800">{tckr}</h1>

      <div className='flex justify-between items-center'>
        <CompanyActions
          active={active}
          onFetchFilings={() => start({ kind: 'documents-only' })}
          onRunChecklist={() => start({ kind: 'checklist' })}
          onAskSnowball={() => setChatOpen(true)}
        />
        <YearRangePicker range={range} onChange={setRange} />
      </div>

      <RunBanner state={state} onCancel={cancel} />

      {loading && !hasAny ? (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-2xl bg-secondary-ice" />
          ))}
        </div>
      ) : error && !hasAny ? (
        <EmptyState
          title="Couldn't load evidence"
          description={error}
          action={
            <button onClick={refresh} className="text-sm font-semibold text-secondary-deep underline">
              Retry
            </button>
          }
        />
      ) : !hasAny ? (
        <EmptyState
          title="No checklist yet"
          description="Add categories and questions to the checklist, then run it."
          action={
            <Link to="/checklist" className="text-sm font-semibold text-secondary-deep underline">
              Edit checklist
            </Link>
          }
        />
      ) : (
        <CategoryGrid categories={categories} selectedId={selectedId} onSelect={setSelectedId} />
      )}

      {selected && (
        <CategoryDetail
          category={selected}
          disabled={active}
          onRunCategory={() => start({ kind: 'category', categoryId: selected.id })}
          onRunQuestion={(questionId) => start({ kind: 'question', categoryId: selected.id, questionId })}
        />
      )}

      <ChatPanel tckr={tckr} range={range} open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}

export default Company;
