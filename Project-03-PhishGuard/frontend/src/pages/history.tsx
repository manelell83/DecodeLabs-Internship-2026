import { useCallback, useState } from "react"
import { Search, Inbox, ChevronLeft, ChevronRight } from "lucide-react"
import { toast } from "sonner"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { ScanTable } from "@/components/scans/scan-table"
import { useAsync } from "@/hooks/use-async"
import { scansService } from "@/services/scans"

const RISK_LEVELS = ["", "Low", "Medium", "High", "Critical"]
const PAGE_SIZE = 10

export function HistoryPage() {
  const [search, setSearch] = useState("")
  const [riskLevel, setRiskLevel] = useState("")
  const [page, setPage] = useState(1)

  const fetchScans = useCallback(
    () =>
      scansService.list({
        page,
        page_size: PAGE_SIZE,
        search: search || undefined,
        risk_level: riskLevel || undefined,
      }),
    [page, search, riskLevel],
  )

  const { data, loading, refetch } = useAsync(fetchScans, [page, search, riskLevel])

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this scan permanently?")) return
    await scansService.remove(id)
    toast.success("Scan deleted")
    refetch()
  }

  const totalPages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Scan History</h2>
        <p className="text-sm text-muted-foreground">
          Search, filter, and review every email PhishGuard has analyzed.
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by sender or subject..."
            className="pl-9"
            value={search}
            onChange={(e) => {
              setPage(1)
              setSearch(e.target.value)
            }}
          />
        </div>
        <select
          className="h-10 rounded-lg border border-border bg-card px-3 text-sm"
          value={riskLevel}
          onChange={(e) => {
            setPage(1)
            setRiskLevel(e.target.value)
          }}
        >
          {RISK_LEVELS.map((level) => (
            <option key={level} value={level}>
              {level || "All risk levels"}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <Skeleton className="h-96" />
      ) : !data || data.items.length === 0 ? (
        <EmptyState
          icon={Inbox}
          title="No matching scans"
          description="Try a different search term or clear your filters."
        />
      ) : (
        <>
          <ScanTable scans={data.items} onDelete={handleDelete} />
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              Page {page} of {totalPages} — {data.total} total scans
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
