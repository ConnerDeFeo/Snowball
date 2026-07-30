import GradeCompanyForm from '../features/home/GradeCompanyForm'
import RecentCompanies from '../features/home/RecentCompanies'

function Home() {
  return (
    <div className="flex min-h-screen flex-col from-primary to-secondary-ice">
      <div className="flex flex-1 flex-col items-center justify-center gap-8">
        <GradeCompanyForm />
        <RecentCompanies />
      </div>
    </div>
  )
}

export default Home
