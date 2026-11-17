import AddCategoryForm from './AddCategoryForm'
import { useSelectedCategory } from '../../hooks/useSelectedCategory'
import type { useChecklist } from '../../hooks/useChecklist'

interface CategoryListProps {
  checklist: ReturnType<typeof useChecklist>
}

function CategoryList({ checklist }: CategoryListProps) {
  const { categoryId, select } = useSelectedCategory()

  async function handleCreated(newId: string) {
    await checklist.refresh()
    select(newId)
  }

  return (
    <nav className="w-64 shrink-0 self-start rounded-2xl border border-secondary-ice bg-white/70 p-3 shadow-lg shadow-secondary/20 backdrop-blur">
      <ul className="flex flex-col gap-1">
        {checklist.categories.map((category) => (
          <li key={category.id}>
            <button
              data-close
              onClick={() => select(category.id)}
              className={`flex w-full cursor-pointer items-center justify-between gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors ${
                category.id === categoryId ? 'bg-secondary-ice text-slate-800' : 'text-slate-500 hover:bg-secondary-ice/60'
              }`}
            >
              <span>{category.name}</span>
              <span className="shrink-0 text-xs text-slate-400">{category.questions.length}</span>
            </button>
          </li>
        ))}
        {!checklist.loading && checklist.categories.length === 0 && (
          <li className="px-3 py-2 text-sm text-slate-500">No categories yet.</li>
        )}
      </ul>
      <AddCategoryForm nextOrder={checklist.categories.length} onCreated={handleCreated} />
    </nav>
  )
}

export default CategoryList
