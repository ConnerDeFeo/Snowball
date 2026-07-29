import { NavLink } from 'react-router-dom'
import { RUBRIC_CATEGORIES } from '../../enums/RubricCategory'
import { displayCategory } from '../../constants/categories'
import type { useRubric } from '../../hooks/useRubric'

interface CategoryListProps {
  rubric: ReturnType<typeof useRubric>
}

function CategoryList({ rubric }: CategoryListProps) {
  return (
    <nav className="w-64 shrink-0 rounded-2xl border border-secondary-ice bg-white/70 p-3 shadow-lg shadow-secondary/20 backdrop-blur">
      <ul className="flex flex-col gap-1">
        {RUBRIC_CATEGORIES.map((category) => {
          const shape = rubric.shapes.get(category)
          return (
            <li key={category}>
              <NavLink
                to={`/rubric/${category}`}
                className={({ isActive }) =>
                  `flex items-center justify-between gap-2 rounded-lg px-3 py-2 text-sm transition-colors ${
                    isActive ? 'bg-secondary-ice text-slate-800' : 'text-slate-500 hover:bg-secondary-ice/60'
                  }`
                }
              >
                <span className="flex items-center gap-2">
                  <span
                    className={`h-2 w-2 shrink-0 rounded-full ${shape ? 'bg-secondary-deep' : 'bg-slate-300'}`}
                  />
                  {displayCategory(category)}
                </span>
                {shape && <span className="shrink-0 text-xs text-slate-400">{shape.version}</span>}
              </NavLink>
            </li>
          )
        })}
      </ul>
    </nav>
  )
}

export default CategoryList
