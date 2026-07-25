import { useCallback, useMemo, useState } from "react"
import { Search, Inbox, ChevronLeft, ChevronRight } from "lucide-react"
import { toast } from "sonner"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { AuditTable } from "@/components/audit/audit-table"
import { useAsync } from "@/hooks/use-async"
import { auditsService } from "@/services/audits"

const LEVELS = ["", "Excellent", "Good", "Fair", "Poor"]
const PAGE_SIZE = 10

export function HistoryPage() {
  const [search, setSearch] = useState("")
  const [level, setLevel] = useState("")
  const [page, setPage] = useState(1)

  const fetchAudits = useCallback(
    () => auditsService.list({ page, page_size: PAGE_SIZE, level: level || undefined }),
    [page, level],
  )

  const { data, loading, refetch } = useAsync(fetchAudits, [page, level])

  const filteredItems = useMemo(() => {
    if (!data) return []
    if (!search.trim()) return data.items
    const term = search.trim().toLowerCase()
    return data.items.filter(
      (a) =>
        (a.hostname || "").toLowerCase().includes(term) ||
        (a.os_summary || "").toLowerCase().includes(term),
    )
  }, [data, search])

  const handleDelete = async (id: number) => {
    if (!window.confirm("Delete this audit permanently?")) return
    await auditsService.remove(id)
    toast.success("Audit deleted")
    refetch()
  }

  const totalPages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1

  return (
    <div className="flex flex-col gap-4">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Audit History</h2>
        <p className="text-sm text-muted-foreground">
          Search, filter, and review every audit run.
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by hostname or OS..."
            className="pl-9"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <select
          className="h-10 rounded-lg border border-border bg-card px-3 text-sm"
          value={level}
          onChange={(e) => {
            setPage(1)
            setLevel(e.target.value)
          }}
        >
          {LEVELS.map((l) => (
            <option key={l} value={l}>
              {l || "All levels"}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <Skeleton className="h-96" />
      ) : !data || filteredItems.length === 0 ? (
        <EmptyState
          icon={Inbox}
          title="No matching audits"
          description="Try a different search term or clear your filters."
        />
      ) : (
        <>
          <AuditTable audits={filteredItems} onDelete={handleDelete} />
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              Page {page} of {totalPages} — {data.total} total audits
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
