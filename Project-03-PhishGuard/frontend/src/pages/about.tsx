import { ShieldCheck, FolderGit2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const TECH_STACK = [
  "FastAPI", "SQLAlchemy", "SQLite", "Pydantic", "Pytest",
  "React", "TypeScript", "Vite", "TailwindCSS", "Recharts",
]

export function AboutPage() {
  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-4">
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <ShieldCheck className="h-6 w-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold tracking-tight">PhishGuard</h2>
          <p className="text-sm text-muted-foreground">
            DecodeLabs Cybersecurity Internship — Project 03
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>About this project</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-3 text-sm text-muted-foreground">
          <p>
            PhishGuard is a phishing awareness and email analysis platform built as a
            Blue Team SOC tool. It parses submitted emails, runs them through a rule-based
            detection engine covering URL structure, brand impersonation, and social-engineering
            language, and produces an explainable 0–100 risk score with actionable recommendations.
          </p>
          <p>
            Every score is fully traceable to the specific indicators that produced it — there
            is no opaque machine-learning model involved, which keeps the tool auditable and
            trustworthy for training and awareness purposes.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Technology Stack</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {TECH_STACK.map((tech) => (
              <span
                key={tech}
                className="rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium"
              >
                {tech}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FolderGit2 className="h-4 w-4" /> Source
          </CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">
          Part of the DecodeLabs-Internship-2026 repository, alongside the Password Strength
          Checker, CipherLab, and BlueShield Auditor projects.
        </CardContent>
      </Card>
    </div>
  )
}
