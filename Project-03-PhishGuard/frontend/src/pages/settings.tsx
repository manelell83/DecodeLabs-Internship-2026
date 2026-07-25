import { useEffect, useState } from "react"
import { useTheme } from "next-themes"
import { Sun, Moon, Laptop } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { API_BASE_URL } from "@/services/api"

const THEME_OPTIONS = [
  { value: "light", label: "Light", icon: Sun },
  { value: "dark", label: "Dark", icon: Moon },
  { value: "system", label: "System", icon: Laptop },
]

export function SettingsPage() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-4">
      <div>
        <h2 className="text-xl font-bold tracking-tight">Settings</h2>
        <p className="text-sm text-muted-foreground">
          Preferences are stored locally in your browser.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-2">
            {THEME_OPTIONS.map(({ value, label, icon: Icon }) => (
              <button
                key={value}
                onClick={() => setTheme(value)}
                className={cn(
                  "flex flex-col items-center gap-2 rounded-lg border border-border p-4 text-sm transition-colors cursor-pointer",
                  mounted && theme === value
                    ? "border-primary bg-primary/10 text-primary"
                    : "hover:bg-muted",
                )}
              >
                <Icon className="h-5 w-5" />
                {label}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>API Connection</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-2 text-sm">
          <p className="text-muted-foreground">
            The frontend communicates with the PhishGuard FastAPI backend at:
          </p>
          <code className="rounded-md bg-muted px-3 py-2 font-mono text-xs">{API_BASE_URL}</code>
          <p className="text-xs text-muted-foreground">
            Set <code className="font-mono">VITE_API_BASE_URL</code> in a <code className="font-mono">.env</code> file to point at a different backend.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Local Data</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Reset theme preference stored in this browser.
          </p>
          <Button variant="outline" size="sm" onClick={() => setTheme("system")}>
            Reset
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
