import YearRangePicker from '../company/YearRangePicker'
import ViewNav from './ViewNav'
import CompanyActions from '../company/CompanyActions'
import Button from '../../shared/Button'
import ProgressBar from '../../shared/ProgressBar'
import type { RunState } from '../../hooks/evidenceRunReducer'
import type { CompanyView } from '../../constants/companyViews'
import type { YearRange } from '../../constants/yearRange'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface CompanyControlsProps {
  tckr: string
  range: YearRange
  onRangeChange: (range: YearRange) => void
  view: CompanyView
  onViewChange: (view: CompanyView) => void
  checklistCount: string
  categories: EvidenceCategory[]
  selectedCategoryId: string | undefined
  onSelectCategory: (id: string) => void
  onFetchFilings: () => void
  onRunChecklist: () => void
  onCancelRun: () => void
  runState: RunState
}

function CompanyControls(p: CompanyControlsProps) {
  return (
    <section className="flex flex-col gap-3 pr-4">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-slate-800">{p.tckr}</h1>
        {p.runState.phase === 'fetching-docs' || p.runState.phase === 'running' ? (
          <div className="w-28" title={`${p.runState.completed}/${p.runState.total}`}>
            <ProgressBar completed={p.runState.completed} total={p.runState.total} />
          </div>
        ) : (
          <Button variant="ghost" size="xs" onClick={p.onFetchFilings}>
            Fetch filings
          </Button>
        )}
      </div>
        <YearRangePicker range={p.range} onChange={p.onRangeChange} />
      <ViewNav
        value={p.view}
        onChange={p.onViewChange}
        checklistCount={p.checklistCount}
        categories={p.categories}
        selectedCategoryId={p.selectedCategoryId}
        onSelectCategory={p.onSelectCategory}
        checklistFooter={
          <CompanyActions
            active={p.runState.phase === 'fetching-docs' || p.runState.phase === 'running'}
            onRun={p.onRunChecklist}
            onCancel={p.onCancelRun}
          />
        }
      />
    </section>
  )
}

export default CompanyControls
