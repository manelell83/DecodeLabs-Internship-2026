import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold",
  {
    variants: {
      variant: {
        default: "border-border bg-muted text-foreground",
        critical: "border-critical/30 bg-critical/10 text-critical",
        high: "border-high/30 bg-high/10 text-high",
        medium: "border-medium/30 bg-medium/10 text-medium",
        low: "border-low/30 bg-low/10 text-low",
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

export function riskVariant(level: string): BadgeProps["variant"] {
  switch (level) {
    case "Critical":
      return "critical"
    case "High":
      return "high"
    case "Medium":
      return "medium"
    case "Low":
      return "low"
    default:
      return "default"
  }
}
