import { Menu, ShieldCheck } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/layout/theme-toggle"

interface TopbarProps {
  title: string
  onMenuClick: () => void
}

export function Topbar({ title, onMenuClick }: TopbarProps) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-border bg-card/60 px-4 md:px-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="md:hidden" onClick={onMenuClick} aria-label="Open menu">
          <Menu className="h-5 w-5" />
        </Button>
        <div className="flex items-center gap-2 md:hidden">
          <ShieldCheck className="h-5 w-5 text-primary" />
          <span className="text-sm font-bold">PhishGuard</span>
        </div>
        <h1 className="hidden text-lg font-semibold tracking-tight md:block">{title}</h1>
      </div>
      <ThemeToggle />
    </header>
  )
}
