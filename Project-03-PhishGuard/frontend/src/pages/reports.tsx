import { useCallback, useState } from "react"
import { toast } from "sonner"
import { FileJson, FileText, FolderOpen } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge, riskVariant } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { useAsync } from "@/hooks/use-async"
import { scansService } from "@/services/scans"
import { formatDate, triggerDownload } from "@/lib/utils"

export function ReportsPage() {
  const fetchScans = useCallback(() => scansService.list({ page: 1, page_size: 20 }), [])
  const { data, loading } = useAsync(fetchScans, [])
  const [busyId, setBusyId] = useState<number | null>(null)

  const downloadJson = async (id: number) => {
    setBusyId(id)
    try {
      const report = await scansService.getJsonReport(id)
      triggerDownload(
        new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
        `phishguard_scan_${id}.json`,
      )
      toast.success("JSON report downloaded")
    } finally {
      setBusyId(null)
    }
  }

  const downloadPdf = async (id: number) => {
    setBusyId(id)
    try {
      const blob = await scansService.getPdfBlob(id)
      triggerDownload(blob, `phishguard_scan_${id}.pdf`)
      toast.success("PDF report downloaded")
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Reports</h2>
        <p className="text-sm text-muted-foreground">
          Generate and download JSON or PDF reports for any completed scan.
        </p>
      </div>

      {loading ? (
        <Skeleton className="h-96" />
      ) : !data || data.items.length === 0 ? (
        <EmptyState
          icon={FolderOpen}
          title="No reports available"
          description="Analyze an email first to generate downloadable reports."
        />
      ) : (
        <div className="flex flex-col gap-2">
          {data.items.map((scan) => (
            <Card key={scan.id} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-medium">{scan.subject || "(no subject)"}</p>
                <p className="text-xs text-muted-foreground">
                  {scan.sender || "Unknown sender"} · {formatDate(scan.created_at)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={riskVariant(scan.risk_level)}>{scan.risk_level}</Badge>
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-1.5"
                  disabled={busyId === scan.id}
                  onClick={() => downloadJson(scan.id)}
                >
                  <FileJson className="h-3.5 w-3.5" /> JSON
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-1.5"
                  disabled={busyId === scan.id}
                  onClick={() => downloadPdf(scan.id)}
                >
                  <FileText className="h-3.5 w-3.5" /> PDF
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
