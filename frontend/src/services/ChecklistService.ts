import { get, post, patch, del } from './API'
import type {
  Category,
  CategoryBody,
  QuestionBody,
  SubAgentBody,
  IdResponse,
  VersionResponse,
  StatusResponse,
} from './types/ChecklistTypes'

export function getChecklist(): Promise<Category[]> {
  return get<Category[]>('/checklist')
}

export function createCategory(body: CategoryBody): Promise<IdResponse> {
  return post<IdResponse>('/checklist', body)
}

export function patchCategory(categoryId: string, body: Partial<CategoryBody>): Promise<StatusResponse> {
  return patch<StatusResponse>(`/checklist/${categoryId}`, body)
}

export function deleteCategory(categoryId: string): Promise<StatusResponse> {
  return del<StatusResponse>(`/checklist/${categoryId}`)
}

export function createQuestion(categoryId: string, body: QuestionBody): Promise<IdResponse> {
  return post<IdResponse>(`/checklist/${categoryId}/questions`, body)
}

export function patchQuestion(categoryId: string, qid: string, body: Partial<QuestionBody>): Promise<StatusResponse> {
  return patch<StatusResponse>(`/checklist/${categoryId}/questions/${qid}`, body)
}

export function deleteQuestion(categoryId: string, qid: string): Promise<StatusResponse> {
  return del<StatusResponse>(`/checklist/${categoryId}/questions/${qid}`)
}

export function createSubAgent(categoryId: string, qid: string, body: SubAgentBody): Promise<IdResponse> {
  return post<IdResponse>(`/checklist/${categoryId}/questions/${qid}/sub_agents`, body)
}

export function patchSubAgent(
  categoryId: string,
  qid: string,
  said: string,
  body: Partial<SubAgentBody>,
): Promise<VersionResponse> {
  return patch<VersionResponse>(`/checklist/${categoryId}/questions/${qid}/sub_agents/${said}`, body)
}

export function deleteSubAgent(categoryId: string, qid: string, said: string): Promise<StatusResponse> {
  return del<StatusResponse>(`/checklist/${categoryId}/questions/${qid}/sub_agents/${said}`)
}
