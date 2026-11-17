import { Link, NavLink } from 'react-router-dom'
import TickerSearch from '../../shared/TickerSearch'
import RecentList from './RecentList'

interface SidebarProps {
  children?: React.ReactNode
  // Set on the company page so the editor opens in place instead of navigating away.
  onEditChecklist?: () => void
  editingChecklist?: boolean
}

const EDIT_LINK_CLASS = 'mr-4 rounded-lg px-3 py-2 text-sm font-medium transition-colors'
const activeClass = (active: boolean) =>
  active ? 'bg-white text-secondary-deep shadow-sm' : 'text-slate-600 hover:bg-white/60'

function Sidebar({ children, onEditChecklist, editingChecklist }: SidebarProps) {
  return (
    <div className="flex h-full flex-col gap-4 border-r border-secondary-ice bg-secondary-ice/40 py-4 pl-4">
      <Link to="/" className="flex items-center gap-2 pr-4 text-lg font-bold text-slate-800">
        <span className="text-secondary-deep">❄</span>
        Snowball
      </Link>
      <div className="pr-4">
        <TickerSearch />
      </div>

      <div className="flex min-h-0 flex-1 flex-col gap-5 overflow-y-auto">
        {children}
        <RecentList />
      </div>

      {onEditChecklist ? (
        <button
          data-close
          onClick={onEditChecklist}
          className={`${EDIT_LINK_CLASS} cursor-pointer text-left ${activeClass(!!editingChecklist)}`}
        >
          ✎ Edit checklist
        </button>
      ) : (
        <NavLink to="/checklist" className={({ isActive }) => `${EDIT_LINK_CLASS} ${activeClass(isActive)}`}>
          ✎ Edit checklist
        </NavLink>
      )}
    </div>
  )
}

export default Sidebar
