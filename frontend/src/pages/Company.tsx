import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import YearRangePicker from '../features/company/YearRangePicker';
import CompanyActions from '../features/company/CompanyActions';
import RunBanner from '../features/company/RunBanner';
import ChecklistView from '../features/company/ChecklistView';
import FinancialsView from '../features/financials/FinancialsView';
import { mergeEvidence } from '../features/company/mergeEvidence';
import ChatPanel from '../features/company/subfeatures/chat/ChatPanel';
import Tabs from '../shared/Tabs';
import { COMPANY_TABS } from '../constants/companyTabs';
import { useYearRange } from '../hooks/useYearRange';
import { useEvidenceRun } from '../hooks/useEvidenceRun';
import { useEvidence } from '../hooks/useEvidence';
import { useFinancials } from '../hooks/useFinancials';
import { recordRecent } from '../hooks/useRecents';
import type { CompanyTab } from '../constants/companyTabs';
import type { EvidenceCategory } from '../services/types/EvidenceTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const [sessionEvidence, setSessionEvidence] = useState<EvidenceCategory[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [chatOpen, setChatOpen] = useState(false)
  const [tab, setTab] = useState<CompanyTab>('checklist')

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
  }, [tckr, range.start, range.end])

  // A finished run may have just downloaded new filings, so reload their statements.
  const { refresh: refreshFinancials } = financials
  useEffect(() => {
    if (state.phase === 'done') refreshFinancials()
  }, [state.phase, refreshFinancials])

  const categories = mergeEvidence(serverEvidence, sessionEvidence)
  const active = state.phase === 'fetching-docs' || state.phase === 'running'

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

      <Tabs options={COMPANY_TABS} value={tab} onChange={setTab} />

      {tab === 'checklist' ? (
        <ChecklistView
          categories={categories}
          loading={loading}
          error={error}
          onRetry={refresh}
          selectedId={selectedId}
          onSelect={setSelectedId}
          active={active}
          onStart={start}
        />
      ) : (
        <FinancialsView
          filings={financials.filings}
          loading={financials.loading}
          error={financials.error}
          onRetry={financials.refresh}
        />
      )}

      <ChatPanel tckr={tckr} range={range} open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}

export default Company;
