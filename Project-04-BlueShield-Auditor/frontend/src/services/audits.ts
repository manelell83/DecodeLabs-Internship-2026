import { apiClient } from "@/services/api"
import type { AuditCreatePayload, AuditDetail, AuditListResponse } from "@/types/api"

export interface ListAuditsParams {
  page?: number
  page_size?: number
  level?: string
}

export const auditsService = {
  async create(payload: AuditCreatePayload): Promise<AuditDetail> {
    const { data } = await apiClient.post<AuditDetail>("/audits", payload)
    return data
  },

  async list(params: ListAuditsParams = {}): Promise<AuditListResponse> {
    const { data } = await apiClient.get<AuditListResponse>("/audits", { params })
    return data
  },

  async get(id: number): Promise<AuditDetail> {
    const { data } = await apiClient.get<AuditDetail>(`/audits/${id}`)
    return data
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/audits/${id}`)
  },

  async getJsonReport(id: number): Promise<Record<string, unknown>> {
    const { data } = await apiClient.get(`/audits/${id}/report`, { params: { format: "json" } })
    return data
  },

  async getPdfBlob(id: number): Promise<Blob> {
    const { data } = await apiClient.get(`/audits/${id}/report`, {
      params: { format: "pdf" },
      responseType: "blob",
    })
    return data
  },
}
