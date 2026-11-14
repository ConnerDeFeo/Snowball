import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import AppShell from '../shared/layout/AppShell';
import CompanyControls from '../features/sidebar/CompanyControls';
import ChecklistView from '../features/company/ChecklistView';
import RunBanner from '../features/company/RunBanner';
import FinancialsView from '../features/financials/FinancialsView';
import EventsView from '../features/events/EventsView';
import ChatView from '../features/company/subfeatures/chat/ChatView';
import { mergeEvidence } from '../features/company/mergeEvidence';
import { countAnswered } from '../features/company/evidenceStats';
import { useYearRange } from '../hooks/useYearRange';
import { useCompanyView } from '../hooks/useCompanyView';
import { useAutoFetchFilings } from '../hooks/useAutoFetchFilings';
import { useSlashToChat } from '../hooks/useSlashToChat';
import { useChat } from '../hooks/useChat';
import { useChatModel } from '../hooks/useChatModel';
import { useEvidenceRun } from '../hooks/useEvidenceRun';
import { useEvidence } from '../hooks/useEvidence';
import { useFinancials } from '../hooks/useFinancials';
import { useEvents } from '../hooks/useEvents';
import { recordRecent } from '../hooks/useRecents';
import type { EvidenceCategory } from '../services/types/EvidenceTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const { view, setView } = useCompanyView()
  const [sessionEvidence, setSessionEvidence] = useState<EvidenceCategory[]>([])
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const { model, setModel } = useChatModel()
  const chat = useChat({ tckr, range, model })
  const { serverEvidence, error, loading, refresh } = useEvidence(tckr, range)
  const financials = useFinancials(tckr, range)
  const events = useEvents(tckr, range)

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

  // A finished run may have just downloaded new filings, so reload their statements and events.
  const { refresh: refreshFinancials } = financials
  const { refresh: refreshEvents } = events
  useEffect(() => {
    if (state.phase === 'done') {
      refreshFinancials()
      refreshEvents()
    }
  }, [state.phase, refreshFinancials, refreshEvents])

  // Opening Financials with nothing cached fetches the filings automatically.
  useAutoFetchFilings({
    enabled: view === 'financials',
    empty: !financials.loading && !financials.error && financials.filings.length === 0,
    busy: state.phase === 'fetching-docs' || state.phase === 'running',
    fetch: () => start({ kind: 'documents-only' }),
    key: `${tckr}:${range.start}-${range.end}`,
  })

  // Same for Events: nothing cached means the 8-Ks haven't been fetched yet.
  useAutoFetchFilings({
    enabled: view === 'events',
    empty: !events.loading && !events.error && events.events.length === 0,
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
    />
  )

  return (
    <AppShell controls={controls}>
      {view === 'chat' && (
        <ChatView tckr={tckr} range={range} chat={chat} inputRef={inputRef} model={model} onModelChange={setModel} />
      )}
      {view === 'checklist' && (
        <div className="h-full p-6">
          <ChecklistView
            categories={categories}
            loading={loading}
            error={error}
            onRetry={refresh}
            active={active}
            state={state}
            onStart={start}
            onRun={() => start({ kind: 'checklist' })}
            onCancel={cancel}
          />
        </div>
      )}
      {view === 'financials' && (
        <div className="h-full overflow-y-auto p-6">
          <div className="mb-4">
            <RunBanner state={state} />
          </div>
          <FinancialsView
            filings={financials.filings}
            loading={financials.loading}
            error={financials.error}
            onRetry={financials.refresh}
            fetching={active}
          />
        </div>
      )}
      {view === 'events' && (
        <div className="h-full overflow-y-auto p-6">
          <div className="mb-4">
            <RunBanner state={state} />
          </div>
          <EventsView
            tckr={tckr}
            events={events.events}
            loading={events.loading}
            error={events.error}
            onRetry={events.refresh}
            fetching={active}
          />
        </div>
      )}
    </AppShell>
  )
}

export default Company;
