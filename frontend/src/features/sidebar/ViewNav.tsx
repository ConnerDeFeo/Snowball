import { COMPANY_VIEWS } from '../../constants/companyViews'
import CategoryNav from './CategoryNav'
import type { CompanyView } from '../../constants/companyViews'
import type { EvidenceCategory } from '../../services/types/EvidenceTypes'

interface ViewNavProps {
  value: CompanyView | null
  onChange: (view: CompanyView) => void
  checklistCount?: string
  // Shown under Checklist while it's the active view; the editor sidebar omits them.
  categories?: EvidenceCategory[]
  selectedCategoryId?: string
  onSelectCategory?: (id: string) => void
  // Rendered under the category list (the run button).
  checklistFooter?: React.ReactNode
}

function ViewNav({ value, onChange, checklistCount, categories = [], selectedCategoryId, onSelectCategory, checklistFooter }: ViewNavProps) {
  return (
    <nav className="flex flex-col gap-1">
      {COMPANY_VIEWS.map((v) => (
        <div key={v.value} className="flex flex-col gap-1">
          <button
            data-close
            onClick={() => onChange(v.value)}
            className={`flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${
              v.value === value ? 'bg-white font-semibold text-secondary-deep shadow-sm' : 'text-slate-600 hover:bg-white/60'
            }`}
          >
            {v.label}
            {v.value === 'checklist' && checklistCount && <span className="text-xs text-slate-400">{checklistCount}</span>}
          </button>
          {v.value === 'checklist' && value === 'checklist' && categories.length > 0 && onSelectCategory && (
            <>
              <CategoryNav categories={categories} selectedId={selectedCategoryId} onSelect={onSelectCategory} />
              {checklistFooter && <div className="ml-3 pl-2">{checklistFooter}</div>}
            </>
          )}
        </div>
      ))}
    </nav>
  )
}

export default ViewNav
