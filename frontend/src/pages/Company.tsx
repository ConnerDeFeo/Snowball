import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import AppShell from '../shared/layout/AppShell';
import CompanyControls from '../features/sidebar/CompanyControls';
import ChecklistView from '../features/company/ChecklistView';
import RunBanner from '../features/company/RunBanner';
import FinancialsView from '../features/financials/FinancialsView';
import EventsView from '../features/events/EventsView';
import InsidersView from '../features/insiders/InsidersView';
import ChecklistEditor from '../features/checklist/ChecklistEditor';
import { EDIT_CHECKLIST_VIEW } from '../constants/companyViews';
import ChatView from '../features/company/subfeatures/chat/ChatView';
import { mergeEvidence } from '../features/company/mergeEvidence';
import { countAnswered } from '../features/company/evidenceStats';
import { useYearRange } from '../hooks/useYearRange';
import { useCompanyView } from '../hooks/useCompanyView';
import { useSelectedCategory } from '../hooks/useSelectedCategory';
import { useAutoFetchFilings } from '../hooks/useAutoFetchFilings';
import { useSlashToChat } from '../hooks/useSlashToChat';
import { useChat } from '../hooks/useChat';
import { useChatModel } from '../hooks/useChatModel';
import { useEvidenceRun } from '../hooks/useEvidenceRun';
import { useEvidence } from '../hooks/useEvidence';
import { useFinancials } from '../hooks/useFinancials';
import { useEvents } from '../hooks/useEvents';
import { useInsiders } from '../hooks/useInsiders';
import { recordRecent } from '../hooks/useRecents';
import type { EvidenceCategory } from '../services/types/EvidenceTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const { view, setView } = useCompanyView()
  const { categoryId, select: selectCategory } = useSelectedCategory()
  const [sessionEvidence, setSessionEvidence] = useState<EvidenceCategory[]>([])
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const { model, setModel, effort, setEffort } = useChatModel()
  const chat = useChat({ tckr, range, model, effort })
  const { serverEvidence, error, loading, refresh } = useEvidence(tckr, range)
  const financials = useFinancials(tckr, range)
  const events = useEvents(tckr, range)
  const insiders = useInsiders(tckr, range)

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
  const { refresh: refreshInsiders } = insiders
  useEffect(() => {
    if (state.phase === 'done') {
      refreshFinancials()
      refreshEvents()
      refreshInsiders()
    }
  }, [state.phase, refreshFinancials, refreshEvents, refreshInsiders])

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

  // And for Insiders: nothing cached means Form 4 and 13D filings haven't been fetched yet.
  useAutoFetchFilings({
    enabled: view === 'insiders',
    empty: !insiders.loading && !insiders.error && insiders.filings.length === 0,
    busy: state.phase === 'fetching-docs' || state.phase === 'running',
    fetch: () => start({ kind: 'documents-only' }),
    key: `${tckr}:${range.start}-${range.end}`,
  })

  // Leaving the checklist editor: reload evidence so the Checklist tab shows the edits.
  const prevView = useRef(view)
  useEffect(() => {
    if (prevView.current === EDIT_CHECKLIST_VIEW && view !== EDIT_CHECKLIST_VIEW) refresh()
    prevView.current = view
  }, [view, refresh])

  useSlashToChat(() => {
    if (view !== 'chat') setView('chat')
    requestAnimationFrame(() => inputRef.current?.focus())
  })

  const categories = mergeEvidence(serverEvidence, sessionEvidence)
  const active = state.phase === 'fetching-docs' || state.phase === 'running'
  const answered = categories.reduce((sum, c) => sum + countAnswered(c), 0)
  const total = categories.reduce((sum, c) => sum + c.questions.length, 0)
  const selectedCategoryId = categories.find((c) => c.id === categoryId)?.id ?? categories[0]?.id

  const controls = (
    <CompanyControls
      tckr={tckr}
      range={range}
      onRangeChange={setRange}
      view={view}
      onViewChange={setView}
      checklistCount={total > 0 ? `${answered}/${total}` : ''}
      categories={categories}
      selectedCategoryId={selectedCategoryId}
      onSelectCategory={selectCategory}
      onFetchFilings={() => start({ kind: 'documents-only' })}
      onRunChecklist={() => start({ kind: 'checklist' })}
      onCancelRun={cancel}
      runState={state}
    />
  )

  return (
    <AppShell
      controls={controls}
      onEditChecklist={() => setView(EDIT_CHECKLIST_VIEW)}
      editingChecklist={view === EDIT_CHECKLIST_VIEW}
    >
      {view === EDIT_CHECKLIST_VIEW && <ChecklistEditor />}
      {view === 'chat' && (
        <ChatView tckr={tckr} range={range} chat={chat} inputRef={inputRef} model={model} onModelChange={setModel} effort={effort} onEffortChange={setEffort} />
      )}
      {view === 'checklist' && (
        <div className="h-full p-6">
          <ChecklistView
            categories={categories}
            selectedId={selectedCategoryId}
            loading={loading}
            error={error}
            onRetry={refresh}
            active={active}
            state={state}
            onStart={start}
            onEdit={() => setView(EDIT_CHECKLIST_VIEW)}
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
      {view === 'insiders' && (
        <div className="h-full overflow-y-auto p-6">
          <div className="mb-4">
            <RunBanner state={state} />
          </div>
          <InsidersView
            tckr={tckr}
            filings={insiders.filings}
            loading={insiders.loading}
            error={insiders.error}
            onRetry={insiders.refresh}
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
