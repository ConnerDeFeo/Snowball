import { useSearchParams } from 'react-router-dom'

// The category open in the checklist editor lives in the URL (?category=), like the view and year range.
export function useSelectedCategory() {
  const [searchParams, setSearchParams] = useSearchParams()
  const categoryId = searchParams.get('category')

  function select(id: string | null) {
    setSearchParams((prev) => {
      const params = new URLSearchParams(prev)
      if (id) params.set('category', id)
      else params.delete('category')
      return params
    })
  }

  return { categoryId, select }
}
