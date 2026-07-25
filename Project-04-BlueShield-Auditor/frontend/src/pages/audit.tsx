import { useState } from "react"
import { toast } from "sonner"
import { AuditTrigger } from "@/components/audit/audit-trigger"
import { AuditResult } from "@/components/audit/audit-result"
import { auditsService } from "@/services/audits"
import type { AuditDetail, AuditMode } from "@/types/api"

export function AuditPage() {
  const [result, setResult] = useState<AuditDetail | null>(null)
  const [running, setRunning] = useState(false)

  const handleRun = async (mode: AuditMode) => {
    setRunning(true)
    setResult(null)
    try {
      const audit = await auditsService.create({ mode })
      setResult(audit)
      toast.success(`Audit complete — ${audit.level} (${audit.score}/100)`)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to run audit.")
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight">System Audit</h2>
        <p className="text-sm text-muted-foreground">
          Run a security audit against this workstation, or a demo audit with simulated data.
        </p>
      </div>

      <AuditTrigger onRun={handleRun} running={running} />

      {result && <AuditResult audit={result} />}
    </div>
  )
}
