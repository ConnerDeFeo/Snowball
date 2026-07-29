import Header from '../shared/Header'
import GradeCompanyForm from '../features/home/GradeCompanyForm'
import RecentCompanies from '../features/home/RecentCompanies'

function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-b from-primary to-secondary-ice">
      <Header />
      <main className="flex flex-1 flex-col items-center justify-center gap-8 px-6 pb-24">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-slate-800">
            Grade any <span className="text-secondary-deep">company</span>.
          </h1>
          <p className="mt-4 text-lg text-slate-500">
            Enter a ticker symbol and Snowball scores it on FCF fundamentals.
          </p>
        </div>
        <GradeCompanyForm />
        <RecentCompanies />
      </main>
    </div>
  )
}

export default Home
