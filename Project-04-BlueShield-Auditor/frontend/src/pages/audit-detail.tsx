import { useCallback } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { ArrowLeft, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { AuditResult } from "@/components/audit/audit-result"
import { useAsync } from "@/hooks/use-async"
import { auditsService } from "@/services/audits"

export function AuditDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const auditId = Number(id)

  const fetchAudit = useCallback(() => auditsService.get(auditId), [auditId])
  const { data: audit, loading, error } = useAsync(fetchAudit, [auditId])

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-4">
      <Button variant="ghost" size="sm" className="w-fit gap-1.5" onClick={() => navigate("/history")}>
        <ArrowLeft className="h-4 w-4" /> Back to history
      </Button>

      {loading && <Skeleton className="h-96" />}

      {error && (
        <EmptyState
          icon={AlertCircle}
          title="Audit not found"
          description="This audit may have been deleted."
          action={
            <Link to="/history">
              <Button className="mt-2">Return to History</Button>
            </Link>
          }
        />
      )}

      {audit && <AuditResult audit={audit} />}
    </div>
  )
}
