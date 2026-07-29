import type { RubricCategory } from '../enums/RubricCategory'
import type { Section } from '../enums/Sections'

// Mirrors the backend's `value.replace("_", " ").capitalize()` (Python
// capitalize() only uppercases the first letter of the whole string).
export function displayCategory(category: RubricCategory): string {
  const spaced = category.replaceAll('_', ' ')
  return spaced.charAt(0).toUpperCase() + spaced.slice(1)
}

// "part_i_item_1a" -> "Part I, Item 1A"
export function displaySection(section: Section): string {
  const match = section.match(/^part_([ivx]+)_item_(\d+)([a-z]?)$/)
  if (!match) return section
  const [, part, num, letter] = match
  return `Part ${part.toUpperCase()}, Item ${num}${letter.toUpperCase()}`
}
