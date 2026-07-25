import { useState } from "react"
import { Loader2, ScanLine, MonitorCog, PlayCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { AuditMode } from "@/types/api"

interface AuditTriggerProps {
  onRun: (mode: AuditMode) => void
  running: boolean
}

const MODES: { value: AuditMode; label: string; description: string; icon: typeof MonitorCog }[] = [
  {
    value: "real",
    label: "Real Audit",
    description: "Inspects this actual workstation. Checks that need admin rights fall back to simulated data automatically.",
    icon: MonitorCog,
  },
  {
    value: "demo",
    label: "Demo Audit",
    description: "Runs entirely on realistic simulated data — useful for demos on any machine.",
    icon: PlayCircle,
  },
]

export function AuditTrigger({ onRun, running }: AuditTriggerProps) {
  const [mode, setMode] = useState<AuditMode>("real")

  return (
    <Card>
      <CardContent className="flex flex-col gap-4 p-5">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {MODES.map(({ value, label, description, icon: Icon }) => (
            <button
              key={value}
              onClick={() => setMode(value)}
              className={cn(
                "flex flex-col items-start gap-2 rounded-lg border p-4 text-left transition-colors cursor-pointer",
                mode === value ? "border-primary bg-primary/5" : "border-border hover:bg-muted",
              )}
            >
              <div className="flex items-center gap-2">
                <Icon className={cn("h-4 w-4", mode === value ? "text-primary" : "text-muted-foreground")} />
                <span className="text-sm font-semibold">{label}</span>
              </div>
              <p className="text-xs text-muted-foreground">{description}</p>
            </button>
          ))}
        </div>

        <Button onClick={() => onRun(mode)} disabled={running} className="w-fit gap-2">
          {running ? <Loader2 className="h-4 w-4 animate-spin" /> : <ScanLine className="h-4 w-4" />}
          {running ? "Auditing system..." : `Run ${mode === "real" ? "Real" : "Demo"} Audit`}
        </Button>
      </CardContent>
    </Card>
  )
}
