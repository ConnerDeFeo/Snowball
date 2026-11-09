import { Outlet } from 'react-router-dom';
import CategoryList from '../features/checklist/CategoryList';
import EmptyState from '../shared/EmptyState';
import { useChecklist } from '../hooks/useChecklist';

function Checklist() {
  const checklist = useChecklist()

  return (
    <div className="flex min-h-screen flex-col from-primary to-secondary-ice">
      <main className="mx-auto flex w-full max-w-6xl flex-1 gap-6 px-6 py-10">
        {checklist.error ? (
          <div className="flex-1">
            <EmptyState
              title="Couldn't load the checklist"
              description={checklist.error}
              action={
                <button onClick={checklist.refresh} className="text-sm font-semibold text-secondary-deep underline">
                  Retry
                </button>
              }
            />
          </div>
        ) : (
          <>
            <CategoryList checklist={checklist} />
            <div className="flex-1">
              <Outlet context={checklist} />
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default Checklist
