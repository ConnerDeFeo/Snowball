import { useNavigate } from 'react-router-dom'
import ViewNav from './ViewNav'
import { lastCompany } from '../../hooks/useRecents'
import type { CompanyView } from '../../constants/companyViews'

// Sidebar section for the checklist editor: jump back to the last company's views.
function EditorControls() {
  const navigate = useNavigate()
  const last = lastCompany()
  if (!last) return null

  function go(view: CompanyView) {
    navigate(`/company/${last!.ticker}?start=${last!.start_year}&end=${last!.end_year}&view=${view}`)
  }

  return (
    <section className="flex flex-col gap-2">
      <h1 className="px-3 text-2xl font-bold text-slate-800">{last.ticker}</h1>
      <ViewNav value={null} onChange={go} />
    </section>
  )
}

export default EditorControls
