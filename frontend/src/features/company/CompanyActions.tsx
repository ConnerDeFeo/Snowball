import Button from '../../shared/Button'
import Spinner from '../../shared/Spinner'

interface CompanyActionsProps {
  active: boolean
  onRun: () => void
  onCancel: () => void
}

// One action: run the checklist (it fetches filings first). Turns into Cancel while running.
function CompanyActions({ active, onRun, onCancel }: CompanyActionsProps) {
  return (
    <div className="[&>button]:w-full">
      {active ? (
        <Button variant="ghost" onClick={onCancel}>
          <span className="flex items-center justify-center gap-2">
            <Spinner /> Cancel
          </span>
        </Button>
      ) : (
        <Button onClick={onRun}>Run checklist ▸</Button>
      )}
    </div>
  )
}

export default CompanyActions
