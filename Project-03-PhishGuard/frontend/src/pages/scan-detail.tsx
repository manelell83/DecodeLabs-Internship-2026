import { useCallback } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { ArrowLeft, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { ScanResult } from "@/components/analyzer/scan-result"
import { useAsync } from "@/hooks/use-async"
import { scansService } from "@/services/scans"

export function ScanDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const scanId = Number(id)

  const fetchScan = useCallback(() => scansService.get(scanId), [scanId])
  const { data: scan, loading, error } = useAsync(fetchScan, [scanId])

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-4">
      <Button variant="ghost" size="sm" className="w-fit gap-1.5" onClick={() => navigate("/history")}>
        <ArrowLeft className="h-4 w-4" /> Back to history
      </Button>

      {loading && <Skeleton className="h-96" />}

      {error && (
        <EmptyState
          icon={AlertCircle}
          title="Scan not found"
          description="This scan may have been deleted."
          action={
            <Link to="/history">
              <Button className="mt-2">Return to History</Button>
            </Link>
          }
        />
      )}

      {scan && <ScanResult scan={scan} />}
    </div>
  )
}
