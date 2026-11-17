import CategoryList from './CategoryList'
import CategoryEditor from './CategoryEditor'
import EmptyState from '../../shared/EmptyState'
import { useChecklist } from '../../hooks/useChecklist'
import { useSelectedCategory } from '../../hooks/useSelectedCategory'

// Category list + editor for the selected category. Used inside the company page and standalone.
function ChecklistEditor() {
  const checklist = useChecklist()
  const { categoryId } = useSelectedCategory()

  return (
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
              {categoryId ? (
                <CategoryEditor categoryId={categoryId} checklist={checklist} />
              ) : (
                <EmptyState title="Select a category" description="Choose a checklist category from the list, or add a new one." />
              )}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default ChecklistEditor
