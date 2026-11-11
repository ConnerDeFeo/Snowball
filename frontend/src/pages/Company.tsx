import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import AppShell from '../shared/layout/AppShell';
import CompanyControls from '../features/sidebar/CompanyControls';
import ChecklistView from '../features/company/ChecklistView';
import FinancialsView from '../features/financials/FinancialsView';
import ChatView from '../features/company/subfeatures/chat/ChatView';
import { mergeEvidence } from '../features/company/mergeEvidence';
import { countAnswered } from '../features/company/evidenceStats';
import { useYearRange } from '../hooks/useYearRange';
import { useCompanyView } from '../hooks/useCompanyView';
import { useAutoFetchFilings } from '../hooks/useAutoFetchFilings';
import { useSlashToChat } from '../hooks/useSlashToChat';
import { useChat } from '../hooks/useChat';
import { useEvidenceRun } from '../hooks/useEvidenceRun';
import { useEvidence } from '../hooks/useEvidence';
import { useFinancials } from '../hooks/useFinancials';
import { recordRecent } from '../hooks/useRecents';
import type { EvidenceCategory } from '../services/types/EvidenceTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const { view, setView } = useCompanyView()
  const [sessionEvidence, setSessionEvidence] = useState<EvidenceCategory[]>([])
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const chat = useChat({ tckr, range })
  const { serverEvidence, error, loading, refresh } = useEvidence(tckr, range)
  const financials = useFinancials(tckr, range)

  const onResult = useCallback(
    (categories: EvidenceCategory[]) => setSessionEvidence((prev) => [...prev, ...categories]),
    [],
  )
  const { state, start, cancel } = useEvidenceRun({ tckr, range, onResult })

  useEffect(() => {
    if (tckr) recordRecent(tckr, range.start, range.end)
    // eslint-disable-next-line react-hooks/set-state-in-effect -- drops this tab's run results when ticker/range changes
    setSessionEvidence([])
    cancel() // clear the previous company's run state (and its error banner)
  }, [tckr, range.start, range.end, cancel])

  // A finished run may have just downloaded new filings, so reload their statements.
  const { refresh: refreshFinancials } = financials
  useEffect(() => {
    if (state.phase === 'done') refreshFinancials()
  }, [state.phase, refreshFinancials])

  // Opening Financials with nothing cached fetches the filings automatically.
  useAutoFetchFilings({
    enabled: view === 'financials',
    empty: !financials.loading && !financials.error && financials.filings.length === 0,
    busy: state.phase === 'fetching-docs' || state.phase === 'running',
    fetch: () => start({ kind: 'documents-only' }),
    key: `${tckr}:${range.start}-${range.end}`,
  })

  useSlashToChat(() => {
    if (view !== 'chat') setView('chat')
    requestAnimationFrame(() => inputRef.current?.focus())
  })

  const categories = mergeEvidence(serverEvidence, sessionEvidence)
  const active = state.phase === 'fetching-docs' || state.phase === 'running'
  const answered = categories.reduce((sum, c) => sum + countAnswered(c), 0)
  const total = categories.reduce((sum, c) => sum + c.questions.length, 0)

  const controls = (
    <CompanyControls
      tckr={tckr}
      range={range}
      onRangeChange={setRange}
      view={view}
      onViewChange={setView}
      checklistCount={total > 0 ? `${answered}/${total}` : ''}
      state={state}
      active={active}
      onRun={() => start({ kind: 'checklist' })}
      onCancel={cancel}
    />
  )

  return (
    <AppShell controls={controls}>
      {view === 'chat' && <ChatView tckr={tckr} range={range} chat={chat} inputRef={inputRef} />}
      {view === 'checklist' && (
        <div className="h-full p-6">
          <ChecklistView
            categories={categories}
            loading={loading}
            error={error}
            onRetry={refresh}
            active={active}
            onStart={start}
          />
        </div>
      )}
      {view === 'financials' && (
        <div className="h-full overflow-y-auto p-6">
          <FinancialsView
            filings={financials.filings}
            loading={financials.loading}
            error={financials.error}
            onRetry={financials.refresh}
            onFetch={() => start({ kind: 'documents-only' })}
            fetching={active}
          />
        </div>
      )}
    </AppShell>
  )
}

export default Company;
