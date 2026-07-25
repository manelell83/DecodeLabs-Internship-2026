import { apiClient } from "@/services/api"
import type { ScanCreatePayload, ScanDetail, ScanListResponse } from "@/types/api"

export interface ListScansParams {
  page?: number
  page_size?: number
  search?: string
  risk_level?: string
}

export const scansService = {
  async create(payload: ScanCreatePayload): Promise<ScanDetail> {
    const { data } = await apiClient.post<ScanDetail>("/scans", payload)
    return data
  },

  async list(params: ListScansParams = {}): Promise<ScanListResponse> {
    const { data } = await apiClient.get<ScanListResponse>("/scans", { params })
    return data
  },

  async get(id: number): Promise<ScanDetail> {
    const { data } = await apiClient.get<ScanDetail>(`/scans/${id}`)
    return data
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(`/scans/${id}`)
  },

  reportUrl(id: number, format: "json" | "pdf"): string {
    return `${apiClient.defaults.baseURL}/scans/${id}/report?format=${format}`
  },

  async getJsonReport(id: number): Promise<Record<string, unknown>> {
    const { data } = await apiClient.get(`/scans/${id}/report`, { params: { format: "json" } })
    return data
  },

  async getPdfBlob(id: number): Promise<Blob> {
    const { data } = await apiClient.get(`/scans/${id}/report`, {
      params: { format: "pdf" },
      responseType: "blob",
    })
    return data
  },
}
