import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import YearRangePicker from '../features/company/YearRangePicker';
import CompanyActions from '../features/company//CompanyActions';
import GradeRunBanner from '../features/company//GradeRunBanner';
import GradesGrid from '../features/company//GradesGrid';
import CategoryDetail from '../features/company//CategoryDetail';
import { mergeGrades } from '../features/company//mergeGrades';
import ChatPanel from '../features/company//subfeatures/chat/ChatPanel';
import EmptyState from '../shared/EmptyState';
import { useYearRange } from '../hooks/useYearRange';
import { useGradeRun } from '../hooks/useGradeRun';
import { useGrades } from '../hooks/useGrades';
import { recordRecent } from '../hooks/useRecents';
import type { RubricCategory } from '../enums/RubricCategory';
import type { GradedTimePeriod } from '../services/types/GradingTypes';

function Company() {
  const { tckr = '' } = useParams<{ tckr: string }>()
  const { range, setRange } = useYearRange()
  const [sessionGrades, setSessionGrades] = useState<GradedTimePeriod[]>([])
  const [selected, setSelected] = useState<RubricCategory | null>(null)
  const [chatOpen, setChatOpen] = useState(false)

  const { serverGrades, error: gradesError, loading: gradesLoading, refresh: refreshGrades } = useGrades(tckr, range)

  const { state, start, cancel } = useGradeRun({
    tckr,
    range,
    onResult: (graded) => setSessionGrades((prev) => mergeSession(prev, graded)),
  })

  useEffect(() => {
    if (tckr) recordRecent(tckr, range.start, range.end)
  }, [tckr, range.start, range.end])

  const grades = mergeGrades(serverGrades, sessionGrades)
  const active = state.phase === 'fetching-docs' || state.phase === 'grading'
  const hasAnyGrades = grades.size > 0

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-6 py-10">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">{tckr}</h1>
          <p className="text-sm text-slate-500">
            {range.start}–{range.end}
          </p>
        </div>
        <YearRangePicker range={range} onApply={setRange} />
      </div>

      <CompanyActions
        active={active}
        onFetchFilings={() => start({ kind: 'documents-only' })}
        onGradeAll={() => start({ kind: 'all' })}
        onAskSnowball={() => setChatOpen(true)}
      />

      <GradeRunBanner state={state} onCancel={cancel} />

      {gradesLoading && !hasAnyGrades ? (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-2xl bg-secondary-ice" />
          ))}
        </div>
      ) : gradesError && !hasAnyGrades ? (
        <EmptyState
          title="Couldn't load grades"
          description={gradesError}
          action={
            <button onClick={refreshGrades} className="text-sm font-semibold text-secondary-deep underline">
              Retry
            </button>
          }
        />
      ) : !hasAnyGrades && !active ? (
        <EmptyState
          title={`No grades yet for ${tckr}`}
          description="Grade all to get started."
        />
      ) : (
        <GradesGrid grades={grades} selected={selected} onSelect={setSelected} />
      )}

      {selected && (
        <CategoryDetail
          category={selected}
          graded={grades.get(selected)}
          disabled={active}
          onGradeThis={() => start({ kind: 'section', category: selected })}
        />
      )}

      <ChatPanel tckr={tckr} range={range} open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  )
}

function mergeSession(prev: GradedTimePeriod[], next: GradedTimePeriod[]): GradedTimePeriod[] {
  const map = new Map(prev.map((g) => [g.category, g]))
  for (const g of next) map.set(g.category, g)
  return Array.from(map.values())
}

export default Company;
