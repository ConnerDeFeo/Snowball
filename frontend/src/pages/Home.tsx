import AppShell from '../shared/layout/AppShell'
import TickerSearch from '../shared/TickerSearch'
import RecentCompanies from '../features/home/RecentCompanies'

function Home() {
  return (
    <AppShell>
      <div className="flex h-full flex-col items-center justify-center gap-6 px-6 pb-16">
        <TickerSearch large autoFocus />
        <RecentCompanies />
      </div>
    </AppShell>
  )
}

export default Home
