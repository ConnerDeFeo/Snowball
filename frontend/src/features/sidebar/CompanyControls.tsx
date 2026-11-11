import YearRangePicker from '../company/YearRangePicker'
import CompanyActions from '../company/CompanyActions'
import RunBanner from '../company/RunBanner'
import ViewNav from './ViewNav'
import type { CompanyView } from '../../constants/companyViews'
import type { YearRange } from '../../constants/yearRange'
import type { RunState } from '../../hooks/evidenceRunReducer'

interface CompanyControlsProps {
  tckr: string
  range: YearRange
  onRangeChange: (range: YearRange) => void
  view: CompanyView
  onViewChange: (view: CompanyView) => void
  checklistCount: string
  state: RunState
  active: boolean
  onRun: () => void
  onCancel: () => void
}

function CompanyControls(p: CompanyControlsProps) {
  return (
    <section className="flex flex-col gap-3">
      <h1 className="px-3 text-2xl font-bold text-slate-800">{p.tckr}</h1>
      <div className="px-3">
        <YearRangePicker range={p.range} onChange={p.onRangeChange} />
      </div>
      <ViewNav value={p.view} onChange={p.onViewChange} checklistCount={p.checklistCount} />
      <div className="px-3">
        <CompanyActions active={p.active} onRun={p.onRun} onCancel={p.onCancel} />
      </div>
      <div className="px-3">
        <RunBanner state={p.state} />
      </div>
    </section>
  )
}

export default CompanyControls
