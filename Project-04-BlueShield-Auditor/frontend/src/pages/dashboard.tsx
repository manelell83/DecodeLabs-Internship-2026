import { useCallback } from "react"
import { Link } from "react-router-dom"
import { ScanLine, ShieldAlert, Gauge, Inbox } from "lucide-react"
import { StatCard } from "@/components/dashboard/stat-card"
import { TrendChart } from "@/components/dashboard/trend-chart"
import { CategoryChart } from "@/components/dashboard/category-chart"
import { AuditTable } from "@/components/audit/audit-table"
import { EmptyState } from "@/components/ui/empty-state"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"
import { useAsync } from "@/hooks/use-async"
import { statsService } from "@/services/stats"
import { auditsService } from "@/services/audits"

export function DashboardPage() {
  const statsFetch = useCallback(() => statsService.get(), [])
  const recentFetch = useCallback(() => auditsService.list({ page: 1, page_size: 5 }), [])

  const { data: stats, loading: statsLoading } = useAsync(statsFetch, [])
  const { data: recent, loading: recentLoading } = useAsync(recentFetch, [])

  if (statsLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-28" />
        ))}
      </div>
    )
  }

  if (!stats || stats.total_audits === 0) {
    return (
      <EmptyState
        icon={Inbox}
        title="No audits yet"
        description="Run your first workstation audit to start populating your Blue Team dashboard."
        action={
          <Link to="/audit">
            <Button className="mt-2">Run an Audit</Button>
          </Link>
        }
      />
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={ScanLine} label="Total Audits" value={stats.total_audits} tone="primary" />
        <StatCard
          icon={Gauge}
          label="Latest Score"
          value={stats.latest_score ?? "—"}
        />
        <StatCard icon={Gauge} label="Average Score" value={stats.average_score} />
        <StatCard
          icon={ShieldAlert}
          label="Failing Categories"
          value={stats.top_failing_categories.length}
          tone="poor"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <TrendChart data={stats.trend} />
        <CategoryChart data={stats.top_failing_categories} />
      </div>

      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold">Recent Audits</h3>
          <Link to="/history" className="text-xs font-medium text-primary hover:underline">
            View all
          </Link>
        </div>
        {recentLoading ? (
          <Skeleton className="h-48" />
        ) : (
          recent && <AuditTable audits={recent.items} />
        )}
      </div>
    </div>
  )
}
