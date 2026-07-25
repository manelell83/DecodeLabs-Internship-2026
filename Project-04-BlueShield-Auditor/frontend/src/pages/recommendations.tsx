import { useCallback } from "react"
import { Link } from "react-router-dom"
import { ClipboardCheck, AlertTriangle, ArrowRight } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge, severityVariant } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { useAsync } from "@/hooks/use-async"
import { auditsService } from "@/services/audits"
import { formatDate } from "@/lib/utils"

export function RecommendationsPage() {
  const fetchLatest = useCallback(async () => {
    const list = await auditsService.list({ page: 1, page_size: 1 })
    if (list.items.length === 0) return null
    return auditsService.get(list.items[0].id)
  }, [])

  const { data: audit, loading } = useAsync(fetchLatest, [])

  if (loading) return <Skeleton className="h-96" />

  if (!audit) {
    return (
      <EmptyState
        icon={ClipboardCheck}
        title="No recommendations yet"
        description="Run an audit first — recommendations are generated from its findings."
        action={
          <Link to="/audit">
            <Button className="mt-2">Run an Audit</Button>
          </Link>
        }
      />
    )
  }

  const actionable = audit.findings.filter(
    (f) => (f.status === "fail" || f.status === "warning") && f.recommendation,
  )

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Recommendations</h2>
        <p className="text-sm text-muted-foreground">
          Based on your most recent audit (#{audit.id}, {formatDate(audit.created_at)}).
        </p>
      </div>

      {actionable.length === 0 ? (
        <EmptyState
          icon={ClipboardCheck}
          title="No outstanding issues"
          description="Your most recent audit found nothing that needs action. Great work."
        />
      ) : (
        <div className="flex flex-col gap-3">
          {actionable.map((finding) => (
            <Card key={finding.id}>
              <CardHeader className="flex-row items-start justify-between space-y-0">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-poor" />
                  <CardTitle className="text-foreground">
                    {finding.category.replaceAll("_", " ")}
                  </CardTitle>
                </div>
                <Badge variant={severityVariant(finding.severity)}>{finding.severity}</Badge>
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                <p className="text-sm text-muted-foreground">{finding.description}</p>
                <div className="flex items-start gap-2 rounded-lg bg-primary/5 p-3 text-sm text-primary">
                  <ArrowRight className="mt-0.5 h-4 w-4 shrink-0" />
                  {finding.recommendation}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Link to={`/history/${audit.id}`} className="self-start text-xs font-medium text-primary hover:underline">
        View full audit detail →
      </Link>
    </div>
  )
}
