export const FORM_TYPES = ['10-K', '10-Q', 'DEF 14A'] as const

export type FormType = (typeof FORM_TYPES)[number]

// DEF 14A has no valid Section enum on the backend, so sub-agents can only
// target 10-K or 10-Q filing sections.
export const SUB_AGENT_FORMS = ['10-K', '10-Q'] as const

export type SubAgentForm = (typeof SUB_AGENT_FORMS)[number]
