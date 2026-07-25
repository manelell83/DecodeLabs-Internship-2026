"""Generates JSON and PDF reports for a completed audit run."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.exceptions import ReportGenerationError
from app.models.audit_run import AuditRun

_LEVEL_HEX = {
    "Excellent": "#16a34a",
    "Good": "#0ea5b7",
    "Fair": "#ca8a04",
    "Poor": "#dc2626",
}


class ReportGenerator:
    """Builds JSON and PDF report artifacts for an audit run and writes them to disk."""

    def __init__(self, reports_dir: Path) -> None:
        self._reports_dir = reports_dir
        self._reports_dir.mkdir(parents=True, exist_ok=True)

    def build_json(self, audit_run: AuditRun) -> dict:
        return {
            "id": audit_run.id,
            "created_at": audit_run.created_at.isoformat(),
            "mode": audit_run.mode,
            "hostname": audit_run.hostname,
            "os_summary": audit_run.os_summary,
            "score": audit_run.score,
            "level": audit_run.level,
            "summary": audit_run.summary,
            "findings": [
                {
                    "category": f.category,
                    "status": f.status,
                    "severity": f.severity,
                    "description": f.description,
                    "evidence": f.evidence,
                    "recommendation": f.recommendation,
                    "weight": f.weight,
                    "source": f.source,
                }
                for f in audit_run.findings
            ],
        }

    def write_json(self, audit_run: AuditRun) -> Path:
        try:
            path = self._reports_dir / f"audit_{audit_run.id}.json"
            path.write_text(json.dumps(self.build_json(audit_run), indent=2), encoding="utf-8")
            return path
        except OSError as exc:
            raise ReportGenerationError(str(exc)) from exc

    def write_pdf(self, audit_run: AuditRun) -> Path:
        try:
            path = self._reports_dir / f"audit_{audit_run.id}.pdf"
            doc = SimpleDocTemplate(str(path), pagesize=letter, title=f"BlueShield Audit Report #{audit_run.id}")
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "BlueShieldTitle", parent=styles["Title"], textColor=colors.HexColor("#0b1220")
            )

            elements = [
                Paragraph("BlueShield Auditor — Security Audit Report", title_style),
                Spacer(1, 0.15 * inch),
                Paragraph(f"Audit ID: {audit_run.id}", styles["Normal"]),
                Paragraph(f"Generated: {datetime.now(timezone.utc).isoformat()}", styles["Normal"]),
                Paragraph(f"Hostname: {audit_run.hostname or 'Unknown'}", styles["Normal"]),
                Paragraph(f"Operating System: {audit_run.os_summary or 'Unknown'}", styles["Normal"]),
                Paragraph(f"Mode: {audit_run.mode}", styles["Normal"]),
                Spacer(1, 0.2 * inch),
                Paragraph(
                    f"Security Score: <b>{audit_run.score}/100</b> &nbsp;&nbsp; Level: "
                    f"<font color='{_LEVEL_HEX.get(audit_run.level, '#000000')}'>"
                    f"<b>{audit_run.level}</b></font>",
                    styles["Normal"],
                ),
                Spacer(1, 0.1 * inch),
                Paragraph(audit_run.summary, styles["Normal"]),
                Spacer(1, 0.3 * inch),
                Paragraph("Findings", styles["Heading2"]),
            ]

            if audit_run.findings:
                table_data = [["Category", "Status", "Severity", "Description", "Recommendation"]]
                for f in audit_run.findings:
                    table_data.append(
                        [
                            f.category.replace("_", " ").title(),
                            f.status.title(),
                            f.severity,
                            Paragraph(f.description, styles["Normal"]),
                            Paragraph(f.recommendation, styles["Normal"]),
                        ]
                    )
                table = Table(table_data, colWidths=[1.0 * inch, 0.7 * inch, 0.7 * inch, 1.8 * inch, 2.0 * inch])
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b1220")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTSIZE", (0, 0), (-1, -1), 8),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f7")]),
                        ]
                    )
                )
                elements.append(table)
            else:
                elements.append(Paragraph("No findings were recorded.", styles["Normal"]))

            doc.build(elements)
            return path
        except OSError as exc:
            raise ReportGenerationError(str(exc)) from exc
