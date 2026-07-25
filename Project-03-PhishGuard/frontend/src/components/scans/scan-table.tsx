import { Link } from "react-router-dom"
import { Trash2, Eye } from "lucide-react"
import { Badge, riskVariant } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/lib/utils"
import type { ScanSummary } from "@/types/api"

interface ScanTableProps {
  scans: ScanSummary[]
  onDelete?: (id: number) => void
}

export function ScanTable({ scans, onDelete }: ScanTableProps) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="w-full min-w-[640px] text-sm">
        <thead>
          <tr className="border-b border-border bg-muted/50 text-left text-xs text-muted-foreground">
            <th className="px-4 py-3 font-medium">Sender / Subject</th>
            <th className="px-4 py-3 font-medium">Date</th>
            <th className="px-4 py-3 font-medium">URLs</th>
            <th className="px-4 py-3 font-medium">Risk</th>
            <th className="px-4 py-3 font-medium text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan) => (
            <tr key={scan.id} className="border-b border-border last:border-0 hover:bg-muted/30">
              <td className="px-4 py-3">
                <p className="font-medium">{scan.subject || "(no subject)"}</p>
                <p className="text-xs text-muted-foreground">{scan.sender || "Unknown sender"}</p>
              </td>
              <td className="px-4 py-3 text-xs text-muted-foreground">
                {formatDate(scan.created_at)}
              </td>
              <td className="px-4 py-3 text-xs text-muted-foreground">{scan.urls_found}</td>
              <td className="px-4 py-3">
                <Badge variant={riskVariant(scan.risk_level)}>
                  {scan.risk_level} · {scan.risk_score}
                </Badge>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center justify-end gap-1">
                  <Link to={`/history/${scan.id}`}>
                    <Button variant="ghost" size="icon" aria-label="View scan">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </Link>
                  {onDelete && (
                    <Button
                      variant="ghost"
                      size="icon"
                      aria-label="Delete scan"
                      onClick={() => onDelete(scan.id)}
                    >
                      <Trash2 className="h-4 w-4 text-critical" />
                    </Button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
