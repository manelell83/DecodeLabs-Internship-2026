export type RiskLevel = "Low" | "Medium" | "High" | "Critical"

export interface Indicator {
  id: number
  category: string
  description: string
  evidence: string
  severity: RiskLevel
  weight: number
}

export interface ScanSummary {
  id: number
  created_at: string
  sender: string | null
  subject: string | null
  risk_score: number
  risk_level: RiskLevel
  urls_found: number
  domains_found: number
}

export interface ScanDetail extends ScanSummary {
  raw_content: string
  summary: string
  indicators: Indicator[]
  recommendations: string[]
}

export interface ScanListResponse {
  total: number
  page: number
  page_size: number
  items: ScanSummary[]
}

export interface ScanCreatePayload {
  raw_content: string
  sender?: string
  subject?: string
}

export interface RiskLevelCount {
  risk_level: string
  count: number
}

export interface CategoryCount {
  category: string
  count: number
}

export interface TrendPoint {
  date: string
  scan_count: number
  average_score: number
}

export interface StatsResponse {
  total_scans: number
  average_score: number
  high_risk_count: number
  risk_level_breakdown: RiskLevelCount[]
  top_categories: CategoryCount[]
  trend: TrendPoint[]
}
