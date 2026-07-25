import { useState } from "react"
import { toast } from "sonner"
import { Copy, FileJson, FileText, AlertTriangle, CheckCircle2, Info } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge, levelVariant, severityVariant } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ScoreGauge } from "@/components/ui/score-gauge"
import { auditsService } from "@/services/audits"
import { formatDate, triggerDownload } from "@/lib/utils"
import type { AuditDetail, Finding } from "@/types/api"

interface AuditResultProps {
  audit: AuditDetail
}

const STATUS_ICON: Record<string, typeof AlertTriangle> = {
  fail: AlertTriangle,
  warning: AlertTriangle,
  pass: CheckCircle2,
  info: Info,
  unavailable: Info,
}

function sortFindings(findings: Finding[]): Finding[] {
  const priority: Record<string, number> = { fail: 0, warning: 1, unavailable: 2, pass: 3, info: 4 }
  return [...findings].sort((a, b) => (priority[a.status] ?? 5) - (priority[b.status] ?? 5))
}

export function AuditResult({ audit }: AuditResultProps) {
  const [downloadingPdf, setDownloadingPdf] = useState(false)
  const findings = sortFindings(audit.findings)

  const handleCopy = async () => {
    const text = [
      `BlueShield Audit #${audit.id}`,
      `Score: ${audit.level} (${audit.score}/100)`,
      `Host: ${audit.hostname} — ${audit.os_summary}`,
      `Summary: ${audit.summary}`,
      "",
      "Findings:",
      ...findings.map((f) => `- [${f.status.toUpperCase()}] ${f.category}: ${f.description}`),
    ].join("\n")

    await navigator.clipboard.writeText(text)
    toast.success("Audit summary copied to clipboard")
  }

  const handleDownloadJson = async () => {
    const report = await auditsService.getJsonReport(audit.id)
    triggerDownload(
      new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
      `blueshield_audit_${audit.id}.json`,
    )
    toast.success("JSON report downloaded")
  }

  const handleDownloadPdf = async () => {
    setDownloadingPdf(true)
    try {
      const blob = await auditsService.getPdfBlob(audit.id)
      triggerDownload(blob, `blueshield_audit_${audit.id}.pdf`)
      toast.success("PDF report downloaded")
    } finally {
      setDownloadingPdf(false)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <Card className="animate-fade-up">
        <CardContent className="flex flex-col items-center gap-6 p-6 sm:flex-row sm:items-start">
          <ScoreGauge score={audit.score} level={audit.level} />
          <div className="flex-1 text-center sm:text-left">
            <div className="mb-2 flex flex-wrap items-center justify-center gap-2 sm:justify-start">
              <Badge variant={levelVariant(audit.level)}>{audit.level}</Badge>
              <Badge variant="outline" className="capitalize">{audit.mode} mode</Badge>
              <span className="text-xs text-muted-foreground">{formatDate(audit.created_at)}</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {audit.hostname} — {audit.os_summary}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">{audit.summary}</p>
            <div className="mt-3 flex flex-wrap justify-center gap-2 sm:justify-start">
              <Button variant="outline" size="sm" className="gap-1.5" onClick={handleCopy}>
                <Copy className="h-3.5 w-3.5" /> Copy
              </Button>
              <Button variant="outline" size="sm" className="gap-1.5" onClick={handleDownloadJson}>
                <FileJson className="h-3.5 w-3.5" /> JSON
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5"
                onClick={handleDownloadPdf}
                disabled={downloadingPdf}
              >
                <FileText className="h-3.5 w-3.5" /> {downloadingPdf ? "Generating..." : "PDF"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Findings ({findings.length})</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-2">
          {findings.map((finding) => {
            const Icon = STATUS_ICON[finding.status] ?? Info
            return (
              <div key={finding.id} className="flex items-start gap-3 rounded-lg border border-border p-3">
                <Icon
                  className={`mt-0.5 h-4 w-4 shrink-0 ${
                    finding.status === "fail" || finding.status === "warning"
                      ? "text-poor"
                      : finding.status === "pass"
                        ? "text-excellent"
                        : "text-muted-foreground"
                  }`}
                />
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-sm font-medium">{finding.category.replaceAll("_", " ")}</span>
                    <Badge variant={severityVariant(finding.severity)} className="text-[10px]">
                      {finding.severity}
                    </Badge>
                    <Badge variant="outline" className="text-[10px] capitalize">
                      {finding.source}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{finding.description}</p>
                  <p className="mt-1 font-mono text-[11px] text-foreground/70">{finding.evidence}</p>
                  {finding.recommendation && finding.recommendation !== "No action needed." && (
                    <p className="mt-1 text-xs text-primary">→ {finding.recommendation}</p>
                  )}
                </div>
              </div>
            )
          })}
        </CardContent>
      </Card>
    </div>
  )
}
