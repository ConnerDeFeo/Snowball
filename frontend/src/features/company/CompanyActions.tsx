import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'

interface CompanyActionsProps {
  active: boolean
  onFetchFilings: () => void
  onRunChecklist: () => void
  onAskSnowball: () => void
}

function CompanyActions({ active, onFetchFilings, onRunChecklist, onAskSnowball }: CompanyActionsProps) {
  return (
    <div className="flex flex-wrap gap-3">
      <Button variant="ghost" onClick={onFetchFilings} disabled={active}>
        {active ? <Spinner /> : 'Fetch filings'}
      </Button>
      <Button onClick={onRunChecklist} disabled={active}>
        {active ? <Spinner /> : 'Run checklist'}
      </Button>
      <Button variant="ghost" onClick={onAskSnowball}>
        Ask Snowball
      </Button>
    </div>
  )
}

export default CompanyActions
