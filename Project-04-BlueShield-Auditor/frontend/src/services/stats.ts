import { apiClient } from "@/services/api"
import type { StatsResponse } from "@/types/api"

export const statsService = {
  async get(): Promise<StatsResponse> {
    const { data } = await apiClient.get<StatsResponse>("/stats")
    return data
  },
}
