import YearRangePicker from '../company/YearRangePicker'
import ViewNav from './ViewNav'
import Button from '../../shared/Button'
import type { CompanyView } from '../../constants/companyViews'
import type { YearRange } from '../../constants/yearRange'

interface CompanyControlsProps {
  tckr: string
  range: YearRange
  onRangeChange: (range: YearRange) => void
  view: CompanyView
  onViewChange: (view: CompanyView) => void
  checklistCount: string
  onFetchFilings: () => void
  fetching: boolean
}

function CompanyControls(p: CompanyControlsProps) {
  return (
    <section className="flex flex-col gap-3 pr-4">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-slate-800">{p.tckr}</h1>
        <Button variant="ghost" size="xs" onClick={p.onFetchFilings} disabled={p.fetching}>
          {p.fetching ? 'Fetching…' : 'Fetch filings'}
        </Button>
      </div>
        <YearRangePicker range={p.range} onChange={p.onRangeChange} />
      <ViewNav value={p.view} onChange={p.onViewChange} checklistCount={p.checklistCount} />
    </section>
  )
}

export default CompanyControls
