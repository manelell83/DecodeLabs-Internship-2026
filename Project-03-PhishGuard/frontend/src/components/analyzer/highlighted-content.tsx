import { Fragment } from "react"
import type { ReactNode } from "react"
import type { Indicator } from "@/types/api"

interface HighlightedContentProps {
  content: string
  indicators: Indicator[]
}

interface Range {
  start: number
  end: number
  severity: string
}

function findRanges(content: string, indicators: Indicator[]): Range[] {
  const lowerContent = content.toLowerCase()
  const ranges: Range[] = []

  for (const indicator of indicators) {
    const needle = indicator.evidence.trim().toLowerCase()
    if (!needle || needle.length < 3) continue

    let fromIndex = 0
    while (fromIndex <= lowerContent.length) {
      const idx = lowerContent.indexOf(needle, fromIndex)
      if (idx === -1) break
      ranges.push({ start: idx, end: idx + needle.length, severity: indicator.severity })
      fromIndex = idx + needle.length
    }
  }

  ranges.sort((a, b) => a.start - b.start)

  const merged: Range[] = []
  for (const range of ranges) {
    const last = merged[merged.length - 1]
    if (last && range.start <= last.end) {
      last.end = Math.max(last.end, range.end)
    } else {
      merged.push({ ...range })
    }
  }
  return merged
}

const SEVERITY_MARK_CLASS: Record<string, string> = {
  Critical: "bg-critical/20 text-critical",
  High: "bg-high/20 text-high",
  Medium: "bg-medium/20 text-medium",
  Low: "bg-low/20 text-low",
}

export function HighlightedContent({ content, indicators }: HighlightedContentProps) {
  const ranges = findRanges(content, indicators)

  if (ranges.length === 0) {
    return <pre className="whitespace-pre-wrap break-words font-mono text-sm">{content}</pre>
  }

  const segments: ReactNode[] = []
  let cursor = 0

  ranges.forEach((range, idx) => {
    if (range.start > cursor) {
      segments.push(<Fragment key={`t-${idx}`}>{content.slice(cursor, range.start)}</Fragment>)
    }
    segments.push(
      <mark
        key={`m-${idx}`}
        className={`rounded px-0.5 ${SEVERITY_MARK_CLASS[range.severity] ?? "bg-primary/20 text-primary"}`}
      >
        {content.slice(range.start, range.end)}
      </mark>,
    )
    cursor = range.end
  })

  if (cursor < content.length) {
    segments.push(<Fragment key="t-end">{content.slice(cursor)}</Fragment>)
  }

  return <pre className="whitespace-pre-wrap break-words font-mono text-sm">{segments}</pre>
}
