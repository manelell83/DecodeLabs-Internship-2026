import { Link } from "react-router-dom"
import { ShieldCheck, ScanLine, BarChart3, FileText, ArrowRight, MonitorCog } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ThemeToggle } from "@/components/layout/theme-toggle"

const FEATURES = [
  {
    icon: MonitorCog,
    title: "Real Workstation Audits",
    description:
      "Inspects password policy, accounts, Defender, firewall, updates, and BitLocker on the actual machine.",
  },
  {
    icon: ScanLine,
    title: "Honest Fallbacks",
    description:
      "Checks that need elevation gracefully fall back to labeled simulated data — never a silent lie.",
  },
  {
    icon: BarChart3,
    title: "Composite Security Score",
    description: "A single 0–100 posture score, fully traceable to the specific findings behind it.",
  },
  {
    icon: FileText,
    title: "Exportable Reports",
    description: "Generate professional JSON and PDF audit reports, ready to share with your team.",
  },
]

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <span className="text-lg font-bold tracking-tight">BlueShield Auditor</span>
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Link to="/dashboard">
            <Button>Open Console</Button>
          </Link>
        </div>
      </header>

      <section className="enterprise-grid-bg relative mx-auto max-w-6xl px-6 py-24 text-center">
        <span className="mb-4 inline-block rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
          DecodeLabs Cybersecurity Internship — Project 04
        </span>
        <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight md:text-6xl">
          Enterprise-grade security audits for your{" "}
          <span className="text-primary">own workstation</span>
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-muted-foreground md:text-lg">
          Evaluate password policy, accounts, Defender, firewall, updates, and encryption in one
          click — with a clear security score and actionable recommendations.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link to="/audit">
            <Button size="lg" className="gap-2">
              Run an Audit <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <Link to="/dashboard">
            <Button size="lg" variant="outline">
              View Dashboard
            </Button>
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <Card key={title} className="animate-fade-up">
              <CardHeader>
                <div className="mb-2 flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Icon className="h-5 w-5" />
                </div>
                <CardTitle className="text-foreground">{title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">{description}</CardContent>
            </Card>
          ))}
        </div>
      </section>

      <footer className="border-t border-border py-8 text-center text-xs text-muted-foreground">
        Built for the DecodeLabs Cybersecurity Internship 2026 — Project 04: BlueShield Auditor
      </footer>
    </div>
  )
}
