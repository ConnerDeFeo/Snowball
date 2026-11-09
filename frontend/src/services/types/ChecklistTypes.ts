import type { SubAgentForm } from '../../enums/FormType'
import type { Section } from '../../enums/Sections'

export interface SubAgent {
  id: string
  form: SubAgentForm
  section: Section
  prompt: string
  version: string
}

export interface Question {
  id: string
  text: string
  order: number
  latest_only: boolean
  version: string
  sub_agents: SubAgent[]
}

export interface Category {
  id: string
  name: string
  order: number
  questions: Question[]
}

export interface CategoryBody {
  name: string
  order: number
}

export interface QuestionBody {
  text: string
  order: number
  latest_only: boolean
}

export interface SubAgentBody {
  form: string
  section: string
  prompt: string
}

export interface IdResponse {
  id: string
}

export interface VersionResponse {
  version: string
}

export interface StatusResponse {
  status: string
}
