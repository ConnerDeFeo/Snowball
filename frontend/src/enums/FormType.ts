export const FORM_TYPES = ['10-K', '10-Q', 'DEF 14A'] as const

export type FormType = (typeof FORM_TYPES)[number]

// DEF 14A has no valid Section enum on the backend, so only 10-K and 10-Q
// sections can be targeted.
export const SECTION_FORMS = ['10-K', '10-Q'] as const

export type SectionForm = (typeof SECTION_FORMS)[number]
