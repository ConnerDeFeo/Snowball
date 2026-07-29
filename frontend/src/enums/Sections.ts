import type { SubAgentForm } from './FormType'

export const TEN_K_SECTIONS = [
  'part_i_item_1',
  'part_i_item_1a',
  'part_i_item_1b',
  'part_i_item_2',
  'part_i_item_3',
  'part_i_item_4',
  'part_ii_item_5',
  'part_ii_item_6',
  'part_ii_item_7',
  'part_ii_item_7a',
  'part_ii_item_8',
  'part_ii_item_9',
  'part_ii_item_9a',
  'part_ii_item_9b',
  'part_iii_item_10',
  'part_iii_item_11',
  'part_iii_item_12',
  'part_iii_item_13',
  'part_iii_item_14',
  'part_iv_item_15',
  'part_iv_item_16',
] as const

export const TEN_Q_SECTIONS = [
  'part_i_item_1',
  'part_i_item_2',
  'part_i_item_3',
  'part_i_item_4',
  'part_ii_item_1',
  'part_ii_item_1a',
  'part_ii_item_2',
  'part_ii_item_3',
  'part_ii_item_4',
  'part_ii_item_5',
  'part_ii_item_6',
] as const

export type TenKSection = (typeof TEN_K_SECTIONS)[number]
export type TenQSection = (typeof TEN_Q_SECTIONS)[number]
export type Section = TenKSection | TenQSection

export function sectionsForForm(form: SubAgentForm): readonly Section[] {
  return form === '10-K' ? TEN_K_SECTIONS : TEN_Q_SECTIONS
}
