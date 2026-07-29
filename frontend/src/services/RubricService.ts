import { get, post, patch, del } from './API'
import type { RubricCategory } from '../enums/RubricCategory'
import type {
  RubricShape,
  CreateRubricBody,
  EditRubricBody,
  SubAgentBody,
  VersionResponse,
  StatusResponse,
} from './types/RubricTypes'

export function getRubric(): Promise<RubricShape[]> {
  return get<RubricShape[]>('/rubric')
}

export function getCategory(category: RubricCategory): Promise<RubricShape> {
  return get<RubricShape>(`/rubric/${category}`)
}

export function createMeta(category: RubricCategory, body: CreateRubricBody): Promise<VersionResponse> {
  return post<VersionResponse>(`/rubric/${category}`, body)
}

export function patchDirections(category: RubricCategory, body: EditRubricBody): Promise<VersionResponse> {
  return patch<VersionResponse>(`/rubric/${category}`, body)
}

export function deleteMeta(category: RubricCategory): Promise<StatusResponse> {
  return del<StatusResponse>(`/rubric/${category}`)
}

export function createSubAgent(category: RubricCategory, body: SubAgentBody): Promise<VersionResponse> {
  return post<VersionResponse>(`/rubric/${category}/sub_agent`, body)
}

export function patchSubAgent(category: RubricCategory, body: SubAgentBody): Promise<VersionResponse> {
  return patch<VersionResponse>(`/rubric/${category}/sub_agent`, body)
}

export function deleteSubAgent(
  category: RubricCategory,
  form: string,
  section: string,
): Promise<StatusResponse> {
  const params = new URLSearchParams({ form, section })
  return del<StatusResponse>(`/rubric/${category}/sub_agent?${params.toString()}`)
}
