import { Outlet } from 'react-router-dom';
import CategoryList from '../features/rubric/CategoryList';
import EmptyState from '../shared/EmptyState';
import { useRubric } from '../hooks/useRubric';

function Rubric() {
  const rubric = useRubric()

  return (
    <div className="flex min-h-screen flex-col from-primary to-secondary-ice">
      <main className="mx-auto flex w-full max-w-6xl flex-1 gap-6 px-6 py-10">
        {rubric.error ? (
          <div className="flex-1">
            <EmptyState
              title="Couldn't load the rubric"
              description={rubric.error}
              action={
                <button onClick={rubric.refresh} className="text-sm font-semibold text-secondary-deep underline">
                  Retry
                </button>
              }
            />
          </div>
        ) : (
          <>
            <CategoryList rubric={rubric} />
            <div className="flex-1">
              <Outlet context={rubric} />
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default Rubric
