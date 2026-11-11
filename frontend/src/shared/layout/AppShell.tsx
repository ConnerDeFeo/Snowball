import { useState } from 'react'
import Sidebar from '../../features/sidebar/Sidebar'

interface AppShellProps {
  controls?: React.ReactNode
  children: React.ReactNode
}

// Left control panel + main area. On small screens the panel is an off-canvas drawer.
function AppShell({ controls, children }: AppShellProps) {
  const [open, setOpen] = useState(false)

  // Close the drawer after navigating (links, or anything marked data-close).
  function handleSidebarClick(e: React.MouseEvent) {
    if ((e.target as HTMLElement).closest('a, [data-close]')) setOpen(false)
  }

  return (
    <div className="flex h-screen bg-primary">
      {open && <div className="fixed inset-0 z-20 bg-slate-900/30 lg:hidden" onClick={() => setOpen(false)} />}
      <aside
        onClick={handleSidebarClick}
        className={`fixed inset-y-0 left-0 z-30 w-64 shrink-0 transition-transform lg:static lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <Sidebar>{controls}</Sidebar>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex h-12 shrink-0 items-center px-3 lg:hidden">
          <button onClick={() => setOpen(true)} className="cursor-pointer rounded-lg px-2 py-1 text-xl text-secondary-deep hover:bg-secondary-ice" aria-label="Open menu">
            ☰
          </button>
        </div>
        <main className="min-h-0 flex-1">{children}</main>
      </div>
    </div>
  )
}

export default AppShell
