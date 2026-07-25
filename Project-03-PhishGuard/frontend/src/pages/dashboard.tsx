import { useCallback } from "react"
import { Link } from "react-router-dom"
import { ScanSearch, ShieldAlert, Gauge, Inbox } from "lucide-react"
import { StatCard } from "@/components/dashboard/stat-card"
import { TrendChart } from "@/components/dashboard/trend-chart"
import { CategoryChart } from "@/components/dashboard/category-chart"
import { ScanTable } from "@/components/scans/scan-table"
import { EmptyState } from "@/components/ui/empty-state"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"
import { useAsync } from "@/hooks/use-async"
import { statsService } from "@/services/stats"
import { scansService } from "@/services/scans"

export function DashboardPage() {
  const statsFetch = useCallback(() => statsService.get(), [])
  const recentFetch = useCallback(() => scansService.list({ page: 1, page_size: 5 }), [])

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

  if (!stats || stats.total_scans === 0) {
    return (
      <EmptyState
        icon={Inbox}
        title="No scans yet"
        description="Analyze your first email to start populating your SOC dashboard."
        action={
          <Link to="/analyzer">
            <Button className="mt-2">Analyze an Email</Button>
          </Link>
        }
      />
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard icon={ScanSearch} label="Total Scans" value={stats.total_scans} tone="primary" />
        <StatCard
          icon={ShieldAlert}
          label="High/Critical Risk"
          value={stats.high_risk_count}
          tone="critical"
        />
        <StatCard icon={Gauge} label="Average Score" value={stats.average_score} />
        <StatCard
          icon={Inbox}
          label="Risk Levels Tracked"
          value={stats.risk_level_breakdown.length}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <TrendChart data={stats.trend} />
        <CategoryChart data={stats.top_categories} />
      </div>

      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold">Recent Scans</h3>
          <Link to="/history" className="text-xs font-medium text-primary hover:underline">
            View all
          </Link>
        </div>
        {recentLoading ? (
          <Skeleton className="h-48" />
        ) : (
          recent && <ScanTable scans={recent.items} />
        )}
      </div>
    </div>
  )
}
