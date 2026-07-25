import { useCallback } from "react"
import { BarChart3 } from "lucide-react"
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { TrendChart } from "@/components/dashboard/trend-chart"
import { CategoryChart } from "@/components/dashboard/category-chart"
import { useAsync } from "@/hooks/use-async"
import { statsService } from "@/services/stats"

const LEVEL_COLORS: Record<string, string> = {
  Excellent: "var(--color-excellent)",
  Good: "var(--color-good)",
  Fair: "var(--color-fair)",
  Poor: "var(--color-poor)",
}

export function StatisticsPage() {
  const fetchStats = useCallback(() => statsService.get(), [])
  const { data: stats, loading } = useAsync(fetchStats, [])

  if (loading) return <Skeleton className="h-96" />

  if (!stats || stats.total_audits === 0) {
    return (
      <EmptyState
        icon={BarChart3}
        title="No statistics yet"
        description="Statistics will appear here once you've run at least one audit."
      />
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Statistics</h2>
        <p className="text-sm text-muted-foreground">
          Aggregate insight across all {stats.total_audits} audits performed.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <TrendChart data={stats.trend} />

        <Card>
          <CardHeader>
            <CardTitle>Security Level Distribution</CardTitle>
          </CardHeader>
          <CardContent className="h-64 pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.level_breakdown}
                  dataKey="count"
                  nameKey="level"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={2}
                >
                  {stats.level_breakdown.map((entry) => (
                    <Cell key={entry.level} fill={LEVEL_COLORS[entry.level] ?? "var(--color-primary)"} />
                  ))}
                </Pie>
                <Legend verticalAlign="bottom" height={24} />
                <Tooltip
                  contentStyle={{
                    background: "var(--color-card)",
                    border: "1px solid var(--color-border)",
                    borderRadius: 8,
                    fontSize: 12,
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <CategoryChart data={stats.top_failing_categories} />
    </div>
  )
}
