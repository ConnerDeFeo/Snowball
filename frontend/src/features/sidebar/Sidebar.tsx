import { Link, NavLink } from 'react-router-dom'
import TickerSearch from '../../shared/TickerSearch'
import RecentList from './RecentList'

interface SidebarProps {
  children?: React.ReactNode
}

function Sidebar({ children }: SidebarProps) {
  return (
    <div className="flex h-full flex-col gap-4 border-r border-secondary-ice bg-secondary-ice/40 p-4">
      <Link to="/" className="flex items-center gap-2 text-lg font-bold text-slate-800">
        <span className="text-secondary-deep">❄</span>
        Snowball
      </Link>
      <TickerSearch />

      <div className="flex min-h-0 flex-1 flex-col gap-5 overflow-y-auto">
        {children}
        <RecentList />
      </div>

      <NavLink
        to="/checklist"
        className={({ isActive }) =>
          `rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
            isActive ? 'bg-white text-secondary-deep shadow-sm' : 'text-slate-600 hover:bg-white/60'
          }`
        }
      >
        ✎ Edit checklist
      </NavLink>
    </div>
  )
}

export default Sidebar
