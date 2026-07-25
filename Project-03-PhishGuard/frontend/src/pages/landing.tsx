import { Link } from "react-router-dom"
import { ShieldCheck, ScanSearch, BarChart3, FileText, ArrowRight, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ThemeToggle } from "@/components/layout/theme-toggle"

const FEATURES = [
  {
    icon: Mail,
    title: "Deep Email Analysis",
    description:
      "Parses headers, body, URLs, and domains to surface phishing red flags a human might miss.",
  },
  {
    icon: ScanSearch,
    title: "Multi-Vector Detection",
    description:
      "Flags IP-based links, shorteners, brand impersonation, credential theft, and scam patterns.",
  },
  {
    icon: BarChart3,
    title: "Explainable Risk Scoring",
    description: "Every score traces back to specific, weighted indicators — never a black box.",
  },
  {
    icon: FileText,
    title: "Exportable Reports",
    description: "Generate professional JSON and PDF reports for every scan, ready to share.",
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
          <span className="text-lg font-bold tracking-tight">PhishGuard</span>
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Link to="/dashboard">
            <Button>Open Console</Button>
          </Link>
        </div>
      </header>

      <section className="security-grid-bg relative mx-auto max-w-6xl px-6 py-24 text-center">
        <span className="mb-4 inline-block rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
          DecodeLabs Cybersecurity Internship — Project 03
        </span>
        <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight md:text-6xl">
          Phishing analysis for your{" "}
          <span className="text-primary">Blue Team</span>
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-muted-foreground md:text-lg">
          Paste a suspicious email and get an instant, explainable risk score — with every
          indicator, recommendation, and report a SOC analyst needs.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link to="/analyzer">
            <Button size="lg" className="gap-2">
              Analyze an Email <ArrowRight className="h-4 w-4" />
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
        Built for the DecodeLabs Cybersecurity Internship 2026 — Project 03: PhishGuard
      </footer>
    </div>
  )
}
