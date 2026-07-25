export type AuditLevel = "Excellent" | "Good" | "Fair" | "Poor"
export type AuditMode = "real" | "demo"
export type FindingStatus = "pass" | "warning" | "fail" | "info" | "unavailable"
export type FindingSeverity = "Info" | "Low" | "Medium" | "High" | "Critical"
export type FindingSource = "real" | "simulated"

export interface Finding {
  id: number
  category: string
  status: FindingStatus
  severity: FindingSeverity
  description: string
  evidence: string
  recommendation: string
  weight: number
  source: FindingSource
}

export interface AuditSummary {
  id: number
  created_at: string
  mode: AuditMode
  hostname: string | null
  os_summary: string | null
  score: number
  level: AuditLevel
}

export interface AuditDetail extends AuditSummary {
  summary: string
  findings: Finding[]
}

export interface AuditListResponse {
  total: number
  page: number
  page_size: number
  items: AuditSummary[]
}

export interface AuditCreatePayload {
  mode: AuditMode
}

export interface LevelCount {
  level: string
  count: number
}

export interface CategoryFailureCount {
  category: string
  count: number
}

export interface TrendPoint {
  date: string
  audit_count: number
  average_score: number
}

export interface StatsResponse {
  total_audits: number
  average_score: number
  latest_score: number | null
  level_breakdown: LevelCount[]
  top_failing_categories: CategoryFailureCount[]
  trend: TrendPoint[]
}
