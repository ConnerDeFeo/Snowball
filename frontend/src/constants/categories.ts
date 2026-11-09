import type { Section } from '../enums/Sections'
import type { Mention } from '../services/types/ReviewTypes'

// "part_i_item_1a" -> "Part I, Item 1A"
export function displaySection(section: Section): string {
  const match = section.match(/^part_([ivx]+)_item_(\d+)([a-z]?)$/)
  if (!match) return section
  const [, part, num, letter] = match
  return `Part ${part.toUpperCase()}, Item ${num}${letter.toUpperCase()}`
}

// "10-Q 2023 Q1 · Part II, Item 1A"
export function displayMention(m: Mention): string {
  return `${m.form} ${m.year}${m.quarter ? ` ${m.quarter}` : ''} · ${displaySection(m.section as Section)}`
}
