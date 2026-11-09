import type { SectionForm } from '../../enums/FormType'
import type { Section } from '../../enums/Sections'

export interface Question {
  id: string
  text: string
  form: SectionForm
  section: Section
  order: number
  latest_only: boolean
  version: string
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
  form: string
  section: string
  order: number
  latest_only: boolean
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
