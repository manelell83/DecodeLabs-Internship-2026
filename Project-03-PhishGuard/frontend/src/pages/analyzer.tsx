import { useState } from "react"
import { toast } from "sonner"
import { EmailForm, type EmailFormValues } from "@/components/analyzer/email-form"
import { ScanResult } from "@/components/analyzer/scan-result"
import { scansService } from "@/services/scans"
import type { ScanDetail } from "@/types/api"

export function AnalyzerPage() {
  const [result, setResult] = useState<ScanDetail | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (values: EmailFormValues) => {
    setSubmitting(true)
    setResult(null)
    try {
      const scan = await scansService.create({
        raw_content: values.raw_content,
        sender: values.sender || undefined,
        subject: values.subject || undefined,
      })
      setResult(scan)
      toast.success(`Analysis complete — ${scan.risk_level} risk (${scan.risk_score}/100)`)
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to analyze email.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Email Analyzer</h2>
        <p className="text-sm text-muted-foreground">
          Paste a suspicious email below to scan it for phishing indicators.
        </p>
      </div>

      <EmailForm onSubmit={handleSubmit} submitting={submitting} />

      {result && <ScanResult scan={result} />}
    </div>
  )
}
