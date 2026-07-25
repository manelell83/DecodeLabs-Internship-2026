import { useState } from "react"
import { toast } from "sonner"
import { Copy, FileJson, FileText, AlertTriangle, CheckCircle2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge, riskVariant } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ScoreGauge } from "@/components/ui/score-gauge"
import { HighlightedContent } from "@/components/analyzer/highlighted-content"
import { scansService } from "@/services/scans"
import { formatDate, triggerDownload } from "@/lib/utils"
import type { ScanDetail } from "@/types/api"

interface ScanResultProps {
  scan: ScanDetail
}

export function ScanResult({ scan }: ScanResultProps) {
  const [downloadingPdf, setDownloadingPdf] = useState(false)

  const handleCopy = async () => {
    const text = [
      `PhishGuard Scan #${scan.id}`,
      `Risk: ${scan.risk_level} (${scan.risk_score}/100)`,
      `Summary: ${scan.summary}`,
      "",
      "Indicators:",
      ...scan.indicators.map((i) => `- [${i.severity}] ${i.category}: ${i.description}`),
      "",
      "Recommendations:",
      ...scan.recommendations.map((r) => `- ${r}`),
    ].join("\n")

    await navigator.clipboard.writeText(text)
    toast.success("Report copied to clipboard")
  }

  const handleDownloadJson = async () => {
    const report = await scansService.getJsonReport(scan.id)
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" })
    triggerDownload(blob, `phishguard_scan_${scan.id}.json`)
    toast.success("JSON report downloaded")
  }

  const handleDownloadPdf = async () => {
    setDownloadingPdf(true)
    try {
      const blob = await scansService.getPdfBlob(scan.id)
      triggerDownload(blob, `phishguard_scan_${scan.id}.pdf`)
      toast.success("PDF report downloaded")
    } finally {
      setDownloadingPdf(false)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <Card className="animate-fade-up">
        <CardContent className="flex flex-col items-center gap-6 p-6 sm:flex-row sm:items-start">
          <ScoreGauge score={scan.risk_score} level={scan.risk_level} />
          <div className="flex-1 text-center sm:text-left">
            <div className="mb-2 flex flex-wrap items-center justify-center gap-2 sm:justify-start">
              <Badge variant={riskVariant(scan.risk_level)}>{scan.risk_level} Risk</Badge>
              <span className="text-xs text-muted-foreground">{formatDate(scan.created_at)}</span>
            </div>
            <p className="text-sm text-muted-foreground">{scan.summary}</p>
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

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Suspicious Content Highlighted</CardTitle>
          </CardHeader>
          <CardContent className="max-h-96 overflow-y-auto rounded-lg bg-muted/50 p-4">
            <HighlightedContent content={scan.raw_content} indicators={scan.indicators} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>
              Indicators ({scan.indicators.length}) &amp; Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent className="flex max-h-96 flex-col gap-4 overflow-y-auto">
            {scan.indicators.length === 0 ? (
              <div className="flex items-center gap-2 rounded-lg bg-low/10 p-3 text-sm text-low">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                No suspicious indicators detected.
              </div>
            ) : (
              <ul className="flex flex-col gap-2">
                {scan.indicators.map((indicator) => (
                  <li
                    key={indicator.id}
                    className="flex items-start gap-2 rounded-lg border border-border p-3"
                  >
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-high" />
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium">
                          {indicator.category.replaceAll("_", " ")}
                        </span>
                        <Badge variant={riskVariant(indicator.severity)} className="text-[10px]">
                          {indicator.severity}
                        </Badge>
                      </div>
                      <p className="text-xs text-muted-foreground">{indicator.description}</p>
                      <p className="mt-1 font-mono text-[11px] text-foreground/70">
                        "{indicator.evidence}"
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            )}

            <div>
              <h4 className="mb-2 text-xs font-semibold text-muted-foreground">
                Recommendations
              </h4>
              <ul className="flex flex-col gap-1.5">
                {scan.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex gap-2 text-sm">
                    <span className="text-primary">•</span> {rec}
                  </li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
