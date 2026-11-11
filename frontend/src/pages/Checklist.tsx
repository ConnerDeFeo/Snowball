import { Outlet } from 'react-router-dom';
import AppShell from '../shared/layout/AppShell';
import EditorControls from '../features/sidebar/EditorControls';
import CategoryList from '../features/checklist/CategoryList';
import EmptyState from '../shared/EmptyState';
import { useChecklist } from '../hooks/useChecklist';

function Checklist() {
  const checklist = useChecklist()

  return (
    <AppShell controls={<EditorControls />}>
      <div className="h-full overflow-y-auto">
        <div className="mx-auto flex w-full max-w-6xl gap-6 px-6 py-10">
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
        </div>
      </div>
    </AppShell>
  )
}

export default Checklist
