import Header from '../shared/Header'
import CompanyDashboard from '../features/company/CompanyDashboard'

function Company() {
  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-b from-primary to-secondary-ice">
      <Header />
      <CompanyDashboard />
    </div>
  )
}

export default Company
