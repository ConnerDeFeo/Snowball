import { useSearchParams } from 'react-router-dom'
import { COMPANY_VIEWS, DEFAULT_VIEW, EDIT_CHECKLIST_VIEW } from '../constants/companyViews'
import type { CompanyView } from '../constants/companyViews'

// The selected company view lives in the URL (?view=), like the year range.
export function useCompanyView() {
  const [searchParams, setSearchParams] = useSearchParams()
  const raw = searchParams.get('view')
  const valid = raw === EDIT_CHECKLIST_VIEW || COMPANY_VIEWS.some((v) => v.value === raw)
  const view: CompanyView = valid ? (raw as CompanyView) : DEFAULT_VIEW

  function setView(next: CompanyView) {
    setSearchParams((prev) => {
      const params = new URLSearchParams(prev)
      params.set('view', next)
      return params
    })
  }

  return { view, setView }
}
