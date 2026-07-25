import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold",
  {
    variants: {
      variant: {
        default: "border-border bg-muted text-foreground",
        excellent: "border-excellent/30 bg-excellent/10 text-excellent",
        good: "border-good/30 bg-good/10 text-good",
        fair: "border-fair/30 bg-fair/10 text-fair",
        poor: "border-poor/30 bg-poor/10 text-poor",
        critical: "border-critical/30 bg-critical/10 text-critical",
        high: "border-high/30 bg-high/10 text-high",
        medium: "border-medium/30 bg-medium/10 text-medium",
        low: "border-low/30 bg-low/10 text-low",
        info: "border-info/30 bg-info/10 text-info",
        outline: "border-border text-muted-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant, className }))} {...props} />
}

export function levelVariant(level: string): BadgeProps["variant"] {
  switch (level) {
    case "Excellent":
      return "excellent"
    case "Good":
      return "good"
    case "Fair":
      return "fair"
    case "Poor":
      return "poor"
    default:
      return "default"
  }
}

export function severityVariant(severity: string): BadgeProps["variant"] {
  switch (severity) {
    case "Critical":
      return "critical"
    case "High":
      return "high"
    case "Medium":
      return "medium"
    case "Low":
      return "low"
    case "Info":
      return "info"
    default:
      return "default"
  }
}
