import { Link } from "react-router-dom"
import { Trash2, Eye } from "lucide-react"
import { Badge, levelVariant } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/lib/utils"
import type { AuditSummary } from "@/types/api"

interface AuditTableProps {
  audits: AuditSummary[]
  onDelete?: (id: number) => void
}

export function AuditTable({ audits, onDelete }: AuditTableProps) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="w-full min-w-[640px] text-sm">
        <thead>
          <tr className="border-b border-border bg-muted/50 text-left text-xs text-muted-foreground">
            <th className="px-4 py-3 font-medium">Hostname / OS</th>
            <th className="px-4 py-3 font-medium">Date</th>
            <th className="px-4 py-3 font-medium">Mode</th>
            <th className="px-4 py-3 font-medium">Score</th>
            <th className="px-4 py-3 font-medium text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {audits.map((audit) => (
            <tr key={audit.id} className="border-b border-border last:border-0 hover:bg-muted/30">
              <td className="px-4 py-3">
                <p className="font-medium">{audit.hostname || "Unknown host"}</p>
                <p className="text-xs text-muted-foreground">{audit.os_summary || "Unknown OS"}</p>
              </td>
              <td className="px-4 py-3 text-xs text-muted-foreground">{formatDate(audit.created_at)}</td>
              <td className="px-4 py-3 text-xs text-muted-foreground capitalize">{audit.mode}</td>
              <td className="px-4 py-3">
                <Badge variant={levelVariant(audit.level)}>
                  {audit.level} · {audit.score}
                </Badge>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center justify-end gap-1">
                  <Link to={`/history/${audit.id}`}>
                    <Button variant="ghost" size="icon" aria-label="View audit">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </Link>
                  {onDelete && (
                    <Button
                      variant="ghost"
                      size="icon"
                      aria-label="Delete audit"
                      onClick={() => onDelete(audit.id)}
                    >
                      <Trash2 className="h-4 w-4 text-poor" />
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
