import type { LucideIcon } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardValue } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface StatCardProps {
  icon: LucideIcon
  label: string
  value: string | number
  tone?: "default" | "poor" | "primary"
  hint?: string
}

export function StatCard({ icon: Icon, label, value, tone = "default", hint }: StatCardProps) {
  return (
    <Card className="animate-fade-up">
      <CardHeader className="flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle>{label}</CardTitle>
        <div
          className={cn(
            "flex h-8 w-8 items-center justify-center rounded-lg",
            tone === "poor" && "bg-poor/10 text-poor",
            tone === "primary" && "bg-primary/10 text-primary",
            tone === "default" && "bg-muted text-muted-foreground",
          )}
        >
          <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent>
        <CardValue>{value}</CardValue>
        {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
      </CardContent>
    </Card>
  )
}
