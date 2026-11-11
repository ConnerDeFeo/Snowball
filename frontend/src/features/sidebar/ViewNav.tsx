import { COMPANY_VIEWS } from '../../constants/companyViews'
import type { CompanyView } from '../../constants/companyViews'

interface ViewNavProps {
  value: CompanyView | null
  onChange: (view: CompanyView) => void
  checklistCount?: string
}

function ViewNav({ value, onChange, checklistCount }: ViewNavProps) {
  return (
    <nav className="flex flex-col gap-1">
      {COMPANY_VIEWS.map((v) => (
        <button
          key={v.value}
          data-close
          onClick={() => onChange(v.value)}
          className={`flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${
            v.value === value ? 'bg-white font-semibold text-secondary-deep shadow-sm' : 'text-slate-600 hover:bg-white/60'
          }`}
        >
          {v.label}
          {v.value === 'checklist' && checklistCount && <span className="text-xs text-slate-400">{checklistCount}</span>}
        </button>
      ))}
    </nav>
  )
}

export default ViewNav
