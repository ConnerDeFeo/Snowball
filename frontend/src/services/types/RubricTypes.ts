import type { RubricCategory } from '../../enums/RubricCategory'

export interface SubAgentDirection {
  prompt: string
  version: string
}

export interface RubricShape {
  rubric_category: RubricCategory
  name: string
  directions: string
  version: string
  sub_agent_directions: Record<string, SubAgentDirection>
}

export interface CreateRubricBody {
  name: string
  directions: string
}

export interface EditRubricBody {
  directions?: string
}

export interface SubAgentBody {
  form: string
  section: string
  prompt: string
}

export interface VersionResponse {
  version: string
}

export interface StatusResponse {
  status: string
}
