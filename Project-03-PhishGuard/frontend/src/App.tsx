import { Routes, Route, Navigate } from "react-router-dom"
import { AppLayout } from "@/components/layout/app-layout"
import { LandingPage } from "@/pages/landing"
import { DashboardPage } from "@/pages/dashboard"
import { AnalyzerPage } from "@/pages/analyzer"
import { HistoryPage } from "@/pages/history"
import { ScanDetailPage } from "@/pages/scan-detail"
import { ReportsPage } from "@/pages/reports"
import { StatisticsPage } from "@/pages/statistics"
import { SettingsPage } from "@/pages/settings"
import { AboutPage } from "@/pages/about"

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route element={<AppLayout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/analyzer" element={<AnalyzerPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/history/:id" element={<ScanDetailPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/statistics" element={<StatisticsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
