import { Component, type ErrorInfo, type ReactNode } from "react"
import { AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ErrorBoundaryProps {
  children: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("PhishGuard UI crashed:", error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background p-6 text-center text-foreground">
          <AlertTriangle className="h-10 w-10 text-critical" />
          <div>
            <h1 className="text-lg font-semibold">Something interrupted the page</h1>
            <p className="mt-1 max-w-md text-sm text-muted-foreground">
              This is often caused by a browser extension (translator, password manager, ad
              blocker) modifying the page. Try disabling extensions or reloading in a private
              window.
            </p>
          </div>
          <Button onClick={() => window.location.reload()}>Reload the page</Button>
        </div>
      )
    }

    return this.props.children
  }
}
